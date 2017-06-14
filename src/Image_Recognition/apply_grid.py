import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
import os


def apply_grid(name):
	# Open image file
	image = Image.open('screenshots_cropped/' + name)
	my_dpi=300.


	# Set up figure
	fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
	ax=fig.add_subplot(111)

	# Remove whitespace from around the image
	fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

	# Set the gridding interval: here we use the major tick interval
	myInterval=200.
	loc = plticker.MultipleLocator(base=myInterval)
	ax.xaxis.set_major_locator(loc)
	ax.yaxis.set_major_locator(loc)

	# Add the grid
	ax.grid(which='major', axis='both', linestyle='-')

	# Add the image
	ax.imshow(image)

	# Find number of gridsquares in x and y direction
	nx=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(myInterval)))
	ny=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(myInterval)))

	# Add some labels to the gridsquares
	for j in range(ny):
	    y=myInterval/2+j*myInterval
	    for i in range(nx):
	        x=myInterval/2.+float(i)*myInterval
	        ax.text(x,y,'{:d}'.format(i+j*nx),color='w',ha='center',va='center')

	# Save the figure
	fig.savefig('screenshots_grid/' + name, dpi=my_dpi)


if __name__=='__main__':
	[apply_grid(file) for file in os.listdir('screenshots_cropped') if file[0] != '.' and int(file.split('.')[0]) >= 96]
