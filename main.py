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


def analyze_position(engine, board, depth) -> chess.engine.InfoDict:
    return engine.analyse(board, chess.engine.Limit(depth=depth))


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

            info = analyze_position(stockfish, board, args.depth)
            score = info["score"].white()
            wdl = info["wdl"].white()

            result = {
                "id": pos_id, 
                "fen": fen, 
                "engine": name,
                "score_cp": score.score(),
                "mate": score.mate(),
                "depth": info["depth"],
                "nodes": info["nodes"],
                "win": wdl.wins,
                "draw": wdl.draws,
                "loss": wdl.losses,
            }

            print(json.dumps(result))
            sys.stdout.flush()

    finally:
        if stockfish:
            stockfish.quit()


if __name__ == "__main__":
    main()
