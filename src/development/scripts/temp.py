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

# Convert to numpy array
x_min = min(x)
y_min = min(y)
w = int(max(x) - x_min) + 2
h = int(max(y) - y_min) + 2
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

    
    pt_x += abs(x_min)
    pt_y += abs(y_min)
    grid[int(pt_x), int(pt_y), :] = [255, 255, 255]
    

    #grid[1, 100, :] = [255, 255, 255]

img = np.rot90(m=grid, k=1)
img = img.copy()
#img = Image.fromarray(grid, 'RGB').show()

#grid = np.rot90(m=grid, k=-1)  # k = -1 undoes the rotation


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

# Draw lines on the image
if lines is not None:
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

    # Show result
    cv2.imwrite("/home/chris/Documents/HoughTransform.jpg", img)
    cv2.imshow("Result Image", img)
    cv2.waitKey()
else:
    print("No lines found")

