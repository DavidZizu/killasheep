import os
import cv2


def resize_image(name, label, dataset_type=None):
	img = cv2.imread(label + '/' + name, cv2.IMREAD_GRAYSCALE)
	#print img
        img = cv2.resize(img,None,fx=28. / img.shape[0], fy=28. / img.shape[1], interpolation = cv2.INTER_CUBIC)
	cv2.imwrite('../../screenshots_resized/' + dataset_type + '/' + label + '/' + name, img) if dataset_type else cv2.imwrite('screenshots_resized/' + name, img)

if __name__=='__main__':
	#for training model
	# os.chdir('screenshots_split/train_split/')
	# [resize_image(file, 'train_split', '0') for file in os.listdir('0') if file[0] != '.']
	# [resize_image(file, 'train_split', '1') for file in os.listdir('1') if file[0] != '.']
	# os.chdir('../test_split')
	# [resize_image(file, 'test_split', '0') for file in os.listdir('0') if file[0] != '.']
	# [resize_image(file, 'test_split', '1') for file in os.listdir('1') if file[0] != '.']

	os.chdir('run')
	[resize_image(file, label='screenshots_split') for file in os.listdir('screenshots_split') if file[0] != '.']
