import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from mancala_minimax.board import Board, move_piece

class BoardTestCase(unittest.TestCase):

    def test_move_piece_invalid_move(self):
        # INITALIZATION
        # -------------
        board = Board()
        row = 0
        column = 0
        return_full_history = False
        board.tiles[row][column] = 0
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        expected = ([],False,False)
        self.assertTrue( result == expected )
    
    def test_move_piece_valid_move_1(self):
        # INITALIZATION
        # -------------
        board = Board()
        row = 0
        column = 1
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[5,0,4,4,4,4],[5,5,4,4,4,4]] )
        self.assertTrue( result[0][-1].top_score == 1 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == False )
    
    def test_move_piece_valid_move_2(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[0,1,4,4,4,4],[4,4,4,4,4,4]]
        row = 0
        column = 1
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[0,0,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][-1].top_score == 5 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == False )
    
    def test_move_piece_valid_move_3(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[0,1,4,4,4,4],[0,4,4,4,4,4]]
        row = 0
        column = 1
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[1,0,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][-1].top_score == 0 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == False )
    
    def test_move_piece_valid_move_4(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[0,2,4,4,4,4],[0,4,4,4,4,4]]
        row = 0
        column = 1
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[1,0,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][-1].top_score == 1 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == True )
    
    def test_move_piece_valid_move_5(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[1,2,4,4,4,4],[0,4,4,4,4,4]]
        row = 0
        column = 0
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[0,2,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][-1].top_score == 1 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == True )
    
    def test_move_piece_valid_large_1(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[0,0,0,0,0,12],[0,0,0,0,0,0]]
        row = 0
        column = 5
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[1,1,1,1,1,0],[1,1,1,1,1,1]] )
        self.assertTrue( result[0][-1].top_score == 1 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == False )
    
    def test_move_piece_valid_large_2(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[0,0,0,0,0,13],[0,0,0,0,0,0]]
        row = 0
        column = 5
        return_full_history = False
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][-1].tiles == [[1,1,1,1,1,0],[1,1,1,1,1,0]] )
        self.assertTrue( result[0][-1].top_score == 3 )
        self.assertTrue( result[0][-1].bottom_score == 0 )
        self.assertTrue( result[1] == False )
    
    def test_move_piece_history(self):
        # INITALIZATION
        # -------------
        board = Board()
        board.tiles = [[0,2,4,4,4,4],[0,4,4,4,4,4]]
        row = 0
        column = 1
        return_full_history = True
        
        # ACTION
        # ------
        result = move_piece(board=board,row=row,column=column,return_full_history=return_full_history)

        # ASSERT
        # ------
        self.assertTrue( result[0][0].tiles == [[0,0,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][0].top_score == 0 )
        self.assertTrue( result[0][0].bottom_score == 0 )
        self.assertTrue( result[0][0].held_marbles == 2 )
    
        self.assertTrue( result[0][1].tiles == [[1,0,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][1].top_score == 0 )
        self.assertTrue( result[0][1].bottom_score == 0 )
        self.assertTrue( result[0][1].held_marbles == 1 )

        self.assertTrue( result[0][2].tiles == [[1,0,4,4,4,4],[0,4,4,4,4,4]] )
        self.assertTrue( result[0][2].top_score == 1 )
        self.assertTrue( result[0][2].bottom_score == 0 )
        self.assertTrue( result[0][2].held_marbles == 0 )

        self.assertTrue( result[1] == True )

if __name__ == "__main__":
    unittest.main()