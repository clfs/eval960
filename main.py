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
    parser = argparse.ArgumentParser(
        description="Analyze Chess960 FENs with UCI chess engines."
    )
    parser.add_argument(
        "--position",
        type=int,
        metavar="N",
        default=None,
        help="Specific Chess960 position ID to analyze (0-959). Default is to analyze all 960 positions.",
    )
    parser.add_argument(
        "--engine",
        action="append",
        required=True,
        help="Path to an engine executable. Can be provided multiple times.",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=0.5,
        help="Time limit for analysis in seconds (default: 0.5).",
    )
    args = parser.parse_args()

    # Determine which positions to analyze
    if args.position is not None:
        if not (0 <= args.position <= 959):
            raise ValueError("Position ID must be between 0 and 959.")
        positions = [args.position]
    else:
        positions = range(960)

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

        for pos_id in positions:
            board = chess.Board()
            board.set_chess960_pos(pos_id)
            fen = board.fen()

            result = {"id": pos_id, "fen": fen}

            for name, engine in engines:
                result[name] = analyze_position(engine, board, args.time_limit)

            print(json.dumps(result))
            sys.stdout.flush()

    finally:
        for _, engine in engines:
            engine.quit()


if __name__ == "__main__":
    main()
