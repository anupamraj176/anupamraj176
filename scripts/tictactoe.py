import sys
import json
import random
import os

STATE_FILE = "assets/ttt_state.json"
README_FILE = "README.md"
REPO = "anupamraj176/anupamraj176"

def check_winner(board):
    wins = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
        [0, 4, 8], [2, 4, 6]             # diagonals
    ]
    for w in wins:
        if board[w[0]] != " " and board[w[0]] == board[w[1]] == board[w[2]]:
            return board[w[0]]
    if " " not in board:
        return "Draw"
    return None

def main():
    issue_title = sys.argv[1] if len(sys.argv) > 1 else ""
    if not issue_title.startswith("ttt|"):
        print("Not a tic-tac-toe move.")
        return

    with open(STATE_FILE, "r") as f:
        state = json.load(f)

    board = state["board"]
    winner = state["winner"]

    if issue_title == "ttt|new":
        board = [" "] * 9
        winner = None
    else:
        try:
            move = int(issue_title.split("|")[1])
        except:
            print("Invalid move index.")
            return

        if winner or board[move] != " ":
            print("Game over or invalid move.")
            return
        
        # Player makes a move
        board[move] = "X"
        winner = check_winner(board)
        
        # AI makes a move
        if not winner:
            empty_cells = [i for i, cell in enumerate(board) if cell == " "]
            if empty_cells:
                ai_move = random.choice(empty_cells)
                board[ai_move] = "O"
                winner = check_winner(board)

    state["board"] = board
    state["winner"] = winner

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    # Generate README HTML
    html = "<table>\n"
    for row in range(3):
        html += "  <tr>\n"
        for col in range(3):
            idx = row * 3 + col
            val = board[idx]
            if val == " " and not winner:
                link = f"https://github.com/{REPO}/issues/new?title=ttt%7C{idx}&body=Just+push+%27Submit+new+issue%27+without+changing+the+title."
                html += f"    <td width='50' height='50' align='center'><a href='{link}'>⬜</a></td>\n"
            else:
                display = "❌" if val == "X" else "⭕" if val == "O" else "⬜"
                html += f"    <td width='50' height='50' align='center'>{display}</td>\n"
        html += "  </tr>\n"
    html += "</table>\n"

    if winner:
        if winner == "Draw":
            html += "<p>It's a draw!</p>\n"
        else:
            display = "❌" if winner == "X" else "⭕"
            html += f"<p>{display} wins!</p>\n"
        reset_link = f"https://github.com/{REPO}/issues/new?title=ttt%7Cnew&body=Just+push+%27Submit+new+issue%27."
        html += f"<p><a href='{reset_link}'>Play again</a></p>\n"

    # Replace in README
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- tictactoe_start -->"
    end_marker = "<!-- tictactoe_end -->"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx + len(start_marker)] + "\n<div align=\"center\">\n" + html + "</div>\n" + content[end_idx:]
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    main()
