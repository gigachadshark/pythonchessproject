from turtle import left
from const import *
from sqaure import Square
from piece import *
from move import Move
import copy

class Board:
    
    def __init__(self):
        self.squares= [[0,0,0,0,0,0,0,0] for col in range(COLS)] #a list of 8 zeros for each col 
        self.last_move = None 
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self,piece,move):
        initial = move.initial
        final = move.final 

        #console board move update 
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #pawn promotion 
        if isinstance(piece, Pawn ):
            self.check_promotion(piece, final)

        #king castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook   #check if queen side or king side castling 
                self.move(rook, rook.moves[-1])

        #move
        piece.moved = True

        #clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move 

    def valid_move(self,piece,move):
        return move in piece.moves

    def check_promotion(self,piece, final):
        if final.row == 0 or final.row ==7: #when pawn is ready to be promoted
            self.squares[final.row][final.col].piece = Queen(piece.colour)
    
    def castling(self,initial, final):
        return abs(initial.col - final.col) == 2
        #kings moves 2 sqaures so is castling no other way for king move 2 squares
    
    def in_check(self,piece,move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self) #making copy of all properties of the board 
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.colour):#checking if any white piece has final move with king
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row , col, bool= False) #calculating valid moves for enemy piece
                    for m in p.moves:     #looping each move
                        if isinstance(m.final.piece,King):   #checking if final sqaure has a piece which is king
                            return True
        
        return False


    def calc_moves(self,piece,row,col, bool =True ):
        #this is going to calculate all the possible valid moves of a specific piece on a specific position 
        
        def pawn_moves():
            #steps
            if piece.moved:
                steps= 1 #this is because when a pawn has made as move it can only move one step 
            else:
                steps= 2 # if the pawn hasnt moved then it can moved 2 steps 
            
            #vertical moves 
            start = row + piece.dir
            end = row + (piece.dir * (1+ steps))
            for possible_move_row in range(start,end,piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create intial and final move squares
                        initial = Square(row,col)
                        final = Square(possible_move_row,col)
                        #create a new move
                        move = Move(initial,final)

                        #check possible checks 
                        if bool:
                            if not self.in_check(piece, move):
                                #add new move
                                piece.add_move(move)
                        else:
                            #add new move
                            piece.add_move(move)
                    else:
                        break # this means pawn is blocked 
                else:
                    break # not in range 


            #diagonal moves for when pawn takes opponent piece
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1 , col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                        #create intial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        #create a new move
                        move = Move(initial,final)

                        #check possible checks 
                        if bool:
                            if not self.in_check(piece, move):
                                #add new move
                                piece.add_move(move)
                        else:
                            #add new move
                            piece.add_move(move)
                
        def knight_moves():
            # 8 possible moves 
            possible_moves= [
                (row-2, col +1),
                (row - 1 , col +2),
                (row + 1, col + 2),
                (row +2 , col + 1),
                (row+2 , col -1),
                (row+1, col-2),
                (row-1,col -2),
                (row -2, col -1),
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.colour):
                        # create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square (possible_move_row, possible_move_col, final_piece)
                        #create new move
                        move = Move(initial, final)

                        #check possible checks 
                        if bool:
                            if not self.in_check(piece, move):
                                #add new move
                                piece.add_move(move)
                            else:
                                break  #break the loop the prevent king from check 
                        else:
                            #add new move
                            piece.add_move(move)

        def straightline_moves(incrs): #increments

            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True: 
                    if Square.in_range(possible_move_col, possible_move_row):
                        #create sqaures of the possible new move
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row,possible_move_col, final_piece)
                        #create a possible new move
                        move= Move(initial,final)

                        #empty = continue looping 
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #check possible checks 
                            if bool:
                                if not self.in_check(piece, move):
                                    #add new move
                                    piece.add_move(move)
                            else:
                                #add new move
                                piece.add_move(move)

                        #has enemy piece = add move and then break
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.colour):
                            #check possible checks 
                            if bool:
                                if not self.in_check(piece, move):
                                    #add new move
                                    piece.add_move(move)
                            else:
                                #add new move
                                piece.add_move(move)
                            break

                        #has team piece  = break 
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.colour):
                            break
                    
                    #not in range
                    else: break

                    #incremeting incrs (the increments)   
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col +0), # up
                (row-1,col+1), # up right
                (row+0,col+1), # right
                (row+1,col+1), # down right
                (row+1, col+0), #down
                (row+1, col -1), # down left
                (row+0,col-1), # left
                (row-1, col-1) # up left
            ]

            #normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.colour): 
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square (possible_move_row, possible_move_col)
                        #create new move
                        move = Move(initial, final)
                        #check possible checks 
                        if bool:
                            if not self.in_check(piece, move):
                                #add new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            #add new move
                            piece.add_move(move)

            #castling moves 
            if not piece.moved:
                #queen castling 
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece(): #castling not possible as there are pieces in between 
                                break

                            if c == 3:
                                piece.left_rook == left_rook #adds left rook to king

                                initial = Square(row, 0) #rook move
                                final = Square(row,3)
                                moveR = Move(initial , final)

                                initial = Square(row, col) #king move
                                final = Square(row,2)
                                moveK = Move(initial , final)

                                #check possible checks 
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR): #if moving both piece not in check 
                                        #add new move to rook
                                        left_rook.add_move(moveR)
                                        #add new move to king
                                        piece.add_move(moveK)
                                else:
                                    #add new move to rook
                                    left_rook.add_move(moveR)
                                    #add new move King
                                    piece.add_move(moveK)


                #king castling 
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                        if not right_rook.moved: 
                            for c in range(5,7):
                                if self.squares[row][c].has_piece(): #castling not possible as there are pieces in between 
                                    break

                                if c == 6 :
                                    piece.right_rook == right_rook #adds right rook to king

                                    initial = Square(row, 7) #rook move
                                    final = Square(row,5)
                                    moveR = Move(initial , final)
                                    

                                    initial = Square(row, col) #king move
                                    final = Square(row,6)
                                    moveK = Move(initial , final)

                                    #check possible checks 
                                    if bool:
                                        if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR): #if moving both piece not in check 
                                            #add new move to rook
                                            right_rook.add_move(moveR)
                                            #add new move to king
                                            piece.add_move(moveK)
                                    else:
                                        #add new move to rook
                                        right_rook.add_move(moveR)
                                        #add new move King
                                        piece.add_move(moveK)
            
        if isinstance(piece,Pawn): 
            pawn_moves()
        
        elif isinstance(piece,Knight): 
            knight_moves()

        elif isinstance(piece,Bishop): 
            straightline_moves([
                (-1, 1), #up right 
                (-1,-1), #up left corner
                (1,1), #down right
                (1,-1) #down left 
            ])
        
        elif isinstance(piece,Rook): 
            straightline_moves([
                (-1,0), # up 
                (0 , 1), # right
                (1,0), # down 
                (0,-1)#left
            ])
        
        elif isinstance(piece,Queen):  #queen is combination of the increments of the bishop and rook 
            straightline_moves([
                (-1, 1), #up right 
                (-1,-1), #up left corner
                (1,1), #down right
                (1,-1), #down left 
                (-1,0), # up 
                (0 , 1), # right
                (1,0), # down 
                (0,-1)#left
            ])
        
        elif isinstance(piece,King): 
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col]= Square(row, col)   #creating board full of sqaure objects which will become pieces

    def _add_pieces(self, colour):
        if colour == 'white':
            row_pawn, row_other = (6,7)   #setting position of white pawn 
        else:
            row_pawn, row_other = (1,0)
        #adding pawns to the board 
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(colour))
            

        #adding knights to the board 
        self.squares[row_other][1] = Square(row_other, 1, Knight(colour))
        self.squares[row_other][6] = Square(row_other, 6, Knight(colour))
        

        #adding bishops to the board 
        self.squares[row_other][2] = Square(row_other, 2, Bishop(colour))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(colour))

        #self.squares[4][4] = Square(4, 4, Bishop(colour)) this is for testing valid moves 

        #adding rooks to the board
        self.squares[row_other][0] = Square(row_other, 0, Rook(colour))
        self.squares[row_other][7] = Square(row_other, 7, Rook(colour))

        #self.squares[4][4] = Square(4, 4, Rook(colour)) #this is for testing valid moves

        #adding the queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(colour))

        #self.squares[3][3] = Square(3, 3, Queen(colour)) this is for testing valid moves 

        #adding king
        self.squares[row_other][4] = Square(row_other, 4, King(colour))

        #self.squares[2][3] = Square(2, 3, King(colour)) this is for testing valid moves 


