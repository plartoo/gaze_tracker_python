#!/usr/bin/python 

import os, re, pickle
from numpy			import *
from pybrain.datasets		import ClassificationDataSet
from SimpleCV			import Image, Color

def thresholdOp(img):
	return img.colorDistance(Color.WHITE).binarize(230).morphOpen()

def extractInput(img):
	img_data = thresholdOp(img)
	flattened = img_data.getNumpy()[:,:,1].flatten()
	flattened[flattened==255]=1
	return flattened	

def generateDictOfClasses(klasses):
	classes = {}
	c = 0
	for k in klasses:
		classes[k] = c
		c += 1
	return classes

def loadData(paths, classes):
	class_dict = generateDictOfClasses(classes)
	all_data = None

	for i in range(len(paths)):
		path = paths[i]
		print path

		for img in os.listdir(path):
			m=re.search('.*Thumbs\.(db)', img) # in windows XP, this is a problem

			if (m is None):
				img_path = path + "/" + img
				img_data = thresholdOp(Image(img_path))
				flattened = img_data.getNumpy()[:,:,1].flatten()	# 25x20 (wxh)
				flattened[flattened==255]=1				# set every '255' to '1'

				if all_data is None:
					all_data = ClassificationDataSet(len(flattened), 
							nb_classes=len(classes), class_labels=classes)

				all_data.addSample(flattened, [class_dict[classes[i]]]) # [data[1],data[2]]

	return all_data


def loadTrainedNetwork(pickle_file):
	fd = open(pickle_file,'r')
	fnn = pickle.load(fd)
	fnn.sorted = False
	fnn.sortModules()
	fd.close()
	print "Loaded trained network from: " + pickle_file
	return fnn

def saveNetwork(pickle_file, network):
	fd = open(pickle_file, 'w')
	pickle.dump(network, fd)
	fd.close()
	print "\nTrained network is saved in: " + pickle_file

