import operator
from graphmaker import *
import scipy.ndimage

def run_image(image_path, size_x = 28, size_y = 28):
	text_output = {}
	curr_img = scipy.ndimage.imread(image_path, flatten = True)
	wordmap = image_pipeline(curr_img)
	for line, words in wordmap.items():
		for word, letters in words.items():
			for i in range(len(letters)-1):
				letter_start = letters[i]
				letter_end = letters[i+1]
				img_subset = curr_img[line[0]:line[1], letter_start:letter_end]
				img_subset = scipy.misc.imresize(img_subset, (size_x, size_y))
				########## Evaluate using Keras ##########
				########## Get the most probable letter ##########
				# text_output[(line[0],line[1], letter_start,letter_end)] = model.evaluate(img_subset)
				########## Remove this following line ##########
				text_output[(line[0],line[1], letter_start,letter_end)] = 'a'
				############################################################
				if i == len(letters)-2:
					text_output[(line[0],line[1], letter_start,letter_end)] += ' '
	return text_output


def make_text(text_output):
	final_text = ''
	right_order = sorted(text_output.keys(), key=operator.itemgetter(0,1,2,3)) 
	for index in right_order:
		final_text += text_output[index]
	return final_text

if __name__ == '__main__':
	final_text = make_text(run_image('paragraph.png'))
	print(final_text)