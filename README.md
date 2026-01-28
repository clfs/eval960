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
  --threads N       set custom number of threads to use
  --nodes N         set soft node limit for analysis (default: 100000)
  --hash N          set custom hash size in MB

If neither --id nor --range is provided, all 960 positions are analyzed.
```

Example:

```plaintext
; uv run eval.py --stockfish $(which stockfish) --id 742
id,fen,engine,depth,seldepth,multipv,score,mate,wins,draws,losses,nodes,time,hashfull,pv
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,1,2,1,12,,43,939,18,20,0.001,0,e2e4
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,2,3,1,35,,89,903,8,45,0.001,0,e2e4
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,3,4,1,52,,151,844,5,74,0.001,0,e2e4
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,4,6,1,72,,269,729,2,398,0.001,0,g2g4
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,5,7,1,62,,203,794,3,801,0.002,0,d2d4 d7d5 f2f3 a7a5 e2e4
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,6,8,1,49,,142,853,5,1313,0.002,0,d2d4 f7f5 a2a4 a7a5
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,7,11,1,49,,140,855,5,2330,0.004,0,e2e4 f7f6 a2a4 e7e5 f2f4 a7a5
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,8,10,1,45,,124,870,6,3664,0.006,0,e2e4 e7e5 f2f4 f7f6 d2d4 e5d4
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,9,12,1,47,,130,865,5,3773,0.006,0,e2e4 e7e5 f2f4 f7f6 d2d4 e5d4 g1d4 d8e6 d4f2 a7a5 d1c3
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,10,15,1,38,,100,893,7,11331,0.019,3,e2e4 e7e5 d1c3 a7a5 f2f4 e5f4 a2a4 f7f5 e4f5 d8c6 g2g4 f4g3
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,11,16,1,29,,73,917,10,20974,0.038,7,e2e4 e7e5 f2f4 e5f4 a2a4 a7a5 g2g3 f4g3 h2g3 g7g6
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,12,15,1,27,,71,918,11,21237,0.038,7,e2e4 e7e5 f2f4 e5f4 a2a4 a7a5 g2g3 f4g3 h2g3 g7g6 d2d4 f7f5 e4f5 g6f5
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,13,18,1,26,,68,921,11,27723,0.051,9,e2e4 e7e5 f2f4 e5f4 b2b3 d8e6 g2g3 b7b6 g3f4 c8b7 d1c3 f8c5
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,14,20,1,25,,65,923,12,36186,0.068,12,e2e4 e7e5 f2f4 e5f4 a2a4 a7a5 d2d4 g7g5 g2g3 f7f5 e4f5 f4g3 g1g3
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,15,23,1,35,,89,903,8,59767,0.114,22,d2d4 d7d5 f2f3 a7a5 e2e4 f7f6 a2a4 e7e5 d4e5 d5e4 f3e4 f6e5 f1b5 e8d6 d1c3
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,16,21,1,36,,94,898,8,76472,0.141,28,d2d4 d7d5 d1c3 f7f6 e2e4 d5e4 c3e4 d8c6
742,rkbnnbqr/pppppppp/8/8/8/8/PPPPPPPP/RKBNNBQR w KQkq - 0 1,Stockfish 17.1,17,17,1,35,,90,902,8,100070,0.19,39,d2d4 d7d5
```
