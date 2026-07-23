# Python Chess Engine

A chess engine built from scratch in Python using the `python-chess` library. The engine uses a custom heuristic evaluation function and alpha-beta search to select moves.

The project includes:

* A command-line human-versus-engine game
* Universal Chess Interface support
* Integration with Lichess through `lichess-bot`

## Features

* Custom board evaluation
* Minimax search with alpha-beta pruning
* Move ordering
* Quiescence search
* Transposition table
* Human-versus-engine command-line interface
* Choice to play as White, Black, or a randomly selected color
* Standard algebraic notation and UCI move input
* Universal Chess Interface support
* Online play through a Lichess bot account

## Board Evaluation

The engine evaluates positions from White's perspective:

* Positive score: White is better
* Negative score: Black is better
* Zero: Equal or drawn position

The evaluation function considers:

* Material balance
* Checkmate and draw conditions
* Piece centralization
* Piece mobility
* Pawn structure
* Passed pawns
* Doubled pawns
* Isolated pawns
* Bishop pair
* Rooks on open and semi-open files
* King safety

Piece values are measured in centipawns:

| Piece  | Value |
| ------ | ----: |
| Pawn   |   100 |
| Knight |   320 |
| Bishop |   330 |
| Rook   |   500 |
| Queen  |   900 |

## Search Algorithm

The engine uses alpha-beta pruning, an optimization of minimax search that avoids exploring branches that cannot affect the final decision.

### Move Ordering

Promising moves are searched first to improve alpha-beta pruning efficiency.

The engine prioritizes:

1. Promotions
2. Captures
3. Checks
4. Castling
5. Quiet moves

Captures are ordered using a basic Most Valuable Victim–Least Valuable Attacker strategy.

### Quiescence Search

When the normal depth limit is reached, the engine continues searching tactical positions involving captures and promotions.

This reduces the horizon effect, where the engine would otherwise stop searching in the middle of a tactical exchange.

### Transposition Table

The engine stores previously evaluated positions in a transposition table.

This prevents repeated searches of identical board positions reached through different move orders.

## Project Structure

```text
chess-engine/
├── board_eval.py
├── main.py
├── search.py
├── uci.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `board_eval.py`

Contains the custom board evaluation function and positional heuristics.

### `search.py`

Contains:

* Alpha-beta pruning
* Move ordering
* Quiescence search
* Transposition table
* Best-move selection

### `main.py`

Runs the command-line human-versus-engine game.

### `uci.py`

Implements the Universal Chess Interface commands used by chess applications and the Lichess bridge.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/chess-engine.git
cd chess-engine
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
chess
```

## Playing Against the Engine

Run:

```bash
python main.py
```

At the beginning of the game, choose whether to play as:

1. White
2. Black
3. A randomly assigned color

Moves can be entered using standard algebraic notation:

```text
e4
Nf3
Bxc6
O-O
```

Moves can also be entered using UCI coordinate notation:

```text
e2e4
g1f3
f1c4
e1g1
```

Type `quit` to stop the game.

## Search Depth

The default search depth is configured in `main.py`:

```python
ENGINE_DEPTH = 4
```

Higher depths generally produce stronger moves but require more computation time.

Because the engine is written in Python and uses a handcrafted evaluation function, it is not intended to compete with advanced engines such as Stockfish.

## UCI Support

Run the engine directly in UCI mode:

```bash
python uci.py
```

Supported commands include:

```text
uci
isready
ucinewgame
position startpos
position startpos moves e2e4 e7e5
position fen <FEN>
go depth <depth>
quit
```

Example session:

```text
uci
isready
position startpos moves e2e4 e7e5 g1f3
go depth 4
```

The engine responds with a move such as:

```text
bestmove b8c6
```

## Lichess Integration

The engine can play online through a Lichess bot account using the external `lichess-bot` bridge.

The communication flow is:

```text
Lichess
   ↓
lichess-bot
   ↓ UCI commands
uci.py
   ↓
search.py
```

To run the bot:

1. Create a dedicated Lichess account and convert it into a bot account.
2. Clone the official `lichess-bot` repository separately.
3. Configure its `config.yml` to point to this engine's `uci.py`.
4. Start the bridge program.

Example Windows command from the separate `lichess-bot` directory:

```powershell
.\venv\Scripts\python.exe lichess-bot.py
```

The computer, internet connection, and bot process must remain active for the bot to stay online.

For safety, the private Lichess API token and `config.yml` should never be uploaded to this repository.

## Technologies and Concepts

* Python
* `python-chess`
* Minimax search
* Alpha-beta pruning
* Move ordering
* Quiescence search
* Transposition tables
* Universal Chess Interface
* Lichess Bot API integration

## Current Limitations

* Search performance is limited by Python execution speed.
* Evaluation weights have not been extensively tuned.
* Search uses a fixed depth instead of time management.
* UCI searches run synchronously and cannot currently be interrupted.
* The engine does not use an opening book.
* The engine does not use endgame tablebases.
* The engine does not use a neural-network evaluation function.

## Possible Future Improvements

* Iterative deepening
* Clock-based time management
* Zobrist hashing
* More advanced transposition-table entries
* Killer-move heuristic
* History heuristic
* Improved piece-square tables
* Opening-book support
* Endgame tablebases
* Automated engine testing
* Performance benchmarking

## Author

Yiteng Zhang

