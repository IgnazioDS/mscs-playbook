from src.patterns.repository import InMemoryUserRepository, User


def test_repository_crud_and_query():
    repo = InMemoryUserRepository()
    alice = User("u1", "Alice", "gold")
    bob = User("u2", "Bob", "silver")

    repo.save(alice)
    repo.save(bob)

    assert repo.get("u1") == alice
    assert len(repo.list_all()) == 2
    assert repo.find_by_tier("gold") == [alice]

    all_users = repo.list_all()
    all_users.append(User("u3", "Eve", "gold"))
    assert repo.get("u3") is None
