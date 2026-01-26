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
; uv run main.py --stockfish $(which stockfish) --id 10
{"id": 10, "fen": "qnnrbbkr/pppppppp/8/8/8/8/PPPPPPPP/QNNRBBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 20, "seldepth": 28, "multipv": 1, "score": {"cp": 41, "mate": null}, "wdl": {"win": 111, "draw": 882, "loss": 7}, "nodes": 255961, "nps": 610885, "hashfull": 97, "tbhits": 0, "time": 0.419, "pv": ["c2c4", "h7h5", "h2h4", "c7c5", "b1c3", "c8b6", "c1b3", "b6c4", "e2e3", "c4b6", "b3c5", "d7d5", "d2d4", "e7e6", "h1h3", "h8h6", "e3e4", "d5e4", "c3e4"]}}
```
