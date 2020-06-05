import os
import sys
import fileinput

old_file = open(input("Please enter input file path: "), 'r+')
new_file = open(input("Please enter output file path: "), 'a')
x_shift = int(input("Please enter X shift value: "))
y_shift = int(input("Please enter Y shift value: "))
z_shift = int(input("Please enter Z shift value: "))

n = 1
modify_next_pose = False
print("Processing file...")
for line in old_file:
	new_line = line

	# Check for specific models to update:
	ground_flag = line.find("<model name='ground")
	if ground_flag > 0: print("\nFound ground plane!")
	campus_flag = line.find("<model name='Campus")
	if campus_flag > 0: print("\nFound campus model!")
	bounding_flag = line.find("<model name='Bounding")
	if bounding_flag > 0: print("\nFound bounding box!")

	# If the model is present, modify the next <pose> tag:
	if ground_flag > 0 or campus_flag > 0 or bounding_flag > 0:
		modify_next_pose = True

	# Check line for the <pose> tag:
	if modify_next_pose == True and line.find("<pose>") > 0:
		print("Updating pose...")
		# Separate out old coordinates:
		data = line[line.find("<pose>")+6:len(line)-8].split()
		x_old, y_old, z_old = int(data[0]), int(data[1]), int(data[2])

		# Prepare new coordinates:
		x_new, y_new, z_new = x_old + x_shift, y_old + y_shift, z_old + z_shift
		print("(%d, %d, %d) >>> (%d, %d, %d)" % (x_old, y_old, z_old, x_new, y_new, z_new))

		# Replace string:
		old_str = str(x_old) + " " + str(y_old) + " " + str(z_old)
		new_str = str(x_new) + " " + str(y_new) + " " + str(z_new)
		line_new = line.replace(old_str, new_str, 1)

		# Write to file:
		new_file.write(line_new)
		modify_next_pose = False
	else:
		new_file.write(new_line)
print("\nComplete!")
