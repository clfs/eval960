# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-chess",
# ]
# ///

import sys
import json
import chess
import chess.engine

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"
LC0_PATH = "/opt/homebrew/bin/lc0"
TIME_LIMIT = 0.5  # seconds per move/analysis


def main():
    filename = "fens.txt"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, "r") as f:
            fens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(json.dumps({"error": "fens.txt not found"}), file=sys.stderr)
        return

    # Initialize engines
    try:
        stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    except Exception as e:
        print(json.dumps({"error": f"Failed to start Stockfish: {e}"}), file=sys.stderr)
        return

    lc0 = None
    try:
        lc0 = chess.engine.SimpleEngine.popen_uci(LC0_PATH)
    except Exception as e:
        print(json.dumps({"error": f"Failed to start LC0: {e}"}), file=sys.stderr)
        stockfish.quit()
        return

    try:
        for i, fen in enumerate(fens):
            result = {"id": i, "fen": fen, "stockfish": None, "lc0": None}

            # Use chess960=True to be safe with FRC FENs
            board = chess.Board(fen, chess960=True)

            # Analyze with Stockfish
            try:
                info_sf = stockfish.analyse(board, chess.engine.Limit(time=TIME_LIMIT))
                score_sf = info_sf["score"].white()
                result["stockfish"] = {
                    "score_cp": score_sf.score(),
                    "mate": score_sf.mate(),
                    "depth": info_sf.get("depth"),
                    "nodes": info_sf.get("nodes"),
                }
            except Exception as e:
                result["stockfish"] = {"error": str(e)}

            # Analyze with Leela
            try:
                info_lc0 = lc0.analyse(board, chess.engine.Limit(time=TIME_LIMIT))
                score_lc0 = info_lc0["score"].white()
                result["lc0"] = {
                    "score_cp": score_lc0.score(),
                    "mate": score_lc0.mate(),
                    "depth": info_lc0.get("depth"),
                    "nodes": info_lc0.get("nodes"),
                }
            except Exception as e:
                result["lc0"] = {"error": str(e)}

            print(json.dumps(result))
            sys.stdout.flush()

    finally:
        if stockfish:
            stockfish.quit()
        if lc0:
            lc0.quit()


if __name__ == "__main__":
    main()
