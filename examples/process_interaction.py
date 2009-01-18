"""
Pygame-Fenix library example
-------
Process interaction
-------
This demonstrates how processes can get information from each other.
Shows distance gathering, angle comparison and collision detection. 
Also demonstrates z sorting.
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
        
        # Create the players
        Guy(270, 180)
        
        # game loop
        while True:
            
            # Check for pressing escape
            if Program.key(K_ESCAPE):
                Program.quit()
                
            # Leave frame
            yield
    

class Guy(Process):
    """ Our player process """
    def begin(self, x, y):
        
        # Initialise some things
        self.x = x
        self.y = y
        # Z order. The lower the Z the "closer" they are to the player.
        # Guy has a lower Z than Other_guy so will appear on top.
        self.z = -300
        self.graph = Program.load_png(os.path.join("gfx", "guy.png"))
        speed = 0
        
        other = Other_guy(320, 240)
        
        font = Program.load_fnt("gfx/font.ttf", 10)
        distance_text = Program.write(font, 0, 0)
        angle_text = Program.write(font, 0, 15)
        collision_text = Program.write(font, 0, 30)
        
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
            
            # Get distance from other guy
            distance_text.text = "Distance: "+ str(self.get_dist(other))
            angle_text.text = "Angle to: "+ str(int(self.get_angle(other)/1000))
            collision_text.text = "Colliding: "+ ("True" if self.collision(other) else "False")
            
            # leave frame
            yield
            


class Other_guy(Process):
    """ The process we'll be comparing with """
    def begin(self, x, y):
        
        # Initialise some things
        self.x = x
        self.y = y
        self.z = -200
        self.graph = Program.load_png(os.path.join("gfx", "guy.png"))
        
        while True:
            yield
        

# Start the game off
if __name__ == '__main__':
    Game()