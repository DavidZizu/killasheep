import os
from PIL import Image
from random import random

os.chdir('screenshots_split')

for x in os.listdir('.'):
	if x.count('.png') > 0:
		a = Image.open(x)
		a.show()
		cat = int(raw_input("Is there a sheep on that image?"))
		folder = 'test_split' if random() < 0.1 else 'train_split' + '/{}'.format(cat)
		print('cp {} {}/.'.format(x, folder))
		
