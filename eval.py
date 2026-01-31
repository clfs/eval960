import argparse
import dataclasses
import csv
import sys

import chess
import chess.engine


@dataclasses.dataclass
class Result:
    id: int
    fen: str
    engine: str
    bestmove: str
    eval: float
    wins: int
    draws: int
    losses: int
    depth: int
    seldepth: int
    nodes: int
    time: float
    hashfull: int


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Chess960 starting positions with Stockfish.",
        epilog="If neither --id nor --range is provided, all 960 positions are analyzed.",
    )

    engine = parser.add_argument_group("engine configuration")
    engine.add_argument(
        "--stockfish",
        type=str,
        metavar="PATH",
        required=True,
        help="path to the Stockfish executable",
    )
    engine.add_argument(
        "--threads",
        type=int,
        metavar="N",
        default=1,
        help="set number of threads to use (default: 1)",
    )
    engine.add_argument(
        "--hash",
        type=int,
        metavar="N",
        default=1024,
        help="set hash size in MB (default: 1024)",
    )

    selection = parser.add_mutually_exclusive_group()
    selection.add_argument(
        "--id",
        type=int,
        metavar="N",
        action="append",
        help="analyze position N; can be provided multiple times",
    )
    selection.add_argument(
        "--range",
        type=str,
        metavar="M-N",
        help="analyze positions M through N inclusive",
    )

    limits = parser.add_argument_group("limits")
    limits.add_argument(
        "--depth",
        type=int,
        metavar="N",
        default=20,
        help="set a depth limit for each analysis (default: 20)",
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

    fields = [f.name for f in dataclasses.fields(Result)]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    sys.stdout.flush()

    with chess.engine.SimpleEngine.popen_uci(args.stockfish) as stockfish:
        name = stockfish.id["name"]

        stockfish.configure(
            {"UCI_ShowWDL": True, "Threads": args.threads, "Hash": args.hash}
        )

        limit = chess.engine.Limit(depth=args.depth)

        for n in sorted(ids):
            board = chess.Board.from_chess960_pos(n)
            info = stockfish.analyse(board, limit)

            result = Result(
                id=n,
                fen=board.fen(),
                engine=name,
                bestmove=board.san(info["pv"][0]),
                eval=info["score"].white().score() / 100,
                wins=info["wdl"].white().wins,
                draws=info["wdl"].white().draws,
                losses=info["wdl"].white().losses,
                depth=info["depth"],
                seldepth=info["seldepth"],
                nodes=info["nodes"],
                time=info["time"],
                hashfull=info["hashfull"],
            )
            writer.writerow(dataclasses.asdict(result))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
