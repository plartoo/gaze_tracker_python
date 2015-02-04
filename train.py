#!/usr/bin/python 

import argparse, os, re, time
from pybrain.datasets           import ClassificationDataSet
from pybrain.tools.shortcuts	import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules	import SoftmaxLayer
from pybrain.structure		import FeedForwardNetwork, LinearLayer, SigmoidLayer, TanhLayer

from train_helper import *
from file_manager import *
from gazer_utils import *
from confusion_matrix import *

data_dir = "images/"
TRAIN = True
TEST = True
CONFUSION_MATRIX = True

f_m = FileManager()
confusion_matrix_file = f_m.getConfusionMatrixFile()

classes = f_m.getClassLabels()
class_dict = generateDictOfClasses(classes)
hiddendim = 40		# number of nodes in hidden layer (>36 is empirically found to be the best)
m=0.1			# momentum in training (0.1 is empirically the best)
wd=0.01			# weight decay in training (0.01 is empirically the best)

pkl_file = f_m.getPickleFile()

if (os.path.exists(pkl_file)):
	prompt = "WARNING: trained pickle file named\t'" + pkl_file + \
		"'\talready exists.\nTo train based on it, enter 'y'.\n" + \
		"Or please provide a new file name with its complete path: "
	pkl_file = raw_input(prompt)

if (pkl_file == 'y'):
	pkl_file = f_m.getPickleFile()
	fnn = loadTrainedNetwork(pkl_file)
else:
	INPUT_FOLDER = data_dir+"train/"
	paths =  [INPUT_FOLDER+b for b in classes]

	trndata = loadData(paths, classes)
	trndata._convertToOneOfMany( )
	fnn = buildNetwork( trndata.indim, hiddendim, trndata.outdim, outclass=SoftmaxLayer ) 

if TRAIN:
	print "\n\nNumber of training patterns: ", len(trndata)
	print "Input and output dimensions: ", trndata.indim, trndata.outdim
	print "First sample (input, target, class):"
	print trndata['input'][0], trndata['target'][0], trndata['class'][0]
	print "\n================\n"

	try:	# to prevent from aciddentally overwriting the already existing pickle file if errored
		trainer = BackpropTrainer( fnn, dataset=trndata, momentum=m,
						verbose=True, weightdecay=wd)
		trainer.trainUntilConvergence(maxEpochs=80)
	except:
		print "Unexpected error."
		raise

	saveNetwork(pkl_file, fnn)
	print "\nTraining completed."

time.sleep(3)	# because Phyo's old laptop is slow to finish writing the pickle file

if TEST:
	# if we want to test solely with the test data, set TEST to 'True'
	TEST_FOLDER = data_dir + "test/"
	paths =  [TEST_FOLDER+b for b in classes]
	cm = ConfusionMatrix(classes)

	correct_count, incorrect_count, total_test_imgs = 0, 0, 0
	for i in range(len(paths)):
		path = paths[i]

		for img in os.listdir(path):
			m=re.search('.*Thumbs\.(db)', img) # in windows XP, this is a problem

			if (m is None):
				img_path = path + "/" + img
				nn_input = extractInput(Image(img_path))

				m=re.search('\d+_\d+_(\w+)\.png', img)
				correct_class = m.group(1)

				v = fnn.activate(nn_input)
				predicted_class = classes[v.argmax(axis=0)]

				cm.updateConfusionArray(class_dict[correct_class], 
							class_dict[predicted_class])

				total_test_imgs += 1
				if correct_class == predicted_class:
					correct_count += 1
				else:
					incorrect_count += 1 

				print predicted_class + "\t" + correct_class


	correct_pcnt = (100*float(correct_count)/float(total_test_imgs))
	incorrect_pcnt = (100*float(incorrect_count)/float(total_test_imgs))
	print "correct percentage: " + str(correct_pcnt)
	print "incorrect percentage: " + str(incorrect_pcnt)
	print "If correct percentage is below 80%, we recommend you collect more data and"
	print "train the network again from anew or based on old pickle file"
	cm.drawConfusionMatrix(outfilename=confusion_matrix_file)

print "\nTrained network is saved in: " + pkl_file + "\n\n"

