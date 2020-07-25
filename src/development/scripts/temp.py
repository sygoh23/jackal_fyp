"""
Temporary file for testing ideas. Not used by the main code and will be deleted at some point.
"""

from obj_utils import *
from PIL import Image, ImageDraw
import torch

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