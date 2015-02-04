import numpy as np
import matplotlib.pyplot as plt

#self.conf_arr = [[73.0, 0.0, 4.0, 8.0, 0.0, 2.0, 1.0, 0.0, 0.0], [6.0, 72.0, 1.0, 0.0, 11.0, 0.0, 0.0, 2.0, 2.0], [6.0, 0.0, 61.0, 0.0, 0.0, 23.0, 0.0, 0.0, 0.0], [11.0, 2.0, 0.0, 45.0, 4.0, 0.0, 4.0, 20.0, 1.0], [1.0, 14.0, 0.0, 1.0, 65.0, 0.0, 1.0, 10.0, 2.0], [5.0, 0.0, 14.0, 4.0, 0.0, 62.0, 0.0, 0.0, 2.0], [0.0, 0.0, 0.0, 5.0, 1.0, 0.0, 57.0, 26.0, 2.0], [0.0, 0.0, 0.0, 1.0, 3.0, 0.0, 18.0, 61.0, 8.0], [0.0, 5.0, 0.0, 0.0, 5.0, 9.0, 7.0, 39.0, 25.0]]

class ConfusionMatrix:
	def __init__(self, classes):
		self.conf_arr = [[0] * len(classes) for i in range(len(classes))]

	def updateConfusionArray(self, r, c):
		self.conf_arr[r][c] += 1

	def drawConfusionMatrix(self, outfilename="confusion_matrix.png"):

		norm_conf = []
		for i in self.conf_arr:
			a = 0
			tmp_arr = []
			a = sum(i, 0)

			for j in i:
				tmp_arr.append(float(j)/float(a))

			norm_conf.append(tmp_arr)

		fig = plt.figure()
		plt.clf()
		ax = fig.add_subplot(111)
		ax.set_aspect(1)
		res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, 
				interpolation='nearest')

		width = len(self.conf_arr)
		height = len(self.conf_arr[0])

		for x in xrange(width):
			for y in xrange(height):
				ax.annotate(str(self.conf_arr[x][y]), xy=(y, x), 
					horizontalalignment='center',
					verticalalignment='center')

		cb = fig.colorbar(res)
		alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		plt.xticks(range(width), alphabet[:width])
		plt.yticks(range(height), alphabet[:height])
		plt.savefig(outfilename, format='png')
		print "Confusion matrix saved in:\t" + outfilename

