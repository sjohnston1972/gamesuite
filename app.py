from flask import Flask, send_from_directory, request, jsonify
import requests
import os
import re

app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)))

OLLAMA_URL = "http://192.168.1.250:11434"

# ── Static routes ──

GAMES = [
    "draughts", "chess", "connect4", "tictactoe", "othello",
    "go", "backgammon", "battleship", "mancala", "mahjong",
    "snakes", "ludo", "nim", "gomoku", "dots", "hangman",
    "memory", "mastermind", "2048", "morris",
]


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<game>.html")
def serve_game(game):
    if game in GAMES:
        return send_from_directory(app.static_folder, f"{game}.html")
    return "Not found", 404


# ── Ollama API ──

@app.route("/api/models")
def list_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        data = r.json()
        names = [m["name"] for m in data.get("models", [])]
        return jsonify({"models": names})
    except Exception as e:
        return jsonify({"error": str(e), "models": []}), 500


@app.route("/api/move", methods=["POST"])
def get_move():
    body = request.json
    board_str = body.get("board", "")
    legal_moves = body.get("legalMoves", [])
    model = body.get("model", "qwen2.5-coder:14b")
    turn_label = body.get("turn", "Red")

    moves_list = "\n".join(f"  {i+1}. {m}" for i, m in enumerate(legal_moves))

    prompt = f"""You are playing a board game as {turn_label}. Here is the board state:

{board_str}

Your legal moves (numbered):
{moves_list}

Pick the BEST move. Reply with ONLY the move number. Just a single integer, nothing else."""

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 10},
            },
            timeout=60,
        )
        result = r.json()
        response_text = result.get("response", "").strip()
        match = re.search(r"\d+", response_text)
        if match:
            move_idx = int(match.group()) - 1
            if 0 <= move_idx < len(legal_moves):
                return jsonify({"moveIndex": move_idx, "raw": response_text})
        return jsonify({"moveIndex": 0, "raw": response_text, "fallback": True})
    except Exception as e:
        return jsonify({"error": str(e), "moveIndex": 0}), 500


# ── Chat ──

chat_histories = {}


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.json
    message = body.get("message", "")
    model = body.get("model", "qwen2.5-coder:14b")
    board_str = body.get("board", "")
    session_id = body.get("sessionId", "default")
    game_status = body.get("gameStatus", "")
    game_name = body.get("gameName", "board game")

    if session_id not in chat_histories:
        chat_histories[session_id] = []

    history = chat_histories[session_id]
    history.append({"role": "user", "content": message})

    if len(history) > 20:
        history[:] = history[-20:]

    system_prompt = (
        f"You are a loud-mouthed {game_name} opponent who NEVER shuts up. "
        "You ALWAYS initiate trash talk — mock their moves, question their intelligence, "
        "brag about your own strategy, make bold predictions about crushing them. "
        "You're like a rowdy opponent at a pub who's had a few pints. "
        "Throw in creative insults, sarcasm, and backhanded compliments. "
        "If they trash talk you, fire back HARDER — never let them have the last word. "
        "Keep responses SHORT — 1-2 punchy sentences max. No essays. "
        "Never use emojis. "
        "\n\n"
        "=== CURRENT GAME STATE (read this carefully!) ===\n"
        f"{game_status}\n"
        "=== HOW TO REACT ===\n"
        "- If you are winning: be smug, mock them.\n"
        "- If you are losing: be defensive, make excuses, blame luck, threaten a comeback.\n"
        "- If the game is over and you LOST: be dramatically salty, demand a rematch.\n"
        "- If the game is over and you WON: gloat mercilessly.\n"
        f"\nBoard:\n{board_str}"
    )

    messages = [{"role": "system", "content": system_prompt}] + history

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.8, "num_predict": 80},
            },
            timeout=30,
        )
        result = r.json()
        reply = result.get("message", {}).get("content", "...").strip()
        history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "*stares silently at the board*", "error": str(e)})


@app.route("/api/chat/clear", methods=["POST"])
def clear_chat():
    body = request.json or {}
    session_id = body.get("sessionId", "default")
    chat_histories.pop(session_id, None)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
