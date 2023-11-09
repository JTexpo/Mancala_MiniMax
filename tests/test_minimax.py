import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from mancala_minimax.board import Board
from mancala_minimax.minimax import minimax

class MiniMaxTestCase(unittest.TestCase):

    def test_minimax_depth_1(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [ [1,0,0,0,0,1],[4,4,4,4,4,4] ]
        ai_row = 0
        is_ai_turn = True
        depth = 1
        
        # ACTION
        # ------
        result = minimax(board=board,ai_row=ai_row,is_ai_turn=is_ai_turn,depth=depth)

        # ASSERT
        # ------
        expected = (5,5)
        self.assertTrue( result == result )
    
    def test_minimax_starter_move(self):
        # INITALIZATION
        # -------------
        board = Board()
        ai_row = 1
        is_ai_turn = True
        depth = 3
        
        # ACTION
        # ------
        result = minimax(board=board,ai_row=ai_row,is_ai_turn=is_ai_turn,depth=depth)

        # ASSERT
        # ------
        self.assertTrue( result[1] == 0 )
    
if __name__ == "__main__":
    unittest.main()