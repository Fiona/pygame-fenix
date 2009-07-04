"""
Invaders demo
This example was initially wrote for europython 2009.
Due to technical difficulties I was unable to show it,
it now lives here - so it was useful afterall!

It is a very simple demo, but it is a fairly good example
as it shows a real-world example of a game that has input,
multiple instances of processes and interactions (collisions)
between other processess.
"""
from fenix.program import Program
from fenix.process import Process 
from pygame.locals import *
from fenix.locals import *


class Game(Process):
	""" The main game process sets up the scene and checks for
	the escape key being pressed (for quitting)
	"""
	def begin(self):
		# Set the resolution and the frames per second
		Program.set_mode((800, 600))
		Program.set_fps(30)

		# load the graphics and store a pointer to the loaded surfaces.
		# Assigning them to the main game object is purely a convention
		# and is not required for pygame-fenix. They are set as members of
		# the game because it is a persistant process that lasts for the
		# length of the game.
		self.g_player = Program.load_png("player.png")
		self.g_enemy = Program.load_png("enemy.png")
		self.g_bullet = Program.load_png("bullet.png")

		# Because it in persistent and holds references to all our graphic
		# surfaces, it makes sense to pass it to all of our objects.
		# Again this is purely a convention. A recommended convention, but
		# entirely optional nontheless.
		Player(self)

		# We create the invaders along the top of the screen.
		for x in range(100, 601, 50):
			Enemy(self, x)

		# Note that we do not save references to the processes. Simply the act
		# of initialising one will cause it to exist. It's internal loop will
		# execute immediately and it can happily act independantly of everything
		# else.
		
		while True:
			# This is the main loop

			# Simple input check
			if Program.key(K_ESCAPE):
				Program.exit()

			# The yield statement signifies that this object is finished for the
			# current frame, on the next frame the loop will resume here until it
			# hits the yield statement again. All objects are designed to act this way.
			yield
			

class Player(Process):
	""" The player object simply takes input and reacts accordingly. """
	def begin(self, game):
		self.x, self.y = 400, 500
		self.graph = game.g_player

		while True:

			# Processes have many member variables, one of the most common is x and y which
			# directly map to the process' coordinates on the screen. They, like all member
			# variables, can be altered at any time.
			# Here we check if the ship should move left/right and change the x (horisontal)
			# coordinate appropriately.
			if Program.key(K_LEFT):
				self.x -= 4
			if Program.key(K_RIGHT):
				self.x += 4
			# The final bit of input is shooting. Again we pass in the game object so we can
			# access graphics and honour the convention set for ourselves when creating the
			# player and enemies.
			if Program.key_released(K_SPACE):
				Bullet(game, self)
				
			yield
			

class Enemy(Process):
	""" The basic enemy process """
	def begin(self, game, x):
		self.x = x
		self.y = 150
		self.graph = game.g_enemy

		_dir = 0
		rem = x
		
		while True:

			# We simply move the enemy right and left.
			# Note that because we are using generators we do not have to keep these throw-away
			# storage variables as members of the process object.
			if _dir:
				if self.x < rem + 50:
					self.x += 2
				else:
					_dir = 0
			else:
				if self.x > rem - 50:
					self.x -= 2
				else:
					_dir = 1
			
			yield
			

class Bullet(Process):
	""" Bullets move up and collide with any enemy. """
	def begin(self, game, player):
		self.x, self.y = player.x, player.y
		self.graph = game.g_bullet

		while True:

			# Here we are telling the bullet process to check
			# collisions with any Enemy process. This method either
			# returns a reference to a collided object or None
			e = self.collision("Enemy")
			if e:
				# If we have collided then we destroy both the enemy
				# and the bulllet
				e.signal(S_KILL)
				# Note that simply exiting from the loop and finishing
				# the execution of the method without yielding causes
				# this object to be removed. Pygame-fenix will do any
				# necessary clean-up.
				# You can do self.signal(S_KILL) and it will have the
				# same effect when the next yield is hit.
				return

			self.y -= 10

			# Quick clean up by checking if the bullet is offscreen
			if self.y < 0:
				return
				
			yield
			

if __name__ == '__main__':
	# To start the game we create the main Game process. The first time
	# a process is created pygame-fenix will invisibly initialise
	# itself. There is no need to specifically tell pygame-fenix to start
	# dealing wih processes.
	# This method of creating objects and having them immediately enter
	# into existance in a real way makes writing games extremely simple.
	# Write the game and not the engine.
	Game()
