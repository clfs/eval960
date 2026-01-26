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
from dataclasses import dataclass, asdict
from typing import Optional

import chess
import chess.engine


@dataclass
class AnalysisResult:
    score_cp: Optional[int]
    mate: Optional[int]
    depth: Optional[int]
    nodes: Optional[int]
    win: Optional[int] = None
    draw: Optional[int] = None
    loss: Optional[int] = None


def analyze_position(engine, board, time_limit) -> AnalysisResult:
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    score = info["score"].white()
    wdl = info.get("wdl")

    win, draw, loss = None, None, None
    if wdl:
        wdl_white = wdl.white()
        win = wdl_white.wins
        draw = wdl_white.draws
        loss = wdl_white.losses

    return AnalysisResult(
        score_cp=score.score(),
        mate=score.mate(),
        depth=info.get("depth"),
        nodes=info.get("nodes"),
        win=win,
        draw=draw,
        loss=loss,
    )


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
        required=True,
        help="Path to an engine executable.",
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

    # Initialize engine
    engine = None
    path = args.engine
    try:
        try:
            engine = chess.engine.SimpleEngine.popen_uci(path)
        except Exception as e:
            raise RuntimeError(f"Failed to start engine at {path}: {e}") from e

        name = engine.id.get("name")
        if not name:
            raise ValueError(f"Could not determine name for engine at {path}")

        if "UCI_ShowWDL" in engine.options:
            engine.configure({"UCI_ShowWDL": True})

        for pos_id in positions:
            board = chess.Board()
            board.set_chess960_pos(pos_id)
            fen = board.fen()

            analysis = asdict(analyze_position(engine, board, args.time_limit))
            result = {"id": pos_id, "fen": fen, "engine": name, **analysis}

            print(json.dumps(result))
            sys.stdout.flush()

    finally:
        if engine:
            engine.quit()


if __name__ == "__main__":
    main()
