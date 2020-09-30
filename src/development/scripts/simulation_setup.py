# STEP 1: CHOOSE ROBOT STARTING LOCATION:
starting_location = 2
# 0: Within Vicinity (ENG Lecture Theatres)
# 1: Sticking Point
# 2: ENG Faculty (B72)
# 3: New Horizons
# 4: Boiler House

# STEP 2: CHOOSE ROBOT TARGET LOCATION:
target_location = 4
# 0: ENG Faculty (B72)
# 1: New Horizons
# 2: HAL
# 3: Monash Motorsport
# 4: ENG Lecture Theatres

# STEP 3: CHOOSE SIMULATION COMPUTER:
system_directories = 0
# 0: Samuel's Computer
# 1: Chris's Computer

###
######
#########
############
###############
##################
##################### PROCESS SYSTEM DIRECTORIES ####################
if system_directories == 0:
    base_pth = "/home/ubuntu/ws/jackal_fyp"
elif system_directories == 1:
    base_pth = "/home/chris/Documents/jackal_fyp"

# Specify file locations:
model_ext = "/src/development/resources/obj_detection/Models/ssd300_epoch6.pth.tar"
font_ext = "/src/development/resources/obj_detection/OpenSans-Regular.ttf"
remove_x_ext = "/live/remove_x.pkl"
remove_y_ext = "/live/remove_y.pkl"
map_ext = "/live/map.png"
hough_ext = "/live/hough.jpg"
pointcloud_ext = "/live/pointcloud.pickle"
pointcloud2_ext = "/live/pointcloud2.pickle"

# Full file paths:
model_pth = base_pth + model_ext
font_pth = base_pth + font_ext
remove_x_pth = base_pth + remove_x_ext
remove_y_pth = base_pth + remove_y_ext
map_pth = base_pth + map_ext
hough_pth = base_pth + hough_ext
pointcloud_pth = base_pth + pointcloud_ext
pointcloud2_pth = base_pth + pointcloud2_ext
