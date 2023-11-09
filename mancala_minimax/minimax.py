from typing import List, Tuple

from mancala_minimax.board import Board, move_piece


def minimax(
    board: Board, ai_row: int, is_ai_turn: bool, depth: int
) -> Tuple[float, int, dict]:
    """A function to preform the mini max algorithm for the board game Mancala

    Args:
        board (Board): the play-able game board
        ai_row (int): which row the AI is on
        is_ai_turn (bool): if it is the AI's turn to act
        depth (int): how much further ahead to mini max

    Returns:
        Tuple[float, int, dict]: 
            best_score (float): What the best posible score is for the AI 
            best_move (int): Which column relates to the best move
            move_compare: A dictionary of all of the moves and their scores 
    """
    # placing above init, due to some logic gates used when assigining varibles
    if depth <= 0:
        if ai_row == 0:
            return board.top_score - board.bottom_score, -1, {}
        elif ai_row == 1:
            return board.bottom_score - board.top_score, -1, {}

    # init
    valid_moves: List[int] = []
    best_move: int = -1
    best_score: float = 0
    points: int = 0
    player_row: int = 1 if ai_row == 0 else 0
    move_compare: dict = {}

    # -------
    # AI TURN
    # -------
    if is_ai_turn:
        # Looking to maximize the AI's score
        best_score = float("-inf")

        # grabbing all valid moves for the ai
        valid_moves = [
            index for index, value in enumerate(board.tiles[ai_row]) if value > 0
        ]

        # itterating over all of the moves to find the best one
        for move in valid_moves:

            # acting on the move and judging the outcome
            board_history, go_again, game_over = move_piece(
                board=board, row=ai_row, column=move, return_full_history=False
            )

            # if the move allows for a follow-up move, then we don't lower the depth and consider that extra move to be of the same move
            # this is to keep the minimax optimized, as you may have a 3 move combo that leaves you in a very bad position
            if go_again and not game_over:
                points, _, _ = minimax(
                    board=board_history[-1], ai_row=ai_row, is_ai_turn=True, depth=depth
                )

            # if the game is not over, then we want to see what the response is from the players move
            elif not game_over:
                points, _, _ = minimax(
                    board=board_history[-1],
                    ai_row=ai_row,
                    is_ai_turn=False,
                    depth=depth - 1,
                )

            # If the game is over, we calculate the final score
            elif game_over and (ai_row == 0):
                points = board_history[-1].top_score - board_history[-1].bottom_score
            elif game_over and (ai_row == 1):
                points = board_history[-1].bottom_score - board_history[-1].top_score

            # Adding the move to the compare, for ranking
            move_compare[move] = [points]

            # if the move nets a better score, then that is our new best move / score
            if points > best_score:
                best_score = points
                best_move = move
    # -----------
    # Player TURN
    # -----------
    else:
        # Looking to minimize the Player's score
        best_score = float("inf")

        # grabbing all valid moves for the player
        valid_moves = [
            index for index, value in enumerate(board.tiles[player_row]) if value > 0
        ]

        # itterating over all of the moves to find the best one
        for move in valid_moves:

            # acting on the move and judging the outcome
            board_history, go_again, game_over = move_piece(
                board=board, row=player_row, column=move, return_full_history=False
            )

            # if the move allows for a follow-up move, then we don't lower the depth and consider that extra move to be of the same move
            # this is to keep the minimax optimized, as you may have a 3 move combo that leaves you in a very bad position
            if go_again and not game_over:
                points, _, _ = minimax(
                    board=board_history[-1],
                    ai_row=ai_row,
                    is_ai_turn=False,
                    depth=depth,
                )
            # if the game is not over, then we want to see what the response is from the players move
            elif not game_over:
                points, _, _ = minimax(
                    board=board_history[-1],
                    ai_row=ai_row,
                    is_ai_turn=True,
                    depth=depth - 1,
                )

            # If the game is over, calculate the final score
            elif game_over and (ai_row == 0):
                points = board_history[-1].top_score - board_history[-1].bottom_score
            elif game_over and (ai_row == 1):
                points = board_history[-1].bottom_score - board_history[-1].top_score

            # Adding the move to the compare, for ranking
            move_compare[move] = [points]

            # if the move nets a wrose score for the AI, then that is our new best move to beat the mini-max
            if points < best_score:
                best_score = points
                best_move = move

    return best_score, best_move, move_compare
