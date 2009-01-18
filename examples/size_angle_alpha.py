"""
Pygame-Fenix library example
-------
Dynamic graphics examples 
-------
Demonstrating processes with dynamic angle, size and alpha settings.
"""

import os
from random import randrange

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
        
        # Create the ... things
        for x in range(10):
            Box()
        
        # game loop
        while True:
            
            # Check for pressing escape
            if Program.key(K_ESCAPE):
                Program.quit()
                
            # Leave frame
            yield
    

class Box(Process):
    """ Little box rotatey thing """
    def begin(self):
        
        # Initialise some things
        self.x = randrange(50, 600)
        self.y = randrange(50, 450)

        self.alpha = 120
        self.size = randrange(10, 250)
        
        self.graph = Program.new_map(100,100)
        Program.map_clear(self.graph, (randrange(50, 200), randrange(50, 200), randrange(50, 200)))
                 
        direction = randrange(0, 2)
        size_to = 0 if direction else 250
        
        # In-game loop
        while True:
            
            # Spin these dudes
            self.angle += 5000 if direction else -5000 
            
            # Size them around
            if size_to == 250:
                self.size += 5
                if self.size >= size_to:
                    size_to = 0
            if size_to == 0:
                self.size -= 5
                if self.size <= size_to:
                    size_to = 250
                    
            # leave frame
            yield
            

# Start the game off
if __name__ == '__main__':
    Game()