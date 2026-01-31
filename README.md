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
usage: eval.py [-h] --stockfish PATH [--threads N] [--hash N] [--depth N]
               [--id N | --range M-N]

Analyze Chess960 starting positions with Stockfish.

options:
  -h, --help        show this help message and exit
  --id N            analyze position N; can be provided multiple times
  --range M-N       analyze positions M through N inclusive

engine settings:
  --stockfish PATH  path to the Stockfish executable
  --threads N       set number of threads to use (default: 1)
  --hash N          set hash size in MB (default: 1024)
  --depth N         set a depth limit (default: 20)

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
; uv run eval.py --stockfish $(which stockfish) --range 20-25 --depth 20
id,fen,engine,bestmove,eval,wins,draws,losses,depth,seldepth,nodes,time,hashfull
20,nbbqnrkr/pppppppp/8/8/8/8/PPPPPPPP/NBBQNRKR w KQkq - 0 1,Stockfish 17.1,c4,0.26,67,922,11,20,29,322512,0.568,0
21,nqbbnrkr/pppppppp/8/8/8/8/PPPPPPPP/NQBBNRKR w KQkq - 0 1,Stockfish 17.1,c4,0.27,70,919,11,20,26,904568,1.65,4
22,nqbnrbkr/pppppppp/8/8/8/8/PPPPPPPP/NQBNRBKR w KQkq - 0 1,Stockfish 17.1,d4,0.38,100,893,7,20,32,399411,0.689,2
23,nqbnrkrb/pppppppp/8/8/8/8/PPPPPPPP/NQBNRKRB w KQkq - 0 1,Stockfish 17.1,O-O,0.16,47,937,16,20,25,319385,0.541,0
24,nbqnbrkr/pppppppp/8/8/8/8/PPPPPPPP/NBQNBRKR w KQkq - 0 1,Stockfish 17.1,d4,0.63,212,785,3,20,35,898726,1.649,5
25,nqnbbrkr/pppppppp/8/8/8/8/PPPPPPPP/NQNBBRKR w KQkq - 0 1,Stockfish 17.1,h4,0.39,103,890,7,20,30,632762,1.163,4
```

Compact multiple analysis files:

```plaintext
; uv run compact.py x.csv y.csv > z.csv
```
