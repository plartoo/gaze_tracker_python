#!/usr/bin/python 

import time, argparse
from pygame.locals import *
from SimpleCV import Color

from file_manager import *
from train_helper import *
from eye_extractor import EyeExtractor
from gazer_utils import *
from box import Box

CAPTURE_VIDEO = True
video_dir = "./video/"

parser = argparse.ArgumentParser()
msg = "Test the trained network for gaze tracking.\ne.g., $ python gazer.py --test ./output/trained.pkl"
parser.add_argument('--test', dest='testing', help=msg)
args = parser.parse_args()
pkl_file = args.testing

f_m = FileManager()
if (pkl_file is None):		# if no neural network file is provided,
	f_m.setup()		# prepare to collect data
	TEST = False
else:
	fnn = loadTrainedNetwork(pkl_file)
	TEST = True

utils = GazerUtils()
disp = utils.getDisplay()
cam = utils.getCamera()
time.sleep(0.1)

img_size = cam.getImage().size()		# (1280, 720)
bait_box = Box(img_size)
gaze_box = Box(img_size)
classes = bait_box.getBoxLabels()

ee = EyeExtractor()

frame_index = 0
sample_count = 0
found_eye_count = 0
running_frame_total = 0.0			# some constants for book-keeping
sample_limit = 900				# number of samples to collect

print "Press 'q' to quit the program"

while (disp.isNotDone()):
	running_frame_total += 1.0

	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[K_q]:			# quit when 'q' is pressed
		disp.done = True
		time.sleep(0.5)
		print "Program Terminated"
		exit()

	img = cam.getImage()
	img = img.scale(.5)			# use smaller image (320, 240)
	img_width = img.size()[0]

	bait = bait_box.updateBox(frame_index)	# draw bait box for eye to follow
	frame_index = bait['frame_index']
	bait_box_label = bait['box_label']
	c = bait['coordinates']
	img.drawRectangle(c[0],c[1],c[2],c[3],Color.GREEN,0,80)

	le_obj = ee.getLeftEye(img)		# left eye detection
	if (le_obj['lefteye'] is not None):
		found_eye_count += 1
		img.drawRectangle(le_obj['x'], le_obj['y'], le_obj['width'], le_obj['height'])

		if (5 < frame_index < 18):	# only saves 'stable' eye images
			if TEST == False:
				sample_count += 1
				fpath = f_m.getFilePath(sample_count, frame_index, bait_box_label)
				le_obj['lefteye'].save(fpath)
				count_x = img_width * (5.0/6)
				img.dl().text(str(sample_count), (count_x, 0), color=Color.RED)
			else:
				nn_input = extractInput(le_obj['lefteye'])
				v = fnn.activate(nn_input)
				predicted_class = classes[v.argmax(axis=0)]

				g_c = gaze_box.getCoordinatesForThisLabel(predicted_class)
				img.drawRectangle(g_c[0],g_c[1],g_c[2],g_c[3],Color.BLUE,0,80)


	running_percentage = utils.runningPercentage(found_eye_count, running_frame_total)
	img.dl().text(str(running_percentage)+"%", (10, 0), color=Color.RED)

	img.scale(2) 				# rescale the image back to original
	img.save(disp)				# display the results
	if CAPTURE_VIDEO:
		img.save(video_dir+str(int(running_frame_total))+".jpeg")

	time.sleep(0.01)

	if ((TEST==False) and (sample_count == sample_limit)):	# stop when sample limit is reached
		message = "Data collection completed.  Please check the " + \
			  "shell/command prompt for the next step"
		y = img.size()[1]*1.0/2
		img.dl().text(message, (30,y), color=Color.RED)
		img.save(disp)
		disp.done = True

		print "=============\nImage data collection is completed."
		print "Splitting images into test and training set...\n"
		f_m.splitTrainingAndTest()
		print "Spliting training and test data is also completed."
		print "To train the collected data, please run 'train.py'"


