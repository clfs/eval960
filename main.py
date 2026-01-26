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
        description="Analyze all Chess960 starting positions with Stockfish."
    )
    parser.add_argument(
        "--stockfish",
        type=str,
        metavar="PATH",
        required=True,
        help="Path to the Stockfish executable.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--id",
        type=int,
        action="append",
        help="Specific position ID to analyze. Can be used multiple times.",
    )
    group.add_argument(
        "--range",
        type=str,
        metavar="START-END",
        help="Range of position IDs to analyze (e.g. 5-10).",
    )

    parser.add_argument(
        "--threads",
        type=int,
        metavar="N",
        default=None,
        help="Set custom number of threads to use.",
    )
    parser.add_argument(
        "--depth",
        type=int,
        metavar="N",
        default=20,
        help="Set custom depth limit for analysis.",
    )
    parser.add_argument(
        "--hash",
        type=int,
        metavar="N",
        default=None,
        help="Set custom hash size in MB.",
    )
    args = parser.parse_args()

    ids = set()
    if args.id:
        ids.update(args.id)
    if args.range:
        try:
            start, end = map(int, args.range.split("-"))
            if start > end:
                raise ValueError
            ids.update(range(start, end + 1))
        except ValueError:
            parser.error(f"Invalid value for --range: {args.range}")

    if not ids:
        position_list = range(960)
    else:
        position_list = sorted(ids)

    if any(i not in range(960) for i in position_list):
        parser.error("Position IDs must be between 0 and 959.")

    with chess.engine.SimpleEngine.popen_uci(args.stockfish) as stockfish:
        name = stockfish.id["name"]

        options = {"UCI_ShowWDL": True}
        if args.threads:
            options["Threads"] = args.threads
        if args.hash:
            options["Hash"] = args.hash
        stockfish.configure(options)

        for n in position_list:
            board = chess.Board.from_chess960_pos(n)
            info = stockfish.analyse(board, chess.engine.Limit(depth=args.depth))

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
