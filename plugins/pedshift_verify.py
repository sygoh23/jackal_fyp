import os
import sys
import fileinput
import matplotlib
import matplotlib.pyplot as plt

old_file = open('/home/ubuntu/ws/jackal_fyp/src/development/resources/pedsim/start_at_b72.xml', 'r+')

all_x = []
all_y = []
agent_x = []
agent_y = []
x_shift = 0
y_shift = 0

n = 1
found_agent = 0
print("Processing file...")
for line in old_file:
	print("Line %d" % n)
	x_pos = line.find('x=')
	y_pos = line.find('y=')

	test_agent = line.find('agent')
	if test_agent > 0:
		found_agent = 1

	# If there are coordinates in the line:
	if x_pos > 0:
		# Extract 'x' coordinate:
		i = 4
		x_stop = True
		while x_stop == True:
			x_stop = line[x_pos+i].isnumeric()
			i += 1

		# Extract 'y' coordinate:
		j = 4
		y_stop = True
		while y_stop == True:
			y_stop = line[y_pos+j].isnumeric()
			j += 1

		# Replace new coordinates:
		x_old = int(line[x_pos+3:x_pos+i-1])
		y_old = int(line[y_pos+3:y_pos+j-1])
		if found_agent == 0:
			all_x.append(x_old)
			all_y.append(y_old)
		if found_agent == 1:
			agent_x.append(x_old)
			agent_y.append(y_old)

	else:
		test = 1
	n += 1

plt.scatter(all_x, all_y, c='g', marker='.', s=30)
plt.scatter(agent_x, agent_y, c='r', marker='.', s=30)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
print("Complete!")
