import os
import cv2


def transform_data(data_type=None):
	X, Y = [], []

	os.chdir('screenshots_resized/')
	if data_type!=None:
                os.chdir(data_type)
		for i in range(2):
			os.chdir(str(i))
			for image in os.listdir('./'):
				if image[0] == '.':
					continue
				img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
				x = img.flatten()
				X.append(x)
				Y.append(i)
			os.chdir('..')

		os.chdir('../..')
	else:
		for image in os.listdir('./'):
			if image[0] == '.':
				continue
			img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
			x = img.flatten()
			X.append(x)
		os.chdir('..')

	return X, Y
