import os
import sys

# Projekt-Root zum Python-Pfad hinzufügen
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

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
