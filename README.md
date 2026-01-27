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
; uv run main.py --stockfish $(which stockfish) --id 10 --depth 5
{"id": 10, "fen": "qnnrbbkr/pppppppp/8/8/8/8/PPPPPPPP/QNNRBBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 1, "seldepth": 2, "multipv": 1, "score": {"cp": 12, "mate": null}, "wdl": {"win": 43, "draw": 939, "loss": 18}, "nodes": 20, "nps": 20000, "hashfull": 0, "tbhits": 0, "time": 0.001, "pv": ["d2d4"]}}
{"id": 10, "fen": "qnnrbbkr/pppppppp/8/8/8/8/PPPPPPPP/QNNRBBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 2, "seldepth": 3, "multipv": 1, "score": {"cp": 27, "mate": null}, "wdl": {"win": 71, "draw": 918, "loss": 11}, "nodes": 45, "nps": 45000, "hashfull": 0, "tbhits": 0, "time": 0.001, "pv": ["d2d4"]}}
{"id": 10, "fen": "qnnrbbkr/pppppppp/8/8/8/8/PPPPPPPP/QNNRBBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 3, "seldepth": 4, "multipv": 1, "score": {"cp": 40, "mate": null}, "wdl": {"win": 107, "draw": 886, "loss": 7}, "nodes": 74, "nps": 74000, "hashfull": 0, "tbhits": 0, "time": 0.001, "pv": ["d2d4"]}}
{"id": 10, "fen": "qnnrbbkr/pppppppp/8/8/8/8/PPPPPPPP/QNNRBBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 4, "seldepth": 6, "multipv": 1, "score": {"cp": 41, "mate": null}, "wdl": {"win": 108, "draw": 885, "loss": 7}, "nodes": 127, "nps": 127000, "hashfull": 0, "tbhits": 0, "time": 0.001, "pv": ["d2d4", "b7b5", "e2e3"]}}
{"id": 10, "fen": "qnnrbbkr/pppppppp/8/8/8/8/PPPPPPPP/QNNRBBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 5, "seldepth": 6, "multipv": 1, "score": {"cp": 63, "mate": null}, "wdl": {"win": 209, "draw": 788, "loss": 3}, "nodes": 217, "nps": 217000, "hashfull": 0, "tbhits": 0, "time": 0.001, "pv": ["d2d4"]}}
```
