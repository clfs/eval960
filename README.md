# eval960

Stockfish evaluations for all Chess960 positions.

Requirements:

- [`uv`](https://github.com/astral-sh/uv) (`brew install uv`)
- [`stockfish`](https://github.com/official-stockfish/Stockfish/) (`brew install stockfish`)

Usage:

```plaintext
; uv run main.py -h
usage: main.py [-h] --stockfish PATH [--id N] [--threads N] [--depth N] [--hash N]

Analyze all Chess960 starting positions with Stockfish.

options:
  -h, --help        show this help message and exit
  --stockfish PATH  Path to the Stockfish executable.
  --id N            Only analyze the specified position (0-959).
  --threads N       Set custom number of threads to use.
  --depth N         Set custom depth limit for analysis.
  --hash N          Set custom hash size in MB.
```

Example:

```plaintext
; uv run main.py --stockfish /opt/homebrew/bin/stockfish --depth 20
{"id": 0, "fen": "bbqnnrkr/pppppppp/8/8/8/8/PPPPPPPP/BBQNNRKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 20, "seldepth": 25, "multipv": 1, "score": {"cp": 17, "mate": null}, "wdl": {"win": 50, "draw": 935, "loss": 15}, "nodes": 524927, "nps": 569335, "hashfull": 192, "tbhits": 0, "time": 0.922, "pv": ["h2h4", "h7h5", "c2c4", "c7c5", "b2b3", "b7b6", "h1h3", "e7e6", "e1f3", "d8c6", "e2e3", "c6e7", "d2d4", "h8h6", "d4c5", "b6c5", "d1c3", "e7g6", "e3e4"]}}
{"id": 1, "fen": "bqnbnrkr/pppppppp/8/8/8/8/PPPPPPPP/BQNBNRKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 20, "seldepth": 25, "multipv": 1, "score": {"cp": 19, "mate": null}, "wdl": {"win": 53, "draw": 933, "loss": 14}, "nodes": 556054, "nps": 543552, "hashfull": 202, "tbhits": 0, "time": 1.023, "pv": ["b2b4", "b7b5", "h2h4", "h7h5", "e2e3", "e7e6", "e1f3", "c8e7", "c1d3", "e7g6", "d3e5", "g6e5", "f3e5", "e8f6", "h1h3", "d7d6", "e5f3", "h8h6", "f3g5", "c7c5", "b4c5", "d6c5", "c2c4"]}}
{"id": 2, "fen": "bqnnrbkr/pppppppp/8/8/8/8/PPPPPPPP/BQNNRBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "info": {"depth": 20, "seldepth": 34, "multipv": 1, "score": {"cp": 31, "mate": null}, "wdl": {"win": 80, "draw": 911, "loss": 9}, "nodes": 528099, "nps": 529157, "hashfull": 194, "tbhits": 0, "time": 0.998, "pv": ["h2h4", "h7h5", "b2b4", "b7b5", "e2e4", "e7e5", "a2a3", "h8h6", "h1h3", "a7a6", "c1b3", "c8b6", "d2d3", "d7d6", "h3g3", "c7c5", "c2c4", "d8e6", "d1e3", "b5c4", "d3c4", "b8d8", "a1c3", "d8h4"]}}
...
```
