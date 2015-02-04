#!/usr/bin/python

import random

class Box:
	def __init__(self,monitorSize, random=False):
		self.random = random
		self.refresh_rate = 20			# change box location every 20 frames
		self.box_index = 0
		self.box_labels = ['topleft', 'topcenter', 'topright',
					'centerleft', 'centercenter', 'centerright',
					'bottomleft', 'bottomcenter', 'bottomright']
		self.cur_label = self.box_labels[4]	# start from center as default
		self.num_boxes = len(self.box_labels)

		self.x = monitorSize[0]/(3*2)
		self.y = monitorSize[1]/(3*2)
		self.width = monitorSize[0]/(3*2)
		self.height = monitorSize[1]/(3*2)

		self.coordinates = {
					'topleft'	: [0, 0, self.width, self.height],
					'topcenter'	: [self.x, 0, self.width, self.height],
					'topright'	: [self.x*2, 0, self.width, self.height],
					'centerleft'	: [0, self.y, self.width, self.height],
					'centercenter'	: [self.x, self.y, self.width, self.height],
					'centerright'	: [self.x*2, self.y, self.width, self.height],
					'bottomleft'	: [0, self.y*2, self.width, self.height],
					'bottomcenter'	: [self.x, self.y*2, self.width, self.height],
					'bottomright'	: [self.x*2, self.y*2, self.width, self.height],
				   }

	def updateBox(self, frame_index):
		frame_index += 1
		if (frame_index % self.refresh_rate == 0):
			frame_index = 0			# reset the frame_index
			self.cur_label = self.__getNewBoxLabel()	# update to new box label

		c = self.coordinates[self.cur_label]

		return {'coordinates':c, 'box_label': self.cur_label, 'frame_index': frame_index}

	def getBoxCoordinates(self, box_label):
		return self.coordinates[box_label]

	def getBoxLabels(self):
		return self.box_labels

	def getCoordinatesForThisLabel(self,label):
		return self.coordinates[label]

	def __getNewBoxLabel(self):
		self.box_index += 1			# increment the box_index
		self.box_index %= self.num_boxes	# reset if it overflows

		if self.random:				# if it's random, we'll override the above value
			self.box_index = random.randint(0,(self.num_boxes-1))

		return self.box_labels[self.box_index]


