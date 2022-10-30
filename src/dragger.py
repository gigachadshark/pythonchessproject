import pygame

from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    #blit methods 
    def update_blit(self, surface):
        self.piece.set_texture(size = 128)# the piece that is being dragged will be bigger than the other pieces 
        texture = self.piece.texture

        img = pygame.image.load(texture) #txture

        img_center = (self.mouseX , self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center) #rect

        surface.blit(img, self.piece.texture_rect) #blitting the piece (transfering from one surface to another )

    
    
    def update_mouse(self, pos):
        self.mouseX , self.mouseY = pos #set positions (x,y)

    def save_initial(self,pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] //SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True 

    def undrag_piece(self):
        self.piece = None
        self.dragging = False 