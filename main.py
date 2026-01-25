# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "stockfish>=4.0.6",
# ]
# ///
import dataclasses
import json
import stockfish

# Sample output from stockfish.get_top_moves(verbose=True):
# [{'Move': 'a2a4', 'Centipawn': 26, 'Mate': None, 'Time': 1, 'Nodes': 11031, 'MultiPVNumber': 1, 'NodesPerSecond': 11031000, 'SelectiveDepth': 9, 'PVMoves': 'a2a4 a7a5 e2e4 f7f5 e4f5 g7g6', 'WDL': '68 921 11'}]

DEPTH = 30
THREADS = 8
HASH = 16384


@dataclasses.dataclass
class TopMove:
    move: str
    centipawns: int | None
    mate: int | None
    multipv_number: int
    selective_depth: int
    pv_moves: list[str]
    win: int
    draw: int
    loss: int

    @classmethod
    def from_stockfish(cls, info: dict) -> "TopMove":
        win, draw, loss = map(int, info["WDL"].split())
        return cls(
            move=info["Move"],
            centipawns=info.get("Centipawn"),
            mate=info.get("Mate"),
            multipv_number=info["MultiPVNumber"],
            selective_depth=info["SelectiveDepth"],
            pv_moves=info["PVMoves"].split(),
            win=win,
            draw=draw,
            loss=loss,
        )


@dataclasses.dataclass
class Result:
    numbering: int
    fen: str
    depth: int
    top_moves: list[TopMove]


def main() -> None:
    engine = stockfish.Stockfish(
        path="/opt/homebrew/bin/stockfish",
        depth=DEPTH,
        parameters={"Threads": THREADS, "Hash": HASH, "UCI_Chess960": True},
    )

    with open("fens.txt") as f:
        fens = f.read().splitlines()

    for i, fen in enumerate(fens):
        engine.set_fen_position(fen)
        info = engine.get_top_moves(num_top_moves=5, verbose=True)
        top_moves = [TopMove.from_stockfish(move) for move in info]
        result = Result(
            numbering=i,
            fen=fen,
            depth=DEPTH,
            top_moves=top_moves,
        )
        print(json.dumps(dataclasses.asdict(result)))


if __name__ == "__main__":
    main()
