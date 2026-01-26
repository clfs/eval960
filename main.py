# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-chess",
# ]
# ///

import sys
import os
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
        description="Analyze Chess960 FENs with Stockfish."
    )
    parser.add_argument(
        "--position",
        type=int,
        metavar="N",
        default=None,
        help="Specific Chess960 position ID to analyze (0-959). Default is to analyze all 960 positions.",
    )
    parser.add_argument(
        "--stockfish",
        required=True,
        help="Path to the Stockfish executable.",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=20,
        help="Depth limit for analysis (default: 20).",
    )
    args = parser.parse_args()

    if args.position is not None and args.position not in range(960):
        parser.error("Position ID must be between 0 and 959.")

    positions = [args.position] if args.position is not None else range(960)

    try:
        stockfish = chess.engine.SimpleEngine.popen_uci(args.stockfish)
    except Exception as e:
        raise RuntimeError(f"Failed to start Stockfish at {args.stockfish}: {e}") from e

    try:
        name = stockfish.id.get("name")
        if not name:
            raise ValueError(f"Engine did not provide an 'id name' response.")
        stockfish.configure({"UCI_ShowWDL": True})

        for pos_id in positions:
            board = chess.Board.from_chess960_pos(pos_id)
            fen = board.fen()

            info = stockfish.analyse(board, chess.engine.Limit(depth=args.depth))

            # The "string" key only contains the last "info string ..." message
            # from the engine, so drop it until the library provides a better
            # way to capture all messages.
            info.pop("string", None)

            result = {
                "id": pos_id,
                "fen": fen,
                "engine": name,
                "info": info,
            }

            print(json.dumps(result, cls=ChessEncoder), flush=True)
    finally:
        stockfish.quit()


if __name__ == "__main__":
    main()
