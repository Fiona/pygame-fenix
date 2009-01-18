"""
Pygame-Fenix library example
-------
Basic example
-------
This shows an example of a sprite with input.
"""

import os

import pygame
from pygame.locals import *

from fenix.program import Program
from fenix.process import Process
 
 
class Game(Process):
    """ This is our main game loop """
    def begin(self):
        # set up the screen
        Program.set_mode((640,480))
        Program.set_fps(30)
        
        # Create the player
        Guy()
        
        # game loop
        while True:
            
            # Check for pressing escape
            if Program.key(K_ESCAPE):
                Program.quit()
                
            # Leave frame
            yield
    

class Guy(Process):
    """ Our player process """
    def begin(self):
        
        # Initialise some things
        self.x = 400
        self.y = 300
        self.graph = Program.load_png(os.path.join("gfx", "guy.png"))
        
        speed = 0.0
        
        # In-game loop
        while True:
            
            # Do input
            if Program.key(K_LEFT):
                self.angle += 10000
            if Program.key(K_RIGHT):
                self.angle -= 10000
            if Program.key(K_UP):
                speed += 2.0
            if Program.key(K_DOWN):
                speed -= 2.0
                
            # normalise speed
            if speed < -10.0:
                speed = -10.0
            if speed > 10.0:
                speed = 10.0
                
            speed *= 0.9
               
            # send the player forwards or backwards depending on speed 
            self.advance(int(speed))                
            
            # leave frame
            yield
            

# Start the game off
if __name__ == '__main__':
    Game()