import csv
import sys
import argparse
import chess
import chess.engine


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Chess960 starting positions with Stockfish.",
        epilog="If neither --id nor --range is provided, all 960 positions are analyzed.",
    )
    parser.add_argument(
        "--stockfish",
        type=str,
        metavar="PATH",
        required=True,
        help="path to the Stockfish executable",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--id",
        type=int,
        metavar="N",
        action="append",
        help="analyze position N; can be provided multiple times",
    )
    group.add_argument(
        "--range",
        type=str,
        metavar="M-N",
        help="analyze positions M through N inclusive",
    )

    parser.add_argument(
        "--multipv",
        type=int,
        metavar="N",
        default=1,
        help="number of principal variations (default: 1)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        metavar="N",
        default=None,
        help="set custom number of threads to use",
    )
    parser.add_argument(
        "--depth",
        type=int,
        metavar="N",
        default=20,
        help="set custom depth limit for analysis",
    )
    parser.add_argument(
        "--hash",
        type=int,
        metavar="N",
        default=None,
        help="set custom hash size in MB",
    )
    args = parser.parse_args()

    ids = set()
    if args.id:
        ids.update(args.id)
    elif args.range:
        start, end = map(int, args.range.split("-"))
        ids.update(range(start, end + 1))
    else:
        ids = set(range(960))

    with chess.engine.SimpleEngine.popen_uci(args.stockfish) as stockfish:
        name = stockfish.id["name"]

        options = {"UCI_ShowWDL": True}
        if args.threads:
            options["Threads"] = args.threads
        if args.hash:
            options["Hash"] = args.hash
        stockfish.configure(options)

        limit = chess.engine.Limit(depth=args.depth)

        fieldnames = [
            "id",
            "fen",
            "engine",
            "multipv",
            "cp",
            "mate",
            "wins",
            "draws",
            "losses",
            "depth",
            "nodes",
            "time",
            "hashfull",
            "pv",
        ]
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()

        for n in sorted(ids):
            board = chess.Board.from_chess960_pos(n)
            info = stockfish.analyse(board, limit, multipv=args.multipv)

            if isinstance(info, dict):
                info = [info]

            for entry in info:
                row = {
                    "id": n,
                    "fen": board.fen(),
                    "engine": name,
                    "multipv": entry["multipv"],
                    "depth": entry["depth"],
                    "nodes": entry["nodes"],
                    "time": entry["time"],
                    "hashfull": entry["hashfull"],
                    "cp": entry["score"].white().score(),
                    "mate": entry["score"].white().mate(),
                    "wins": entry["wdl"].white().wins,
                    "draws": entry["wdl"].white().draws,
                    "losses": entry["wdl"].white().losses,
                    "pv": " ".join(move.uci() for move in entry["pv"]),
                }

                writer.writerow(row)

            sys.stdout.flush()


if __name__ == "__main__":
    main()
