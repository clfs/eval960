# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "stockfish>=4.0.6",
# ]
# ///
import dataclasses
import stockfish


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
        # [{'Move': 'a2a4', 'Centipawn': 26, 'Mate': None, 'Time': 1, 'Nodes': 11031, 'MultiPVNumber': 1, 'NodesPerSecond': 11031000, 'SelectiveDepth': 9, 'PVMoves': 'a2a4 a7a5 e2e4 f7f5 e4f5 g7g6', 'WDL': '68 921 11'}]
        top_move = info[0]
        result = Result(
            numbering=i,
            fen=fen,
            depth=DEPTH,
            best_move=top_move["Move"],
            centipawns=top_move["Centipawn"],
            principal_variation=top_move["PVMoves"].split(" "),
            win=int(top_move["WDL"].split(" ")[0]),
            draw=int(top_move["WDL"].split(" ")[1]),
            loss=int(top_move["WDL"].split(" ")[2]),
        )
        print(result)


if __name__ == "__main__":
    main()
