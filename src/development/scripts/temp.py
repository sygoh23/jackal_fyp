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
#import cv2

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

with open('/home/chris/Documents/pointcloud.pickle', 'rb') as f:
    pointcloud = pickle.load(f)

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

fig = plt.figure(facecolor='k')
ax = fig.add_subplot(1, 1, 1) # nrows, ncols, index
ax.scatter(x, y, facecolors='none', edgecolors='w')
plt.axis('off')
fig.savefig('/home/chris/Documents/test.jpg', facecolor=fig.get_facecolor(), edgecolor='none')
plt.show()

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

#model = KMeans(n_clusters=2)
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

"""
img = plt.imshow(dataset, interpolation='nearest')
img.set_cmap('hot')
plt.axis('off')
plt.show()
"""

"""
fig = plt.figure(frameon=False)
fig.set_size_inches(w,h)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(your_image, aspect='auto')
fig.savefig("test.jpg", dpi)
"""
