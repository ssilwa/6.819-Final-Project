import operator
from graphmaker import *
import scipy.ndimage
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import string

def run_image(model, image_path, size_x = 28, size_y = 28):
	text_output = {}
	num2alpha = dict(zip(range(1, 27), string.ascii_lowercase))
	curr_img = scipy.ndimage.imread(image_path, flatten = True)
	wordmap = image_pipeline(curr_img)
	j = 0
	for line, words in wordmap.items():
		for word, letters in words.items():
			for i in range(len(letters)-1):
				letter_start = letters[i]
				letter_end = letters[i+1]
				img_subset = curr_img[line[0]:line[1], letter_start:letter_end]
				img_subset = np.pad(img_subset, 2, mode = 'constant', constant_values = 255.0)
				img_subset = scipy.misc.imresize(img_subset, (size_x, size_y))
				img_subset = img_subset.astype('float32')
				img_subset = img_subset/255
				img_subset = 1-img_subset
				# img_subset = img_subset - .172227

				########## Evaluate using Keras ##########
				########## Get the most probable letter ##########
				img_subset2 = np.expand_dims(img_subset, axis=0)
				img_subset2 = np.expand_dims(img_subset2, axis=3)
				value = model.predict(x= img_subset2).argmax(axis = -1)[0]
				# print(num2alpha[value])
				########## Remove this following line ##########
				text_output[(line[0],line[1], letter_start,letter_end)] = num2alpha[value]
				# plt.imshow(img_subset)
				# plt.show()
				############################################################
				if letters[i+1] == max(letters):
					text_output[(line[0],line[1], letter_start,letter_end)] += ' '
	return text_output


def make_text(text_output):
	final_text = ''
	right_order = sorted(text_output.keys(), key=operator.itemgetter(0,1,2,3)) 
	for index in right_order:
		final_text += text_output[index]
	return final_text

if __name__ == '__main__':
	model = load_model('models/bin/overdeep_letter_model.h5')
	final_text = make_text(run_image(model, 'test4.png'))
	print(final_text)