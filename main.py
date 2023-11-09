import pyscript
from pyscript import Element
from typing import List

from mancala_minimax.board import Board, move_piece
from mancala_minimax.minimax import minimax

from copy import deepcopy
import time
import asyncio

board: Board = Board()
board_history: List[Board] = [Board()]
is_ai_turn: bool = False
lock_actions: bool = True

top_0_element = Element("top_0")
top_1_element = Element("top_1")
top_2_element = Element("top_2")
top_3_element = Element("top_3")
top_4_element = Element("top_4")
top_5_element = Element("top_5")

bottom_0_element = Element("bottom_0")
bottom_1_element = Element("bottom_1")
bottom_2_element = Element("bottom_2")
bottom_3_element = Element("bottom_3")
bottom_4_element = Element("bottom_4")
bottom_5_element = Element("bottom_5")

held_marbles_element = Element("held_marbles")
turn_element = Element("turn")

player_score_element = Element("player_score")
ai_score_element = Element("ai_score")


async def sync_board_to_gui(board: Board, turn: str):
    top_0_element.element.innerHTML = board.tiles[0][0]
    top_1_element.element.innerHTML = board.tiles[0][1]
    top_2_element.element.innerHTML = board.tiles[0][2]
    top_3_element.element.innerHTML = board.tiles[0][3]
    top_4_element.element.innerHTML = board.tiles[0][4]
    top_5_element.element.innerHTML = board.tiles[0][5]

    bottom_0_element.element.innerHTML = board.tiles[1][0]
    bottom_1_element.element.innerHTML = board.tiles[1][1]
    bottom_2_element.element.innerHTML = board.tiles[1][2]
    bottom_3_element.element.innerHTML = board.tiles[1][3]
    bottom_4_element.element.innerHTML = board.tiles[1][4]
    bottom_5_element.element.innerHTML = board.tiles[1][5]

    held_marbles_element.element.innerHTML = f"Held Marbles: {board.held_marbles}"
    turn_element.element.innerHTML = f"Turn: {turn}"

    player_score_element.element.innerHTML = board.bottom_score
    ai_score_element.element.innerHTML = board.top_score


def player_move(column: int):
    global board, board_history, lock_actions, is_ai_turn

    # Conditions where the player can't move
    if lock_actions or is_ai_turn:
        return

    # acting on the players move
    moved_board_history, did_score, game_over = move_piece(
        board=board, row=1, column=column, return_full_history=True
    )

    # if the player chose an invalid move then the player can choose again
    if not moved_board_history:
        return

    # saving all of the boards + history to allow for the GUI to update
    board = deepcopy(moved_board_history[-1])
    board_history = deepcopy(moved_board_history)
    lock_actions = True

    # if the player didn't score, its now the ais turn
    if not did_score and not game_over:
        is_ai_turn = True

def reset():
    global board, board_history, is_ai_turn, lock_actions
    board = Board()
    board_history = [Board()]
    is_ai_turn = False
    lock_actions = True

async def main():
    global board, board_history, lock_actions, is_ai_turn
    while True:

        # if there is moves in the boards history, then we update the GUI
        if board_history:

            # Updating the board ever .3 seconds
            for board_state in board_history:
                await sync_board_to_gui(board_state, "AI" if is_ai_turn else "You")
                await asyncio.sleep(0.3)
            
            # Clearing out the board history and un-locking all actions
            board_history = []
            lock_actions = False

        # AI's turn
        if not lock_actions and is_ai_turn:

            # Finding the best move for the AI
            best_score, best_move, move_compare = minimax(
                board=board, ai_row=0, is_ai_turn=True, depth=5
            )

            # Acting on the AI's predicted best move
            moved_board_history, did_score, game_over = move_piece(
                board=board, row=0, column=best_move, return_full_history=True
            )

            if moved_board_history:
                # saving all of the boards + history to allow for the GUI to update
                board = deepcopy(moved_board_history[-1])
                board_history = deepcopy(moved_board_history)
                lock_actions = True

            # Giving the turn back to the player
            if not did_score:
                is_ai_turn = False

        await asyncio.sleep(0.5)


pyscript.run_until_complete(main())
