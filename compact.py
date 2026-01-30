import argparse
import csv
import dataclasses
import sys

from eval import Result


def main():
    parser = argparse.ArgumentParser(
        description="For each (id, engine) pair, output the analysis with the highest node count.",
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="one or more .csv files",
    )
    args = parser.parse_args()

    best = {}
    fieldnames = [f.name for f in dataclasses.fields(Result)]

    for path in args.files:
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for entry in reader:
                # Convert numeric fields for correct sorting/comparison.
                entry["id"] = int(entry["id"])
                entry["nodes"] = int(entry["nodes"])

                # Deduplicate by position ID and engine name.
                key = (entry["id"], entry["engine"])

                # Ignore entries with lower node counts.
                if key in best:
                    if entry["nodes"] <= best[key]["nodes"]:
                        continue

                best[key] = entry

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for k in sorted(best.keys()):
        writer.writerow(best[k])


if __name__ == "__main__":
    main()
