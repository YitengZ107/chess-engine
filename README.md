# Python Chess Engine

A chess engine built in Python using the `python-chess` library. The engine evaluates chess positions using custom heuristics and selects moves using alpha-beta search with several performance improvements.

The project includes a command-line interface for playing against the engine and basic Universal Chess Interface support for integration with compatible chess applications.

## Features

* Legal move generation using `python-chess`
* Custom board evaluation
* Alpha-beta pruning
* Move ordering
* Quiescence search
* Transposition table
* Human-versus-engine command-line game
* Basic Universal Chess Interface support
* Standard algebraic notation and UCI move input

## Board Evaluation

The engine evaluates positions from White's perspective:

* Positive score: White is better
* Negative score: Black is better
* Zero: Equal or drawn position

The evaluation function considers:

* Material balance
* Checkmate and draw conditions
* Piece centralization
* Pawn structure
* Passed pawns
* Doubled pawns
* Isolated pawns
* Bishop pair
* Rooks on open and semi-open files
* Piece mobility
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

The engine uses alpha-beta pruning to search possible move sequences.

Alpha-beta pruning produces the same result as standard minimax while avoiding branches that cannot affect the final decision.

Additional search improvements include:

### Move Ordering

Promising moves are searched first to improve alpha-beta pruning efficiency.

The engine prioritizes:

1. Promotions
2. Captures
3. Checks
4. Castling
5. Quiet moves

Captures are ordered using a basic Most Valuable Victim–Least Valuable Attacker approach.

### Quiescence Search

When the normal search reaches its depth limit, the engine continues examining tactical moves such as captures and promotions.

This helps reduce the horizon effect, where the engine stops searching in the middle of a tactical exchange.

### Transposition Table

Previously evaluated positions are stored in a transposition table.

This prevents the engine from repeatedly searching identical positions reached through different move orders.

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

Contains the board evaluation function and positional heuristics.

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

Implements basic Universal Chess Interface communication.

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
.venv\Scripts\Activate.ps1
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

The human player plays as White, and the engine plays as Black.

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

Type:

```text
quit
```

to end the game.

## Search Depth

The default search depth is configured in `main.py`:

```python
ENGINE_DEPTH = 4
```

A larger depth usually produces stronger moves but requires more computation time.

Because the engine is written in Python and uses a handcrafted evaluation function, it is not intended to compete with advanced engines such as Stockfish.

## UCI Support

Run the engine in UCI mode:

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

The engine responds with:

```text
bestmove <move>
```

Example:

```text
bestmove b8c6
```

## Example

```text
Chess Engine
You are playing as White.

Your move: e4
Engine plays: Nc6

Your move: Nf3
Engine plays: e5
```

The exact moves depend on the search depth and board evaluation.

## Technologies

* Python
* `python-chess`
* Minimax search
* Alpha-beta pruning
* Quiescence search
* Transposition tables
* Universal Chess Interface

## Current Limitations

* Search depth is limited by Python performance.
* Evaluation weights have not been extensively tuned.
* UCI time controls are not yet implemented.
* Searches run synchronously and do not currently support interruption.
* The engine does not use an opening book.
* The engine does not use endgame tablebases.
* The engine does not use a neural-network evaluation function.

## Possible Future Improvements

* Iterative deepening
* Time-managed searches
* Zobrist hashing
* Advanced transposition-table entries
* Killer-move heuristic
* History heuristic
* Improved piece-square tables
* Opening-book support
* Endgame tablebases
* Automated engine testing
* Graphical interface integration

## Author

Yiteng Zhang
