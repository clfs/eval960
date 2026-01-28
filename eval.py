import argparse
import dataclasses
import json
import sys

import chess
import chess.engine


@dataclasses.dataclass
class Variation:
    multipv: int
    move: str
    score: int | None
    mate: int | None
    wins: int
    draws: int
    losses: int
    depth: int
    seldepth: int


@dataclasses.dataclass
class Result:
    id: int
    fen: str
    engine: str
    nodes: int
    time: float
    hashfull: int
    variations: list[Variation]


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
        default=1,
        help="set custom number of threads to use (default: 1)",
    )
    parser.add_argument(
        "--nodes",
        type=int,
        metavar="N",
        default=100000,
        help="set soft node limit for analysis (default: 100000)",
    )
    parser.add_argument(
        "--hash",
        type=int,
        metavar="N",
        default=1024,
        help="set custom hash size in MB (default: 1024)",
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

        stockfish.configure(
            {"UCI_ShowWDL": True, "Threads": args.threads, "Hash": args.hash}
        )

        limit = chess.engine.Limit(nodes=args.nodes)

        for n in sorted(ids):
            board = chess.Board.from_chess960_pos(n)
            info = stockfish.analyse(board, limit, multipv=args.multipv)

            variations = []
            for d in info:
                variations.append(
                    Variation(
                        multipv=d["multipv"],
                        move=d["pv"][0].uci(),
                        score=d["score"].white().score(),
                        mate=d["score"].white().mate(),
                        wins=d["wdl"].white().wins,
                        draws=d["wdl"].white().draws,
                        losses=d["wdl"].white().losses,
                        depth=d["depth"],
                        seldepth=d["seldepth"],
                    )
                )

            result = Result(
                id=n,
                fen=board.fen(),
                engine=name,
                nodes=info[0]["nodes"],
                time=info[0]["time"],
                hashfull=info[0]["hashfull"],
                variations=variations,
            )
            print(json.dumps(dataclasses.asdict(result)))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
