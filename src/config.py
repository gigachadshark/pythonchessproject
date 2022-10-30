import pygame
import os

from sound import Sound
from theme import Theme


class Config:

    def __init__(self):
        self.themes = [] # theme - empty list 
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx] #active theme
        self.font = pygame.font.SysFont('monospace', 18, bold = True)
        self.move_sound = Sound(
            os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(
            os.path.join('assets/sounds/capture.wav'))


    def change_theme(self):
        self.idx += 1 # incremend index by one 
        self.idx %= len(self.themes) # e.g [t1,t2,t3,t4] onces reaches last theme cant increments so goes back to first theme and repeats
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme((234,235,200), (119,154,88), (244,247,116), (172,195,51), (255,64,64),(255,0,0))
        brown = Theme((235,209,166), (165,117,80), (245,234,100), (209,185,59), (255,64,64),(255,0,0))
        blue = Theme((229,228,200), (60,95,135), (123,187,227), (43,119,191), (255,64,64),(255,0,0))

        self.themes = (green, brown ,blue)
