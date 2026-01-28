# eval960

Stockfish evaluations for all Chess960 positions.

Requirements:

- [`uv`](https://github.com/astral-sh/uv) (`brew install uv`)
- [`stockfish`](https://github.com/official-stockfish/Stockfish/) (`brew install stockfish`)

Help:

- `uv run eval.py -h`

Examples:

- `uv run eval.py --stockfish $(which stockfish) > results.csv`
