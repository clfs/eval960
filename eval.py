import argparse
import csv
import dataclasses
import sys

import chess
import chess.engine


@dataclasses.dataclass
class Result:
    id: int
    fen: str
    engine: str
    depth: int
    seldepth: int
    multipv: int
    score: int | None
    mate: int | None
    wins: int
    draws: int
    losses: int
    nodes: int
    time: float
    hashfull: int
    pv: str


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

        fieldnames = [f.name for f in dataclasses.fields(Result)]
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()

        for n in sorted(ids):
            board = chess.Board.from_chess960_pos(n)
            info = stockfish.analyse(board, limit, multipv=args.multipv)

            if isinstance(info, dict):
                info = [info]

            for entry in info:
                result = Result(
                    id=n,
                    fen=board.fen(),
                    engine=name,
                    depth=entry["depth"],
                    seldepth=entry["seldepth"],
                    multipv=entry["multipv"],
                    score=entry["score"].white().score(),
                    mate=entry["score"].white().mate(),
                    wins=entry["wdl"].white().wins,
                    draws=entry["wdl"].white().draws,
                    losses=entry["wdl"].white().losses,
                    nodes=entry["nodes"],
                    time=entry["time"],
                    hashfull=entry["hashfull"],
                    pv=" ".join(move.uci() for move in entry["pv"]),
                )
                writer.writerow(dataclasses.asdict(result))

            sys.stdout.flush()


if __name__ == "__main__":
    main()
