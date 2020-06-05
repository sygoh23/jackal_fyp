import os
import sys
import fileinput

old_file = open(input("Please enter input file path: "), 'r+')
new_file = open(input("Please enter output file path: "), 'a')
x_shift = int(input("Please enter X shift value: "))
y_shift = int(input("Please enter Y shift value: "))

n = 1
print("Processing file...")
for line in old_file:
	x_pos = line.find('x=')
	y_pos = line.find('y=')

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
		x_new = x_old + x_shift
		y_new = y_old + y_shift
		print("Line %d: (%d, %d) >>> (%d, %d)" % (n, x_old, y_old, x_new, y_new))

		# Replace all strings:
		x_old_str = 'x="' + str(x_old) + '"'
		y_old_str = 'y="' + str(y_old) + '"'
		x_new_str = 'x="' + str(x_new) + '"'
		y_new_str = 'y="' + str(y_new) + '"'
		line_new = line.replace(x_old_str, x_new_str)
		line_new = line_new.replace(y_old_str, y_new_str)
		new_file.write(line_new)
	else:
		new_file.write(line)
	n += 1

print("Complete!")
