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

    # Determine which positions to analyze
    if args.position is not None:
        if not (0 <= args.position <= 959):
            raise ValueError("Position ID must be between 0 and 959.")
        positions = [args.position]
    else:
        positions = range(960)

    # Initialize Stockfish
    stockfish = None
    path = args.stockfish
    try:
        stockfish = chess.engine.SimpleEngine.popen_uci(path)
    except Exception as e:
        raise RuntimeError(f"Failed to start Stockfish at {path}: {e}") from e

    name = stockfish.id.get("name")
    if not name:
        raise ValueError(f"Could not determine name for Stockfish at {path}")

    stockfish.configure({"UCI_ShowWDL": True})

    for pos_id in positions:
        board = chess.Board()
        board.set_chess960_pos(pos_id)
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

        print(json.dumps(result, cls=ChessEncoder))
        sys.stdout.flush()

    stockfish.quit()


if __name__ == "__main__":
    main()
