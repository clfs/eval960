# eval960

Stockfish evaluations for all Chess960 positions.

Requirements:

```plaintext
; brew install uv stockfish
```

- [uv](https://github.com/astral-sh/uv)
- [Stockfish](https://github.com/official-stockfish/Stockfish/)

Help:

```plaintext
; uv run eval.py -h
usage: eval.py [-h] --stockfish PATH [--id N | --range M-N] [--multipv N] [--threads N] [--nodes N] [--hash N]

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

Example:

```plaintext
; uv run eval.py --stockfish $(which stockfish) --id 742
{"id":742,"fen":"rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1","engine":"Stockfish 17.1","nodes":100070,"time":0.172,"hashfull":0,"variations":[{"multipv":1,"score":35,"mate":null,"wins":90,"draws":902,"losses":8,"depth":17,"seldepth":17,"pv":"d2d4 d7d5"}]}
```
