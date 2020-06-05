import os
import sys
import fileinput

old_file = open(input("Please enter input file path: "), 'r+')
new_file = open(input("Please enter output file path: "), 'a')
x_shift = int(input("Please enter X shift value: "))
y_shift = int(input("Please enter Y shift value: "))
z_shift = int(input("Please enter Z shift value: "))

n = 1
modify_pose = False
print("Processing file...")
for line in old_file:
	# Check for the campus model:
	world_flag = line.find("<model name='Campus")
	if world_flag > 0: 
		modify_pose = True

	# If we are inside the campus model, look for the pose:
	if modify_pose == True:
		has_pose = line.find("<pose>")

		if has_pose > 0:
			print("Updating pose...")

			# Parse x value:
			stop = True
			x_pos = has_pose
			i = 7
			while stop == True:
				stop = line[x_pos+i].isnumeric()
				i += 1
			x_old = int(line[x_pos+6: x_pos+i-1])
			x_new = x_old + x_shift
			print("x: %d >>> x: %d" % (x_old, x_new))				

			# Parse y value:
			j = 1
			stop = True
			y_pos = x_pos+i
			while stop == True:
				stop = line[y_pos+j].isnumeric()
				j += 1
			y_old = int(line[y_pos: y_pos+j])	
			y_new = y_old + y_shift
			print("y: %d >>> z: %d" % (y_old, y_new))	

			# Parse z value:
			k = 0
			stop = True
			z_pos = y_pos+j+2
			while stop == True:
				stop = line[z_pos+k].isnumeric()
				k += 1
			z_old = int(line[z_pos-2: z_pos+k])
			z_new = z_old + z_shift			
			print("z: %d >>> z: %d" % (z_old, z_new))	

			# Replace string:
			old_str = str(x_old) + " " + str(y_old) + " " + str(z_old)
			new_str = str(x_new) + " " + str(y_new) + " " + str(z_new)
			line_new = line.replace(old_str, new_str)
			new_file.write(line_new)
		else:
			new_file.write(line)	
	else:
		new_file.write(line)
	n += 1

print("Complete!")