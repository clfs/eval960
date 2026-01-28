import argparse
import csv
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Convert a JSONL analysis to CSV.")
    parser.add_argument(
        "file",
        metavar="FILE",
        help="a .jsonl file",
    )
    args = parser.parse_args()

    fieldnames = [
        "id",
        "fen",
        "engine",
        "nodes",
        "time",
        "hashfull",
        "multipv",
        "move",
        "score",
        "mate",
        "wins",
        "draws",
        "losses",
        "depth",
        "seldepth",
    ]

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    with open(args.file, "r") as f:
        for line in f:
            data = json.loads(line.strip())

            base_row = {
                "id": data["id"],
                "fen": data["fen"],
                "engine": data["engine"],
                "nodes": data["nodes"],
                "time": data["time"],
                "hashfull": data["hashfull"],
            }

            for v in data["variations"]:
                row = base_row.copy()
                row.update(
                    {
                        "multipv": v["multipv"],
                        "move": v["move"],
                        "score": v["score"],
                        "mate": v["mate"],
                        "wins": v["wins"],
                        "draws": v["draws"],
                        "losses": v["losses"],
                        "depth": v["depth"],
                        "seldepth": v["seldepth"],
                    }
                )
                writer.writerow(row)


if __name__ == "__main__":
    main()
