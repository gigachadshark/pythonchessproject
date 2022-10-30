from re import S
import pygame

from const import *
from board import Board
from dragger import Dragger 
from config import Config
from sqaure import Square

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None 
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    #blit methods 

    def show_bg(self,surface):  
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):      #setting the colour of the boxes
                #colour
                colour = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark  
                '''insted of hard coding colours using variables instead so that theme will change colours for each one'''
                #rect
                rect = (col * SQSIZE, row * SQSIZE,SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, colour, rect) #here the boxes with the colours are made 

                #row coordinates 
                if col == 0:
                    #colour
                    colour = theme.bg.dark if row % 2 == 0 else theme.bg.light  #marking the coords of the sqaures 1-8
                    #label
                    label = self.config.font.render(str(ROWS-row), 1, colour)
                    label_pos = (5, 5 + row * SQSIZE)
                    #blit labels 
                    surface.blit(label, label_pos)
                
                # col coordinates 
                if row == 7:
                    #colour
                    colour = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light  #marking the coords of the sqaures 1-8
                    #label
                    label = self.config.font.render(Square.get_alphacol(col), 1, colour)
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    #blit labels 
                    surface.blit(label, label_pos)

    def show_pieces(self, surface):
         for row in range(ROWS):
            for col in range(COLS):  
                #check if there is a piece on that specific square
                if self.board.squares[row][col].has_piece():
                    piece= self.board.squares[row][col].piece    #saving the checked piece into a variable 
                    
                    #all piece except dragger piece 
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80) #this is so that pieces return to original size and are not large 
                        img = pygame.image.load(piece.texture)   #coverting the piece into a image
                        img_center = col * SQSIZE + SQSIZE // 2 , row *SQSIZE +SQSIZE //2    #centering the image
                        piece.texture_rect = img.get_rect(center = img_center)  
                        surface.blit(img, piece.texture_rect)   #telling pygyame the image 

    def show_moves(self,surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece
            #loop all valid moves  
            for move in piece.moves:
                #create a colour, rect then blit
                colour = theme.moves.light if (move.final.row + move.final.col) % 2 ==0 else theme.moves.dark 
                #rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE , SQSIZE) 
                #blit
                pygame.draw.rect(surface, colour, rect)

    def show_last_move(self,surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial,final]:
                #colour
                colour = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark 
                #rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface,colour,rect)
                
    def show_hover(self,surface):
        if self.hovered_sqr:
            #colour
            colour = (180,180,180)
            #rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            #blit
            pygame.draw.rect(surface,colour,rect, width = 3)

    #other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self,row,col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__() #creating a new game therefore restarting it 