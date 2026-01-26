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

# {"id": 518, "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"string": "NNUE evaluation using nn-37f18f62d772.nnue (6MiB, (22528, 128, 15, 32, 1))", "depth": 30, "seldepth": 44, "multipv": 1, "score": {"cp": 22, "mate": null}, "wdl": {"win": 59, "draw": 928, "loss": 13}, "nodes": 6090037, "nps": 531834, "hashfull": 983, "tbhits": 0, "time": 11.451, "pv": ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "g8f6", "e1h1", "f6e4", "f1e1", "e4d6", "f3e5", "c6e5", "e1e5", "f8e7", "b5f1", "e8h8", "d2d4", "e7f6", "e5e1", "d6f5", "c2c3", "d7d5", "c1f4", "g7g6", "b1d2", "c7c6", "d2f3"]}}


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

    finally:
        if stockfish:
            stockfish.quit()


if __name__ == "__main__":
    main()
