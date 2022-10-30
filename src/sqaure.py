
class Square:

    ALPHACOLS = {0 : 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e',5 :'f',6: 'g', 7 : 'h'}

    def __init__(self, row , col, piece=None):  #piece = none as not all sqaures will have a piece
        self.row = row
        self.col = col
        self.piece = piece 
        self.alphacol = self.ALPHACOLS[col]

    def __eq__(self,other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None #if sqaure has a piece it will return true if it doesnt then it will return false

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self,colour):
        return self.has_piece() and self.piece.colour == colour
    
    def has_rival_piece(self,colour):
        return self.has_piece() and self.piece.colour != colour #checking if it has a piece and the colour of that piece is differnet 

    def isempty_or_rival(self,colour):
        return self.isempty() or self.has_rival_piece(colour)

    @staticmethod # can call the method with the class no the object
    def in_range(*args):# able to recieve as many parameters as it wants 
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True
    
    @staticmethod #accesed with the class not the object
    def get_alphacol(col):
        ALPHACOLS = {0 : 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e',5 :'f',6: 'g', 7 : 'h'}
        return ALPHACOLS[col]