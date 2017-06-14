import os
import shutil
from random import shuffle

os.chdir('screenshots_resized')

for folder in ['test_split', 'train_split']:
	os.chdir(folder)
	os.system('del 0/*')
	size = len(os.listdir(os.getcwd() + '/' + '1'))
	os.chdir('0_all')
	a = os.listdir('.')
	shuffle(a)
	for x in a[:size]:
		shutil.copyfile(x, '../0/{}'.format(x))
	os.chdir('..')
	os.chdir('..')