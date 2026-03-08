# Sockets and Connection Lifecycle

## Key Ideas

- A socket is the operating-system abstraction that binds transport-layer communication to a process, which is why debugging often starts with ports, listening state, and endpoint tuples.
- TCP connection setup and teardown create visible state transitions such as `LISTEN`, `SYN-SENT`, `ESTABLISHED`, and `TIME-WAIT`, and those states explain many operational symptoms.
- The client and server do not perform identical steps: servers bind and listen first, while clients choose an ephemeral port and initiate `connect`.
- A connection is identified by its endpoint tuple, so one server port can support many simultaneous connections as long as the full tuple is distinct.
- Correct socket reasoning links application calls such as `bind`, `listen`, `accept`, `connect`, `send`, and `close` to the underlying packet exchange seen in traces.

## 1. What It Is

Applications do not speak directly in Ethernet frames or IP packets. They use **sockets**, which are operating-system objects representing communication endpoints. A socket couples a transport protocol with local and remote addressing information and exposes operations such as open, bind, listen, connect, read, write, and close.

### 1.1 Core Definitions

- A **socket** is an OS-managed communication endpoint.
- A **listening socket** waits for incoming connection attempts on a local address and port.
- An **established socket** represents one active transport conversation.
- An **ephemeral port** is a short-lived client-side port chosen dynamically by the OS.
- A **four-tuple** identifies a TCP connection by local IP, local port, remote IP, and remote port.
- A **backlog** is the queue capacity for pending inbound connections on a listening socket.
- **Half-close** means one direction of a TCP stream has been closed while the other remains open.

### 1.2 Why This Matters

Many practical questions are really socket-lifecycle questions:

- Why is the port open but connections still fail?
- Why are there many `TIME-WAIT` entries?
- Why can one server port accept many clients simultaneously?
- Why does a connection hang after the application calls `close`?

A good socket model connects application behavior to transport packets and kernel state.

## 2. Server and Client Lifecycle

### 2.1 Server Side

A typical TCP server performs these steps:

1. create a socket,
2. bind it to a local address and port,
3. mark it as listening,
4. accept inbound connections,
5. exchange data on per-connection sockets.

The listening socket is not the same object as each accepted connection socket.

### 2.2 Client Side

A typical TCP client:

1. creates a socket,
2. receives an ephemeral local port from the OS if one is not chosen explicitly,
3. initiates `connect`,
4. exchanges data,
5. closes the connection.

### 2.3 UDP Contrast

UDP sockets do not have the same connection-establishment lifecycle. A UDP socket may send datagrams without a TCP-style handshake or per-flow state machine, although the OS still tracks the local endpoint and optional peer association.

## 3. TCP State Transitions

TCP defines a state machine so that both endpoints agree on when a connection exists and when it has been closed.

Common states include:

- `LISTEN`
- `SYN-SENT`
- `SYN-RECEIVED`
- `ESTABLISHED`
- `FIN-WAIT-1`
- `CLOSE-WAIT`
- `LAST-ACK`
- `TIME-WAIT`

`TIME-WAIT` is especially important operationally because it helps prevent old delayed packets from being confused with packets from a new connection using the same tuple.

## 4. Multiplexing and Port Reuse

One server port such as `443` can handle many clients because each connection has a different tuple. For example:

```text
10.0.0.20:443 <-> 10.0.0.11:51514
10.0.0.20:443 <-> 10.0.0.12:51515
```

The local server port is the same, but the remote endpoints differ, so these are distinct connections.

This is why `ss -tuna` or `netstat` output often shows many established connections bound to one listening port.

## 5. Worked Example

Server:

```text
IP = 10.0.0.20
port = 443
```

Client:

```text
IP = 10.0.0.10
ephemeral port = 51514
```

### 5.1 Server Prepares to Accept

The server application:

1. creates a TCP socket,
2. binds to `10.0.0.20:443`,
3. calls `listen`.

Kernel state for the listening socket is now:

```text
LISTEN
```

### 5.2 Client Initiates Connect

The client creates a TCP socket and calls `connect(10.0.0.20:443)`.

Suppose the OS chooses local port `51514`. The client sends:

```text
SYN from 10.0.0.10:51514 to 10.0.0.20:443
```

