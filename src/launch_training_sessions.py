import os
import time

for i in range(1000):
	with open('times.txt', 'a') as f:
		beginning_time = time.time()
		os.system('python killasheep.py')
		end_time = time.time()
		f.write(str(end_time - beginning_time) + '\n')
