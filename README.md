# eval960

Stockfish evaluations for all Chess960 positions.

- [View the results in Google Sheets](https://docs.google.com/spreadsheets/d/14g88i_mvk2ytQZdp_1tAvJE49pJC4-o6CuNqN4KDcBc/edit)
- [Download the results as a CSV](https://raw.githubusercontent.com/clfs/eval960/refs/heads/main/results.csv)
- [Use Datasette Lite to query the data in your browser](https://lite.datasette.io/?csv=https%3A%2F%2Fraw.githubusercontent.com%2Fclfs%2Feval960%2Frefs%2Fheads%2Fmain%2Fresults.csv#/data?sql=select+*+from+results)

## Requirements

```plaintext
; brew install uv stockfish
```

- [uv](https://github.com/astral-sh/uv)
- [Stockfish](https://github.com/official-stockfish/Stockfish/)

## Usage

```plaintext
; uv run eval.py -h
usage: eval.py [-h] --stockfish PATH [--id N | --range M-N] [--nodes N]
               [--depth N] [--threads N] [--hash N]

Analyze Chess960 starting positions with Stockfish.

options:
  -h, --help        show this help message and exit
  --stockfish PATH  path to the Stockfish executable
  --id N            analyze position N; can be provided multiple times
  --range M-N       analyze positions M through N inclusive
  --nodes N         set soft node limit for analysis
  --depth N         set depth limit for analysis
  --threads N       set number of threads to use (default: 1)
  --hash N          set hash size in MB (default: 1024)

If neither --id nor --range is provided, all 960 positions are analyzed.
```

```plaintext
; uv run compact.py -h
usage: compact.py [-h] FILE [FILE ...]

Output the best analysis for each position-engine pair.

positional arguments:
  FILE        one or more .csv files

options:
  -h, --help  show this help message and exit
```

## Examples

Analyze positions 20 through 25:

```plaintext
; uv run eval.py --stockfish $(which stockfish) --range 20-25
id,fen,engine,move,score,wins,draws,losses,depth,seldepth,nodes,time,hashfull
20,nbbqnrkr/pppppppp/8/8/8/8/PPPPPPPP/NBBQNRKR w KQkq - 0 1,Stockfish 17.1,c2c4,22,60,927,13,16,22,100055,0.185,0
21,nqbbnrkr/pppppppp/8/8/8/8/PPPPPPPP/NQBBNRKR w KQkq - 0 1,Stockfish 17.1,h2h4,22,58,929,13,17,25,100087,0.173,0
22,nqbnrbkr/pppppppp/8/8/8/8/PPPPPPPP/NQBNRBKR w KQkq - 0 1,Stockfish 17.1,d2d4,35,91,901,8,17,20,100039,0.179,0
23,nqbnrkrb/pppppppp/8/8/8/8/PPPPPPPP/NQBNRKRB w KQkq - 0 1,Stockfish 17.1,f1g1,24,62,926,12,14,25,100028,0.196,0
24,nbqnbrkr/pppppppp/8/8/8/8/PPPPPPPP/NBQNBRKR w KQkq - 0 1,Stockfish 17.1,d2d4,76,299,699,2,16,22,100012,0.18,0
25,nqnbbrkr/pppppppp/8/8/8/8/PPPPPPPP/NQNBBRKR w KQkq - 0 1,Stockfish 17.1,d2d4,38,99,894,7,16,22,100052,0.193,1
```

Compact multiple analysis files:

```plaintext
; uv run compact.py x.csv y.csv > z.csv
```
