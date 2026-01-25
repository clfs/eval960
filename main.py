# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///


def main() -> None:
    with open("fens.txt") as f:
        fens = f.read().splitlines()

    for i, fen in enumerate(fens):
        print(i, fen)


if __name__ == "__main__":
    main()
