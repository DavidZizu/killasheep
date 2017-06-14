from PIL import Image
import math
import os

def cut_image(name):
    """slice an image into parts slice_size tall"""
    img = Image.open('screenshots_cropped/' + name)

    for i in range(3):
        for j in range(3):
            # (left, upper, right, lower)
            img.crop((j * 200, i * 200, j * 200 + 200, i * 200 + 200)).save('screenshots_split/' + name.split('.')[0] + '_slice_' + str(i) + '_' + str(j) + '.png')

if __name__ == '__main__':
    [cut_image(file) for file in os.listdir('screenshots_cropped') if file[0] != '.' and int(file.split('.')[0]) > 150]
