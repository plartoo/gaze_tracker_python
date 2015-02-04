#!/usr/bin/python

import pygame, os
from SimpleCV import Camera, Display

class GazerUtils:

	def __init__(self):
		self.fullscreen_size = None
		self.title = None

	def getCamera(self, properties = {"width": 1280, "height": 720}):
		return Camera(prop_set=properties)

	def __setupDisplayProperties(self):
		# centeralize the display window
		os.environ['SDL_VIDEO_CENTERED'] = '1'

		# get the monitor's full screen size
		pygame.init()
		self.fullscreen_size = pygame.display.Info().current_w, pygame.display.Info().current_h
		self.title = 'Gaze Tracker'

	def getDisplay(self):
		self.__setupDisplayProperties()
		return Display(self.fullscreen_size, pygame.RESIZABLE, self.title)
	
	def runningPercentage(self,success, total):
		val = (1.0 * success/total) * 100.0
		return round(val, 2)

