# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "stockfish>=4.0.6",
# ]
# ///
import dataclasses
import json
import stockfish

# [{'Move': 'a2a4', 'Centipawn': 26, 'Mate': None, 'Time': 1, 'Nodes': 11031, 'MultiPVNumber': 1, 'NodesPerSecond': 11031000, 'SelectiveDepth': 9, 'PVMoves': 'a2a4 a7a5 e2e4 f7f5 e4f5 g7g6', 'WDL': '68 921 11'}]

DEPTH = 7

@dataclasses.dataclass
class Result:
    numbering: int
    fen: str
    depth: int
    best_move: str
    centipawns: int
    principal_variation: list[str]
    win: int
    draw: int
    loss: int

    @classmethod
    def from_stockfish(cls, numbering: int, fen: str, depth: int, info: dict) -> "Result":
        win, draw, loss = map(int, info["WDL"].split())
        return cls(
            numbering=numbering,
            fen=fen,
            depth=depth,
            best_move=info["Move"],
            centipawns=info["Centipawn"],
            principal_variation=info["PVMoves"].split(),
            win=win,
            draw=draw,
            loss=loss,
        )


def main() -> None:
    engine = stockfish.Stockfish(
        path="/opt/homebrew/bin/stockfish",
        depth=DEPTH,
        parameters={"Threads": 8, "Hash": 4096, "UCI_Chess960": True},
    )

    # FENs.txt contails the FEN list linked above:
    with open("fens.txt") as f:
        fens = f.read().splitlines()

    for i, fen in enumerate(fens):
        engine.set_fen_position(fen)
        info = engine.get_top_moves(num_top_moves=1, verbose=True)
        result = Result.from_stockfish(i, fen, DEPTH, info[0])
        print(result)


if __name__ == "__main__":
    main()
