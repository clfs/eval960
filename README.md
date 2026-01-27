# eval960

Stockfish evaluations for all Chess960 positions.

Requirements:

- [`uv`](https://github.com/astral-sh/uv) (`brew install uv`)
- [`stockfish`](https://github.com/official-stockfish/Stockfish/) (`brew install stockfish`)

Usage:

```plaintext
; uv run main.py -h
usage: main.py [-h] --stockfish PATH [--id N | --range M-N] [--threads N]
               [--depth N] [--hash N]

Analyze Chess960 starting positions with Stockfish.

options:
  -h, --help        show this help message and exit
  --stockfish PATH  path to the Stockfish executable
  --id N            analyze position N; can be provided multiple times
  --range M-N       analyze positions M through N inclusive
  --threads N       set custom number of threads to use
  --depth N         set custom depth limit for analysis
  --hash N          set custom hash size in MB

If neither --id nor --range is provided, all 960 positions are analyzed.
```

Example:

```plaintext
; uv run main.py --stockfish $(which stockfish) --id 50 --depth 10
{"id": 50, "fen": "bnnrqbkr/pppppppp/8/8/8/8/PPPPPPPP/BNNRQBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": [{"depth": 10, "seldepth": 14, "multipv": 1, "score": {"cp": 76, "mate": null}, "wdl": {"win": 298, "draw": 700, "loss": 2}, "nodes": 13759, "hashfull": 6, "time": 0.023, "pv": ["e2e4", "c7c5", "h2h4", "h7h5", "h1h3", "b7b6", "c2c4", "h8h6", "b2b3", "e7e5", "b1c3", "a7a6"]}]}
```
