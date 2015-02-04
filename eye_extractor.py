#!/usr/bin/python 

from SimpleCV import HaarCascade, Image

class EyeExtractor:
	def __init__(self, box_width=25, box_height=20):
		self.face_cascade = HaarCascade("./HaarCascades/face.xml")
		self.eyes_cascade = HaarCascade("./HaarCascades/two_eyes_big.xml")

		self.box_width = box_width
		self.box_height = box_height

	def getLeftEye(self, image):
		left_eye, x, y ,w, h = None, None, None, None, None
		both_eyes = self.__findBothEyes(image)
		eyes = both_eyes['eyes']

		if (eyes is not None):
			eyes_x = both_eyes['x']
			eyes_y = both_eyes['y']
			box_width = eyes.width()
			box_height = eyes.height()
			x,y,w,h = self.__getLeftEyeAbsoluteDimensions(eyes_x, eyes_y,
								 box_width, box_height)
			left_eye = image.crop(x,y,w,h)
			
		return {'lefteye':left_eye, 'x':x, 'y':y, 'width':w, 'height':h}

	def __getLeftEyeAbsoluteDimensions(self, eyes_x, eyes_y, box_width, box_height):
		x = eyes_x + (box_width * 2/3)
		y = eyes_y
		return x, y, self.box_width, self.box_height

	def __findBothEyes(self, image):
		eyes, eyes_x, eyes_y = None, None, None

		faces = image.findHaarFeatures(self.face_cascade)
		if ( faces is not None ):
			face = self.__getBiggestFeature(faces)
			face_x, face_y = self.__getTopLeftCooridnates(face)

			two_eyes = face.crop().findHaarFeatures(self.eyes_cascade)
			if ( two_eyes is not None ):
				eyes = self.__getBiggestFeature(two_eyes)
				eyes_x, eyes_y = self.__getTopLeftCooridnates(eyes)
				eyes_x, eyes_y = self.__getAbsoluteEyePosition(face_x, face_y, 
									eyes_x, eyes_y)

		return {'eyes':eyes, 'x':eyes_x, 'y':eyes_y}

	def __getBiggestFeature(self, features):
		return features.sortArea()[-1]#.crop()

	def __getTopLeftCooridnates(self, feature):
		x = feature.x - (feature.width()/2)
		y = feature.y - (feature.height()/2)

		return x,y

	def __getAbsoluteEyePosition(self, face_x, face_y, eyes_x, eyes_y):
		x = face_x + eyes_x
		y = face_y + eyes_y

		return x,y


