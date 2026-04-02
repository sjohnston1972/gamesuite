# Game Suite

A collection of 20 classic board games playable in the browser, each with AI opponents and optional LLM trash-talk via Ollama.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Ollama](https://img.shields.io/badge/Ollama-Optional-orange)

## Games

| Game | AI Engine | Style |
|------|-----------|-------|
| Draughts (Checkers) | Minimax + alpha-beta pruning | Warm wood textures |
| Chess | Minimax + piece-square tables | Marble & classical |
| Connect 4 | Minimax + alpha-beta pruning | Blue plastic, drop animation |
| Tic Tac Toe | Perfect minimax (unbeatable on Hard) | Chalk on blackboard |
| Othello (Reversi) | Minimax + corner/mobility strategy | Green felt casino |
| Go (9x9) | Monte Carlo Tree Search | Bamboo & zen |
| Backgammon | Heuristic evaluation | Leather & mahogany |
| Battleship | Probability density targeting | Naval military |
| Mancala | Minimax (depth 4-12) | Carved African wood |
| Mahjong Solitaire | Solitaire (LLM kibitzer) | Jade & Chinese |
| Snakes & Ladders | Dice game (LLM chat) | Colorful retro |
| Nim | Optimal XOR/nim-sum strategy | Matrix green, minimal |
| Ludo | Heuristic evaluation | Bright classic |
| Gomoku (Five in a Row) | Minimax + pattern scoring | Japanese ink wash |
| Dots & Boxes | Greedy + chain analysis | Notebook graph paper |
| Hangman | LLM picks words | Vintage carnival |
| Memory (Concentration) | Adaptive memory AI | Retro pixel art |
| Mastermind | Computer as code-maker | 70s retro plastic pegs |
| 2048 | Single-player puzzle | Clean modern minimal |
| Nine Men's Morris | Minimax + phase-aware eval | Carved stone medieval |

## Features

- **Three play modes** for each game: 1 Player (vs AI), vs LLM (AI moves + Ollama trash talk), 2 Player (hot-seat)
- **Three difficulty levels**: Easy, Medium, Hard — controlling AI search depth or strategy
- **LLM integration**: Connect to a local Ollama instance for a mouthy AI opponent that taunts you, reacts to the game state, and roasts you when you lose
- **Rich canvas graphics**: Each game has a unique visual theme with 3D pieces, animations, and procedural textures
- **Web Audio API**: Synthesised sound effects for moves, captures, wins — no external audio files
- **Zero dependencies on the frontend**: Pure HTML/CSS/JavaScript, no build step, no npm
- **Responsive layout**: Sidebar (settings) | Board (center) | Chat (right)

## Quick Start

### Requirements

- Python 3.10+
- Flask (`pip install flask`)
- Ollama running on your network (optional — games work without it, LLM chat mode requires it)

### Run

```bash
pip install flask requests
python app.py
```

Open http://localhost:5000

### Ollama Setup

By default the app expects Ollama at `http://192.168.1.250:11434`. To change this, edit `OLLAMA_URL` in `app.py`.

Any Ollama model works. Tested with:
- `qwen2.5-coder:14b` (recommended)
- `qwen2.5:7b`
- `mistral:7b`

The LLM is used for **chat/trash-talk only** — game moves are handled by the built-in AI engines (minimax, MCTS, etc.), so the LLM model choice doesn't affect gameplay difficulty.

## Project Structure

```
.
├── app.py              # Flask server + Ollama API proxy
├── index.html          # Front page with game tiles
├── draughts.html       # Draughts (Checkers)
├── chess.html          # Chess
├── connect4.html       # Connect 4
├── tictactoe.html      # Tic Tac Toe
├── othello.html        # Othello (Reversi)
├── go.html             # Go (9x9)
├── backgammon.html     # Backgammon
├── battleship.html     # Battleship
├── mancala.html        # Mancala
├── mahjong.html        # Mahjong Solitaire
├── snakes.html         # Snakes & Ladders
├── nim.html            # Nim
├── ludo.html           # Ludo
├── gomoku.html         # Gomoku (Five in a Row)
├── dots.html           # Dots & Boxes
├── hangman.html        # Hangman
├── memory.html         # Memory (Concentration)
├── mastermind.html     # Mastermind
├── 2048.html           # 2048
├── morris.html         # Nine Men's Morris
└── requirements.txt    # Python dependencies
```

## License

MIT
