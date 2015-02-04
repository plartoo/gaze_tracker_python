#!/usr/bin/python

import os, random, shutil, glob
from box import Box

class FileManager:

	def __init__(self, data_dir="./images/", output_dir="./output/"):
		self.data_dir = data_dir
		self.train_dir = self.data_dir + "train/"
		self.test_dir = self.data_dir + "test/"
		
		self.output_dir = output_dir
		self.pickle_file = self.output_dir + "trained.pkl"
		self.confusion_matrix_file = self.output_dir + "conf.png"
		self.class_labels = Box((0,0)).getBoxLabels()

	def setup(self):
		if (self.__checkDir()):
			print "\nWARNING: Directory named:\t" + self.data_dir + "\talready exists!"
			self.__askAlternativeDir()
		
		if (self.data_dir == 'n'):
			print "Program terminating due to not providing alternative data directory\n"
			exit()
		else:
			print "Directory named:\t"+ self.data_dir +"\tcreated\n"
			os.makedirs(self.data_dir)

	def getDir(self):
		return self.data_dir
		
	def getFileName(self, sample_count, frame_number, class_label):
		s = str(sample_count) + "_" + str(frame_number) + "_" + class_label + ".png"
		return s

	def getFilePath(self, sample_count, frame_number, class_label):
		fname = self.getFileName(sample_count, frame_number, class_label)
		return self.data_dir + fname

	def getPickleFile(self):
		return self.pickle_file

	def getConfusionMatrixFile(self):
		return self.confusion_matrix_file

	def getClassLabels(self):
		return self.class_labels

	def __checkDir(self):
		already_exists = False

		if (os.path.exists(self.data_dir)):
			already_exists = True

		return already_exists

	def __askAlternativeDir(self):
		prompt = "Please provide an alternative directory name to save data files.\n" + \
			"Or enter 'n' to quit the program: "
		self.data_dir = raw_input(prompt)

	def splitTrainingAndTest(self, ratio=0.8):
		for l in self.class_labels:
			files = glob.glob(self.data_dir+"*_"+l+".png")
			random.shuffle(files)
			train_sz = round(len(files)*0.8)
			

			train_dir = self.train_dir + l
			test_dir = self.test_dir + l
			os.makedirs(train_dir)
			os.makedirs(test_dir)

			count = 0
			for f in files:
				dirname = train_dir if (count < train_sz) else test_dir
				print "count: " + str(count) + "\t" + f + "\t=>\t" + dirname
				shutil.move(f, dirname)
				count += 1

			print "For class: " + l + "\tmoved " + str(train_sz) + " files into " + \
				self.train_dir + "\nand " + str(len(files)-train_sz) + \
				" files into " + self.test_dir


