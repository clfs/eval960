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

TIME_LIMIT = 0.5  # seconds per move/analysis


def analyze_position(engine, board, time_limit):
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    score = info["score"].white()
    wdl = info.get("wdl")

    data = {
        "score_cp": score.score(),
        "mate": score.mate(),
        "depth": info.get("depth"),
        "nodes": info.get("nodes"),
    }

    if wdl:
        wdl_white = wdl.white()
        data["win"] = wdl_white.wins
        data["draw"] = wdl_white.draws
        data["loss"] = wdl_white.losses

    return data


def main():
    parser = argparse.ArgumentParser(description="Analyze FENs with UCI chess engines.")
    parser.add_argument(
        "filename",
        nargs="?",
        default="fens.txt",
        help="Path to the file containing FEN strings.",
    )
    parser.add_argument(
        "--engine",
        action="append",
        required=True,
        help="Path to an engine executable. Can be provided multiple times.",
    )
    args = parser.parse_args()

    filename = args.filename

    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")

    with open(filename, "r") as f:
        fens = [line.strip() for line in f if line.strip()]

    # Initialize engines
    engines = []
    try:
        for path in args.engine:
            try:
                engine = chess.engine.SimpleEngine.popen_uci(path)
            except Exception as e:
                raise RuntimeError(f"Failed to start engine at {path}: {e}") from e

            name = engine.id.get("name")
            if not name:
                engine.quit()
                raise ValueError(f"Could not determine name for engine at {path}")

            if any(e[0] == name for e in engines):
                engine.quit()
                raise ValueError(f"Duplicate engine name: {name}")

            if "UCI_ShowWDL" in engine.options:
                engine.configure({"UCI_ShowWDL": True})

            engines.append((name, engine))

        for i, fen in enumerate(fens):
            result = {"id": i, "fen": fen}

            # Use chess960=True to be safe with FRC FENs
            board = chess.Board(fen, chess960=True)

            for name, engine in engines:
                result[name] = analyze_position(engine, board, TIME_LIMIT)

            print(json.dumps(result))
            sys.stdout.flush()

    finally:
        for _, engine in engines:
            engine.quit()


if __name__ == "__main__":
    main()
