import argparse
import csv

import dataclasses
import sys

from eval import Result


def parse_result(d: dict) -> Result:
    return Result(
        id=int(d["id"]),
        fen=d["fen"],
        engine=d["engine"],
        depth=int(d["depth"]),
        seldepth=int(d["seldepth"]),
        multipv=int(d["multipv"]),
        score=int(d["score"]) if d["score"] else None,
        mate=int(d["mate"]) if d["mate"] else None,
        wins=int(d["wins"]),
        draws=int(d["draws"]),
        losses=int(d["losses"]),
        nodes=int(d["nodes"]),
        time=float(d["time"]),
        hashfull=int(d["hashfull"]),
        pv=d["pv"],
    )


def main():
    parser = argparse.ArgumentParser(
        description="Merge CSV files containing analyses.",
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="CSV files to merge",
    )
    args = parser.parse_args()

    if len(args.files) < 2:
        parser.error("At least two files are required.")

    fieldnames = [f.name for f in dataclasses.fields(Result)]
    results = {}

    for path in args.files:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                raise ValueError(f"Error: {path} appears to be empty.")

            if set(reader.fieldnames) != set(fieldnames):
                raise ValueError(
                    f"Error: Header mismatch in {path}. Expected {fieldnames}, got {reader.fieldnames}"
                )

            for row in reader:
                result = parse_result(row)
                key = (result.id, result.depth, result.multipv, result.engine)

                if key in results:
                    existing = results[key]
                    if result.nodes > existing.nodes:
                        results[key] = result
                    elif result.nodes == existing.nodes:
                        if result.time > existing.time:
                            results[key] = result
                else:
                    results[key] = result

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for key in sorted(results.keys()):
        row = dataclasses.asdict(results[key])
        writer.writerow(row)

    sys.stdout.flush()


if __name__ == "__main__":
    main()
