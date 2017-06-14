from PIL import Image
import os.path
import os

def crop_image(name):
	print os.getcwd()
	img = Image.open('screenshots/' + name)
	#img2 = img.crop((420, 149, 1020, 749))
	img2 = img.crop((660, 268, 1260, 868))
        img2.save('screenshots_cropped/' + name)


if __name__=='__main__':
	[crop_image(file) for file in os.listdir('screenshots') if file[0] != '.' and int(file.split('.')[0]) >= 96]
