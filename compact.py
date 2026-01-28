import argparse
import json


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
        print(json.dumps(best[k]))


if __name__ == "__main__":
    main()
