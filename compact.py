import argparse
import json
import sys
import typing

# {"id":742,"fen":"rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1","engine":"Stockfish 17.1","nodes":100070,"time":0.172,"hashfull":0,"variations":[{"multipv":1,"score":35,"mate":null,"wins":90,"draws":902,"losses":8,"depth":17,"seldepth":17,"pv":"d2d4 d7d5"}]}


def main():
    parser = argparse.ArgumentParser(
        description="Output the best analysis for each position-engine pair.",
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="one or more .jsonl files",
    )
    args = parser.parse_args()

    best = {}

    for path in args.files:
        with open(path, "r") as f:
            for line in f:
                entry = json.loads(line.strip())

                # Deduplicate by position ID and engine name.
                key = (entry["id"], entry["engine"])

                # Ignore entries with lower node counts.
                if key in best:
                    if entry["nodes"] <= best[key]["nodes"]:
                        continue

                best[key] = entry

    for k in sorted(best.keys()):
        print(json.dumps(best[k]), separators=(",", ":"))


if __name__ == "__main__":
    main()
