"""
Temporary file for testing ideas. Not used by the main code and will be deleted at some point.
"""

#from obj_utils import *
#from PIL import Image, ImageDraw
#import torch
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, Birch, DBSCAN, KMeans
import numpy as np
import cv2
from PIL import Image
import math
#from utils import get_distance

"""
old = Image.open("/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/0001.jpg")
old_box = torch.tensor([[300, 180, 600, 490]])
new, new_box = resize(image=old, boxes=old_box, return_percent_coords=False)

draw_old = ImageDraw.Draw(old)
draw_old.rectangle(((300, 180), (600, 490)), outline="red")
old.show()

draw_new = ImageDraw.Draw(new)
draw_new.rectangle(((new_box[0][0], new_box[0][1]), (new_box[0][2], new_box[0][3])), outline="red")
new.show()
"""

"""
# Label map
voc_labels = ('entrance')
label_map = {k: v + 1 for v, k in enumerate(voc_labels)}    # {"aeroplane": 1, "bicycle": 2, ...}
label_map['background'] = 0
label_map = {"background": 0, "entrance": 1}
rev_label_map = {v: k for k, v in label_map.items()}  # {1: "aeroplane", 2: "bicycle", ...}

# Color map for bounding boxes of detected objects from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
distinct_colors = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231', '#911eb4', '#46f0f0', '#f032e6',
                   '#d2f53c', '#fabebe', '#008080', '#000080', '#aa6e28', '#fffac8', '#800000', '#aaffc3', '#808000',
                   '#ffd8b1', '#e6beff', '#808080', '#FFFFFF']
label_color_map = {k: distinct_colors[i] for i, k in enumerate(label_map.keys())}   # {"aeroplane": '#e6194b', "bicycle": '#3cb44, ...}

obj = {'boxes': [[0, 1, 2, 3], [4, 5, 6, 7]], 'labels': [1, 1], 'difficulties': [0, 0]}

decay_lr_at = [80000, 100000]
decay_lr_at = [it // (100 // 32) for it in decay_lr_at]

img_names_train = sorted(os.listdir("/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/Images/Train"))
print(img_names_train)
img_names_train.remove("README.md")  # remove readme file
print(img_names_train)
"""


with open('/home/chris/Documents/jackal_fyp/plugins/pointcloud2.pickle', 'rb') as f:
    pointcloud = pickle.load(f)

with open('/home/chris/Documents/jackal_fyp/plugins/tf_point.pickle', 'rb') as f:
    transformed_point_xy = pickle.load(f, encoding='latin1')


##########################################################################
# Point cloud filtering
##########################################################################

dataset = np.array([])
x = []
y = []
z = []
first = True
for point in pointcloud:
    if point[2] > 0.5:
        if first:
            dataset = np.array([point[0], point[1]])
            first = False
        else:
            new_point = np.array([point[0], point[1]])
            dataset = np.vstack((dataset, new_point))

        x.append(point[0])
        y.append(point[1])
        #z.append(point[2])


#fig = plt.figure()
#ax = Axes3D(fig)
#ax.scatter(x, y, z)

"""
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.scatter(x, y)
ax.scatter(0, 0, color='g', s=100)
ax.scatter(transformed_point_xy[0], transformed_point_xy[1], color='r', s=100)
"""

#ax.scatter(x, y, color='w', marker=',')
#plt.axis('off')
#fig.savefig('/home/chris/Documents/test4.jpg', facecolor=fig.get_facecolor(), edgecolor='none')
#plt.show()


#model = AffinityPropagation(damping=0.9)
#model.fit(dataset)
#yhat = model.predict(dataset)

#model = AgglomerativeClustering(n_clusters=3)
#yhat = model.fit_predict(dataset)

#model = Birch(threshold=0.01, n_clusters=3)
#model.fit(dataset)
#yhat = model.predict(dataset)

#model = DBSCAN(eps=0.60, min_samples=9)
#yhat = model.fit_predict(dataset)

#model = KMeans(n_clusters=3)
#model.fit(dataset)
#yhat = model.predict(dataset)

"""
clusters = np.unique(yhat)
for cluster in clusters:
	# get row indexes for samples with this cluster
	row_ix = np.where(yhat == cluster)
	plt.scatter(dataset[row_ix, 0], dataset[row_ix, 1])

plt.show()
"""


##########################################################################
# Create image
##########################################################################

# Convert to numpy array
x_min = min(x)  # -67.5
y_min = min(y)  # -100.6
w = int(max(x) - x_min) + 2     # max x = 61.5
h = int(max(y) - y_min) + 2     # max y = 95.7
c = 3

"""
print()
print(x_min, y_min, max(x), max(y), w, h)
print()
"""

grid = np.zeros((w, h, c), dtype=np.uint8)

for pt_x, pt_y in zip(x, y):
    """
    print("\nBefore translation:")
    print(pt_x, pt_y)
    print()
    """

    """
    if (x_min <= 0) and (y_min <= 0):
        pt_x += abs(x_min)
        pt_y += abs(y_min)

    elif x_min <= 0:
        pt_x += abs(x_min)

    elif y_min <= 0:
        pt_y += abs(y_min)
    """

    """
    print("\nAfter translation:")
    print(pt_x, pt_y)
    print()
    """

    # Translate
    pt_x += abs(x_min)
    pt_y += abs(y_min)

    grid[int(pt_x), int(pt_y), :] = [255, 255, 255]
    

##########################################################################
# Hough transform
##########################################################################

# No rotation
img = grid

# Rotation
#img = np.rot90(m=grid, k=1)
#img = img.copy()
#img = Image.fromarray(grid, 'RGB').show()



