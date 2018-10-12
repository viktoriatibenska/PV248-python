import scorelib as module
import sys

if __name__ == "__main__":
    # sys.stdout = open("output.txt", "w", encoding="utf-8")
    prints = module.load(sys.argv[1])

    for p in prints:
        p.format()
        print()
