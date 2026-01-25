# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-chess",
# ]
# ///

import sys
import json
import argparse
import chess
import chess.engine

TIME_LIMIT = 0.5  # seconds per move/analysis


def main():
    parser = argparse.ArgumentParser(description="Analyze FENs with UCI chess engines.")
    parser.add_argument("filename", nargs="?", default="fens.txt", help="Path to the file containing FEN strings.")
    parser.add_argument("--engine", action="append", required=True, help="Path to an engine executable. Can be provided multiple times.")
    args = parser.parse_args()

    filename = args.filename

    try:
        with open(filename, "r") as f:
            fens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found", file=sys.stderr)
        return

    # Initialize engines
    engines = []
    for path in args.engine:
        try:
            engine = chess.engine.SimpleEngine.popen_uci(path)
            name = engine.id.get("name", "Unknown Engine")
            if any(e[0] == name for e in engines):
                print(f"Error: Duplicate engine name: {name}", file=sys.stderr)
                engine.quit()
                for _, e in engines:
                    e.quit()
                return

            engines.append((name, engine))
        except Exception as e:
            print(f"Error: Failed to start engine at {path}: {e}", file=sys.stderr)
            for _, e in engines:
                e.quit()
            return

    try:
        for i, fen in enumerate(fens):
            result = {"id": i, "fen": fen}

            # Use chess960=True to be safe with FRC FENs
            board = chess.Board(fen, chess960=True)

            for name, engine in engines:
                try:
                    info = engine.analyse(board, chess.engine.Limit(time=TIME_LIMIT))
                    score = info["score"].white()
                    result[name] = {
                        "score_cp": score.score(),
                        "mate": score.mate(),
                        "depth": info.get("depth"),
                        "nodes": info.get("nodes"),
                    }
                except Exception as e:
                    result[name] = {"error": str(e)}

            print(json.dumps(result))
            sys.stdout.flush()

    finally:
        for _, engine in engines:
            engine.quit()


if __name__ == "__main__":
    main()
