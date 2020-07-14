import pickle
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

with open("/home/bob/Documents/walls.pickle", "rb") as f:
    points_list = pickle.load(f)

#print(len(points_list))
polygon = np.array([
    [0, 0],
    [-5.1, -1],
    [-5.1, 1],
    [0, 0]
])
path = mpltPath.Path(polygon)

x = []
y = []
z = []
for pt in points_list:
    if path.contains_point(pt):
        #print(pt)
        x.append(pt[0])
        y.append(pt[1])
        z.append(pt[2])

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(x, y, z)
ax.set_xlim([-5.2, 5.2])
ax.set_ylim([-5.2, 5.2])
ax.set_zlim([-0.4, 1.1])


"""
plt.scatter(x, y)
plt.scatter(x, z)
plt.axis([-5.2, 5.2, -5.2, 5.2]) 
"""
plt.show()


