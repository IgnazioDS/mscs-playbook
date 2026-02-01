# Case Study: Timed Automata for Traffic Signals

## Overview
Traffic signals must enforce minimum green and red durations while responding
to vehicle presence. A timed automaton models these constraints for verification.

## Requirements
- Minimum green duration: 10s
- Maximum wait for cross traffic: 60s
- No conflicting greens

## Approach
- Model signal phases as timed automaton states.
- Verify that invariants hold for all transitions.
- Test edge cases where sensors fail.

## Outcomes
- Timing constraints enforced in all validated traces.
- Misconfigured timers detected by model checking.

## Pitfalls
- Clock resets at wrong transitions
- Missing sensor failure modes

