# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-chess",
# ]
# ///

import json
import argparse
import chess
import chess.engine


class ChessEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, chess.engine.PovScore):
            score = obj.white()
            return {"cp": score.score(), "mate": score.mate()}
        if isinstance(obj, chess.engine.PovWdl):
            wdl = obj.white()
            return {"win": wdl.wins, "draw": wdl.draws, "loss": wdl.losses}
        if isinstance(obj, chess.Move):
            return obj.uci()
        return super().default(obj)


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

        for n in sorted(ids):
            board = chess.Board.from_chess960_pos(n)
            info = stockfish.analyse(board, limit)

            # The "string" key only contains the last "info string ..." message
            # from the engine, so drop it until the library provides a better
            # way to capture all messages.
            info.pop("string", None)

            result = {
                "id": n,
                "fen": board.fen(),
                "engine": name,
                "info": info,
            }

            print(json.dumps(result, cls=ChessEncoder), flush=True)


if __name__ == "__main__":
    main()
