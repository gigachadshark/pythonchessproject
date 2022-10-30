import pygame 
import sys

from const import *
from game import Game
from sqaure import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()



    def mainloop(self):
        
        game = self.game    #game and screen used ined of self.game/ self.screen to make code easier to follow and understand 
        screen = self.screen 
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                #CLICK
                if event.type == pygame.MOUSEBUTTONDOWN: #this is for the click on the piece
                    dragger.update_mouse(event.pos)   #update mouse 
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece(): #checking if clicked sqaure has a piece 
                        piece = board.squares[clicked_row][clicked_col].piece
                        #valid piece (colour)?
                        if piece.colour == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos) #if sqaure has a piece intial row and col is saved in the case of invalid move to return to valid position
                            dragger.drag_piece(piece)
                            #show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                        

                elif event.type == pygame.MOUSEMOTION: #MOUSE MOTION
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    game.set_hover(motion_row,motion_col)

                    if dragger.dragging: #drag a piece that has been saved previously to drag 
                        dragger.update_mouse(event.pos) #update this first as blit depends on mouse position 
                        game.show_bg(screen) #this is so while dragging doesnt make the piece seem like there are 2 
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen) #while dragging all the other pieces remain on the board
                        game.show_hover(screen)
                        dragger.update_blit(screen)


                elif event.type == pygame.MOUSEBUTTONUP: #CLICK RELEASE

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY //SQSIZE
                        released_col = dragger.mouseX //SQSIZE

                        #create possible move 
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        #asking if valid move
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)
                            #sounds
                            game.play_sound(captured)
                            #show methods (draw onto screen)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            #next turn 
                            game.next_turn()



                    dragger.undrag_piece()

                #key press
                elif event.type == pygame.KEYDOWN:
                    
                    #changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()
                    
                    #changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game     
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT: #quit the application
                    pygame.quit()
                    sys.exit()



            pygame.display.update()

main = Main()
main.mainloop()