# Read image 
#img = cv2.imread('/home/chris/Documents/test4.jpg', cv2.IMREAD_COLOR)
#cv2.imshow("Initial", grid)
#cv2.waitKey()


# Convert the image to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Gray", gray)
#cv2.waitKey()

# Find the edges in the image using canny detector
edges = cv2.Canny(gray, 50, 200)
#cv2.imshow("Edges", gray)
#cv2.waitKey()


# Detect points that form a line
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=40, minLineLength=20, maxLineGap=70)
#print(lines)

# Draw lines on the image
if lines is not None:
    lines_list = []     # [np.array[x1, y1, x2, y2], ...]
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
        lines_list.append(line[0])

    # Show result
    cv2.imwrite("/home/chris/Documents/HoughTransform.jpg", img)
    #cv2.imshow("Result Image", img)
    #cv2.waitKey()

else:
    print("No lines found")


##########################################################################
# Reverse transform
##########################################################################

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

#print("\nImage space:")
#print(lines_list)

lines_tuples = []   # [[(x1, y1), (x2, y2)], ...]
for line in lines_list:
    # Rotate back
    #start_transformed = rotate(origin=(abs(y_min), abs(x_min)), point=(line[0], line[1]), angle=math.radians(90))
    start_transformed = (line[0], line[1])

    # Translate back
    start_transformed = (
        start_transformed[0] - abs(y_min),
        start_transformed[1] - abs(x_min)
    )
    
    # Reverse coords
    start_transformed = (start_transformed[1], start_transformed[0])

    # Rotate back
    #end_transformed = rotate(origin=(abs(y_min), abs(x_min)), point=(line[2], line[3]), angle=math.radians(90))
    end_transformed = (line[2], line[3])

    # Translate back
    end_transformed = (
        end_transformed[0] - abs(y_min),
        end_transformed[1] - abs(x_min)
    )

    # Reverse coords
    end_transformed = (end_transformed[1], end_transformed[0])

    lines_tuples.append([start_transformed, end_transformed])

#print("\nTransformed back")
#print(lines_tuples)

"""
print()
print(lines_tuples)

print("\nImage space:")
print(lines_list)

for line in lines_list:
    line -= np.array([abs(x_min), abs(y_min), abs(x_min), abs(y_min)], dtype='int32')

print("\nRobot frame:")
print(lines_list)
"""


##########################################################################
# Duplicates
##########################################################################

#for line in lines_tuples:



##########################################################################
# Analysis
##########################################################################

def get_distance(x1, x2, y1, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

step = 2
start_offset = 30 # How far before start point to start
end_offset = 30  # How far after end point to finish
endpoint_threshold = 1.1  # How close to the endpoint for the iteration to stop. Should be > step/2
min_dist = 999999999    # Init to large number
best_line = [(8725, 8725), (8725, 8725)]
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index

for line in lines_tuples:
    # [(x1, y1), (x2, y2)]

    # Generate x/y points that lie on the line
    start = line[0] # (x1, y1)
    end = line[1]   # (x2, y2)
    line_dist = get_distance(start[0], end[0], start[1], end[1])
    #print('Line length: {}'.format(line_dist))

    # Unit vector in direction of target
    unit_x = (end[0] - start[0])/line_dist
    unit_y = (end[1] - start[1])/line_dist
    #print('Unit x: {}'.format(unit_x))
    #print('Unit y: {}'.format(unit_y))

    current_pt = (start[0] - start_offset*unit_x, start[1] - start_offset*unit_y)
    end_pt = (end[0] + end_offset*unit_x, end[1] + end_offset*unit_y)
    #x_points = [start[0]]
    #y_points = [start[1]]

    
    while get_distance(current_pt[0], end_pt[0], current_pt[1], end_pt[1]) > endpoint_threshold:
        # Get distance to target
        target_dist = get_distance(current_pt[0], transformed_point_xy[0], current_pt[1], transformed_point_xy[1])
        #print('Current point: {}'.format(current_pt))
        #print('Dist to target point: {}'.format(target_dist))
        #print('Current min distance: {}'.format(min_dist))

        if target_dist < min_dist:
            min_dist = target_dist
            best_line = line
            #print('New best line')

        ax.clear()

        # Velodyne points
        ax.scatter(x, y, color='b', s=10)

        # Target point
        ax.scatter(transformed_point_xy[0], transformed_point_xy[1], color='r', s=100)

        # Detected lines
        for endpoints in lines_tuples:
            x_pts = [endpoints[0][0], endpoints[1][0]]
            y_pts = [endpoints[0][1], endpoints[1][1]]
            ax.plot(x_pts, y_pts, linewidth=2)
        
        # Best line
        ax.plot([best_line[0][0], best_line[1][0]], [best_line[0][1], best_line[1][1]], linewidth=4, color='#48f542')

        # Current point
        ax.scatter(current_pt[0], current_pt[1], color='g', s=120)

        plt.pause(0.1)

        
        # Generate next point
        current_pt = (current_pt[0] + step*unit_x, current_pt[1] + step*unit_y)
        #x_points.append(current_pt[0])
        #y_points.append(current_pt[1])
    

#plt.show()





"""
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.scatter(x, y)
ax.scatter(0, 0, color='g', s=100)
ax.scatter(transformed_point_xy[0], transformed_point_xy[1], color='r', s=100)

for line in lines_tuples:
    x_pts = [line[0][0], line[1][0]]
    y_pts = [line[0][1], line[1][1]]
    ax.plot(x_pts, y_pts)

plt.show()
"""