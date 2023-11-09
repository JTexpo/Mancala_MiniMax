from typing import List, Tuple

from copy import deepcopy


class Board:
    def __init__(self):
        self.tiles = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.top_score = 0
        self.bottom_score = 0
        self.held_marbles = 0


def move_piece(
    board: Board, row: int, column: int, return_full_history: bool = False
) -> Tuple[List[Board], bool, bool]:
    """A function to move the mancala piece.

    Args:
        board (Board): the mancala board
        row (int): the row that the piece was selected to be
        column (int): the column that the piece was selected to be
        return_full_history (bool, optional): instructions on wether
            or not to return just the final state, or all of the states prior.
            Defaults to False.

    Returns:
        Tuple[List[Board], bool]:
            board_history (List[Board]): all of the previous board states.
                NOTE will always be populated with at least a size of 1 given that the move is valid
            did_score (bool): an indicator on if the player scored on their last move or not
            game_over (bool): indicates of the game is over
    """
    board_history: List[Board] = []
    marbles: int = board.tiles[row][column]
    active_row: int = row
    active_column: int = column
    active_baord = deepcopy(board)
    player: str = "top" if row == 0 else "bottom"
    did_score: bool = False
    game_over: bool = False
    land_on_empty_marbles_won: int = 0

    # If there are no marbles, then there was no move
    if marbles == 0:
        return [], False, False

    active_baord.tiles[row][column] = 0

    # Making adding a copy of the board showing the marbles picked up
    if return_full_history:
        _board = deepcopy(active_baord)
        _board.held_marbles = marbles
        board_history.append(deepcopy(_board))

    # Itterating over the amount of marbles
    for marbles_left in range(marbles, 0, -1):
        # Resetting did score to false, incase it was set in prior move
        did_score = False

        # Moving the column for the marble to be dropped
        if active_row == 0:
            active_column -= 1
        elif active_row == 1:
            active_column += 1

        # if the column is outside of the range of the board, that means that the person may be eldgible for scoring
        if active_column < 0 or active_column > len(active_baord.tiles[0]) - 1:
            # Checking the top and bottom player to see if they scored
            if player == "top" and active_row == 0:
                active_baord.top_score += 1
                did_score = True
            elif player == "bottom" and active_row == 1:
                active_baord.bottom_score += 1
                did_score = True

            # Toggling the active row, and setting the active column approperately
            active_row = 1 if active_row == 0 else 0
            if did_score:
                active_column = len(active_baord.tiles[0]) if active_row == 0 else -1
            else:
                active_column = len(active_baord.tiles[0]) - 1 if active_row == 0 else 0

        # if the player did score, than that is the end of this marbles move and we can continue to the next
        if did_score:
            # deep copying the board state to show the history on the GUI
            if return_full_history:
                _board = deepcopy(active_baord)
                _board.held_marbles = marbles_left - 1
                board_history.append(deepcopy(_board))

            continue

        # if the player didnt score, then the next spot set gains 1 marble
        active_baord.tiles[active_row][active_column] += 1

        # deep copying the board state to show the history on the GUI
        if return_full_history:
            _board = deepcopy(active_baord)
            _board.held_marbles = marbles_left - 1
            board_history.append(deepcopy(_board))

    # ---------------
    # END OF FOR LOOP
    # ---------------

    # Checking if the last move was done on an empty tile.
    # if the move was done on an empty tile on the players side, the player can collect the enemies marbles
    if not did_score and active_baord.tiles[active_row][active_column] == 1:
        if (
            player == "top"
            and active_row == 0
            and active_baord.tiles[1][active_column] > 0
        ):
            land_on_empty_marbles_won = active_baord.tiles[1][active_column] + 1
            active_baord.tiles[0][active_column] = 0
            active_baord.tiles[1][active_column] = 0
            active_baord.top_score += land_on_empty_marbles_won

        elif (
            player == "bottom"
            and active_row == 1
            and active_baord.tiles[0][active_column] > 0
        ):
            land_on_empty_marbles_won = active_baord.tiles[0][active_column] + 1
            active_baord.tiles[0][active_column] = 0
            active_baord.tiles[1][active_column] = 0
            active_baord.bottom_score += land_on_empty_marbles_won

    # Checking to see if a player has no valid moves left. Which means the games over!
    if active_baord.tiles[0] == [0] * len(active_baord.tiles[0]) or active_baord.tiles[
        1
    ] == [0] * len(active_baord.tiles[1]):
        active_baord.top_score += sum(active_baord.tiles[0])
        active_baord.bottom_score += sum(active_baord.tiles[1])

        active_baord.tiles[0] = [0] * len(active_baord.tiles[0])
        active_baord.tiles[1] = [0] * len(active_baord.tiles[1])

        game_over = True

    # Appending the active board to the board history, index -1 will always be populated and contain the most up to date data
    board_history.append(deepcopy(active_baord))

    return board_history, did_score, game_over
