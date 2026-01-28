# eval960

Stockfish evaluations for all Chess960 positions.

## Requirements

```plaintext
; brew install uv stockfish
```

- [uv](https://github.com/astral-sh/uv)
- [Stockfish](https://github.com/official-stockfish/Stockfish/)

## Usage

```plaintext
; uv run eval.py -h
usage: eval.py [-h] --stockfish PATH [--id N | --range M-N] [--multipv N]
               [--threads N] [--nodes N] [--hash N]

Analyze Chess960 starting positions with Stockfish.

options:
  -h, --help        show this help message and exit
  --stockfish PATH  path to the Stockfish executable
  --id N            analyze position N; can be provided multiple times
  --range M-N       analyze positions M through N inclusive
  --multipv N       number of principal variations (default: 1)
  --threads N       set custom number of threads to use (default: 1)
  --nodes N         set soft node limit for analysis (default: 100000)
  --hash N          set custom hash size in MB (default: 1024)

If neither --id nor --range is provided, all 960 positions are analyzed.
```

```plaintext
; uv run compact.py -h
usage: compact.py [-h] FILE [FILE ...]

Output the best analysis for each position-engine pair.

positional arguments:
  FILE        one or more .jsonl files

options:
  -h, --help  show this help message and exit
```

## Examples

Analyze positions 20 through 25:

```plaintext
; uv run eval.py --stockfish $(which stockfish) --range 20-25
{"id": 20, "fen": "nbbqnrkr/pppppppp/8/8/8/8/PPPPPPPP/NBBQNRKR w KQkq - 0 1", "engine": "Stockfish 17.1", "nodes": 100055, "time": 0.177, "hashfull": 0, "variations": [{"multipv": 1, "move": "c2c4", "score": 22, "mate": null, "wins": 60, "draws": 927, "losses": 13, "depth": 16, "seldepth": 22}]}
{"id": 21, "fen": "nqbbnrkr/pppppppp/8/8/8/8/PPPPPPPP/NQBBNRKR w KQkq - 0 1", "engine": "Stockfish 17.1", "nodes": 100087, "time": 0.163, "hashfull": 0, "variations": [{"multipv": 1, "move": "h2h4", "score": 22, "mate": null, "wins": 58, "draws": 929, "losses": 13, "depth": 17, "seldepth": 25}]}
{"id": 22, "fen": "nqbnrbkr/pppppppp/8/8/8/8/PPPPPPPP/NQBNRBKR w KQkq - 0 1", "engine": "Stockfish 17.1", "nodes": 100039, "time": 0.16, "hashfull": 0, "variations": [{"multipv": 1, "move": "d2d4", "score": 35, "mate": null, "wins": 91, "draws": 901, "losses": 8, "depth": 17, "seldepth": 20}]}
{"id": 23, "fen": "nqbnrkrb/pppppppp/8/8/8/8/PPPPPPPP/NQBNRKRB w KQkq - 0 1", "engine": "Stockfish 17.1", "nodes": 100028, "time": 0.174, "hashfull": 0, "variations": [{"multipv": 1, "move": "f1g1", "score": 24, "mate": null, "wins": 62, "draws": 926, "losses": 12, "depth": 14, "seldepth": 25}]}
{"id": 24, "fen": "nbqnbrkr/pppppppp/8/8/8/8/PPPPPPPP/NBQNBRKR w KQkq - 0 1", "engine": "Stockfish 17.1", "nodes": 100012, "time": 0.164, "hashfull": 0, "variations": [{"multipv": 1, "move": "d2d4", "score": 76, "mate": null, "wins": 299, "draws": 699, "losses": 2, "depth": 16, "seldepth": 22}]}
{"id": 25, "fen": "nqnbbrkr/pppppppp/8/8/8/8/PPPPPPPP/NQNBBRKR w KQkq - 0 1", "engine": "Stockfish 17.1", "nodes": 100052, "time": 0.174, "hashfull": 1, "variations": [{"multipv": 1, "move": "d2d4", "score": 38, "mate": null, "wins": 99, "draws": 894, "losses": 7, "depth": 16, "seldepth": 22}]}
```

Compact multiple analysis files:

```plaintext
; uv run compact.py x.jsonl y.jsonl > z.jsonl
```
