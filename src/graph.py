from random import *
import matplotlib.pyplot as plt

a = []

with open('times.txt', 'r') as f:
	while True:
		s = f.readline().strip()
		if s != "":
			a.append(float(s))
		else:
			break

x = []
y = []
for i in range(0, len(a), 5):
	x.append(i)
	avg = 0
	for j in range(i, min(i + 5, len(a))):
		avg += a[j]
	y.append(avg / 5.)

plt.plot(x, y)
plt.show()
