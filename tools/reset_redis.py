"""
tools.reset_redis
-----------------
Löscht alle GFX-relevanten Redis-Keys.
"""

from core.redis import delete_pattern


def main():
    print("Deleting keys: gfx:*")
    n1 = delete_pattern("*")

    print("Deleting keys: event:*")
    n2 = delete_pattern("event:*")

    print("Deleting keys: startlist:*")
    n3 = delete_pattern("startlist:*")

    print(f"Done. Deleted {n1 + n2 + n3} keys.")


if __name__ == "__main__":
    main()

