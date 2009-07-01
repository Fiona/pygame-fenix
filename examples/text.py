"""
Pygame-Fenix library example
-------
Text example
-------
Just a fun thing with text
"""

import os
from random import randrange 
import copy

import pygame
from pygame.locals import *

from fenix.program import Program
from fenix.process import Process
from fenix.locals import *
 
 
class Game(Process):
    """ This is our main game loop """
    def begin(self):
        # set up the screen
        Program.set_mode((640,480))
        Program.set_fps(30)
        
        font = Program.load_fnt("gfx/font.ttf", 20)
        cheri_font = Program.load_fnt("gfx/cheri.ttf", 30)
        
        # Create the text objects
        text_guys = []
        text_guys.append(Program.write(font, 100, 100, 4, "Texts"))
        text_guys.append(Program.write(font, 200, 150, 4, "Are"))
        text_guys.append(Program.write(font, 400, 200, 4, "Processes"))
        text_guys.append(Program.write(font, 550, 250, 4, "Too!"))
        
        # This is our scrolly message
        message = "This is the Fenix Pygame library! Who needs the goddamn amiga?" + \
            " Weeee! I'm having far too much fun with this! You'll have to try out the" + \
            " library for yourself. :D Fiona made this in the last bit of 2008. For realsies." + \
            " OMG I think it's gonna loop now.....                                           " + \
            " so i herd you like mudkips..?"
            
        scroll_text = []
        
        # game loop
        while True:
            
            # strobe the message along the top
            for single in text_guys:
                single.colour = (randrange(50,200), randrange(50,200), randrange(50,200))
               
            text_guys[3].angle += 3000
            
            # if we don't have a scrolly message, create it
            if len(scroll_text) < 1:
                a,b = 650, 0
                for x in message:
                    a += 25
                    b += 20000
                    guy = Program.write(cheri_font, a, 420, text = x)
                    guy.mystery_angle = b
                    guy.init_x = a
                    guy.colour = (randrange(50,200), randrange(50,200), randrange(50,200))
                    scroll_text.append(guy)
            
            # loop through the scrolly characters and move them and stuff
            for single in scroll_text:
                single.x -= 5                
                single.y = 420 + Program.get_disty(single.mystery_angle, 30)
                single.mystery_angle += 20000
                if single.x <= -25:
                    scroll_text.remove(single)                    
                    single.signal(S_KILL)

            # Check for pressing escape
            if Program.key(K_ESCAPE):
                Program.quit()
                
            # Leave frame
            yield


# Start the game off
if __name__ == '__main__':
    Game()