Client state becomes:

```text
SYN-SENT
```

### 5.3 Server Responds

The server receives the SYN and replies:

```text
SYN-ACK from 10.0.0.20:443 to 10.0.0.10:51514
```

The server creates a new per-connection socket associated with the tuple:

```text
(10.0.0.20, 443, 10.0.0.10, 51514)
```

That new socket enters:

```text
SYN-RECEIVED
```

The original listening socket remains in `LISTEN`.

### 5.4 Client Completes the Handshake

The client replies with:

```text
ACK from 10.0.0.10:51514 to 10.0.0.20:443
```

Now both sides move to:

```text
ESTABLISHED
```

The server's `accept` call can return the new established socket.

### 5.5 Connection Close

If the client closes first, it sends `FIN` and eventually enters `TIME-WAIT` after the close sequence completes. The server may pass through `CLOSE-WAIT` and `LAST-ACK` before fully closing.

Verification: the listening socket stays in `LISTEN`, the accepted connection is identified by the four-tuple `(10.0.0.20, 443, 10.0.0.10, 51514)`, and both endpoints reach `ESTABLISHED` only after the SYN, SYN-ACK, and ACK exchange completes.

## 6. Pseudocode Pattern

```text
procedure tcp_server_lifecycle(local_ip, local_port):
    listener = create_socket("tcp")
    bind(listener, local_ip, local_port)
    listen(listener)

    while true:
        connection = accept(listener)
        handle_connection(connection)
        close(connection)
```

Time: `Theta(1)` worst case for each abstract lifecycle transition or individual `accept` event, ignoring application payload work and scheduler effects. Space: `Theta(1)` auxiliary space per control-path step beyond kernel socket buffers and queued connection state.

## 7. Common Mistakes

1. **Listening-socket confusion.** Treating the listening socket as the same object as each accepted connection obscures how one port can serve many clients; distinguish the passive listener from per-connection sockets.
2. **Port-only identity thinking.** Identifying a TCP connection only by the server port ignores the full four-tuple; simultaneous connections share ports but not complete endpoint tuples.
3. **TIME-WAIT panic.** Seeing many `TIME-WAIT` sockets and assuming the kernel is broken misses their purpose; they are part of correct TCP cleanup and delayed-packet protection.
4. **UDP lifecycle projection.** Expecting UDP sockets to exhibit TCP states such as `SYN-SENT` or `ESTABLISHED` applies the wrong mental model; UDP has a different service and state profile.
5. **Close-is-instant assumption.** Assuming `close` means the network conversation is immediately gone can hide half-close, buffered data, or orderly teardown behavior; inspect connection state transitions explicitly.

## 8. Practical Checklist

- [ ] Use `ss -tuna` to distinguish listening sockets from established connections.
- [ ] Identify TCP connections by the full local-and-remote endpoint tuple, not just one port.
- [ ] Check for `TIME-WAIT`, `CLOSE-WAIT`, or backlog pressure when connection churn is high.
- [ ] Relate `connect`, `accept`, and `close` calls to the SYN, ACK, and FIN packets seen in captures.
- [ ] Remember that the server's listening socket remains open while accepted sockets come and go.
- [ ] Treat UDP socket debugging as a separate model rather than a reduced form of the TCP state machine.

## 9. References

- Stevens, W. Richard, Bill Fenner, and Andrew M. Rudoff. 2003. *UNIX Network Programming, Volume 1* (3rd ed.). Addison-Wesley.
- Stevens, W. Richard, Kevin R. Fall, and Gary R. Wright. 2011. *TCP/IP Illustrated, Volume 1* (2nd ed.). Addison-Wesley.
- Postel, Jon. 1981. *Transmission Control Protocol*. RFC 793. <https://datatracker.ietf.org/doc/html/rfc793>
- Linux Foundation. *socket(7) manual page*. <https://man7.org/linux/man-pages/man7/socket.7.html>
- Linux Foundation. *tcp(7) manual page*. <https://man7.org/linux/man-pages/man7/tcp.7.html>
- Linux Foundation. *ss(8) manual page*. <https://man7.org/linux/man-pages/man8/ss.8.html>
- Kerrisk, Michael. 2010. *The Linux Programming Interface*. No Starch Press.
