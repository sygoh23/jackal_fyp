# https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection

"""
MIT License

Copyright (c) 2019 Sagar Vinodababu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from torchvision import transforms
from obj_utils import *
from PIL import Image, ImageDraw, ImageFont
import sys

##########################
##### Set paths here #####
##########################
img_pth = "/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/Images/All/0005.jpg"
model_pth = "/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/Models/ssd300_epoch6.pth.tar"
font_pth = "/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/OpenSans-Regular.ttf"

# Check filepaths
if not os.path.exists(img_pth):
    print("\n[WARNING]: Error accessing [%s]\nChange path variable: 'font_pth'\n" % img_pth)
    sys.exit()

if not os.path.exists(model_pth):
    print("\n[WARNING]: Error accessing [%s]\nChange path variable: 'model_pth'\nPre-trained model can be downloaded at [https://drive.google.com/file/d/1bvJfF6r_zYl2xZEpYXxgb7jLQHFZ01Qe/view]\n" % model_pth)
    sys.exit()

if not os.path.exists(font_pth):
    print("\n[WARNING]: Error accessing [%s]\nChange path variable: 'font_pth'\n" % font_pth)
    sys.exit()

# Set device
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU found.\n")
else:
    device = torch.device("cpu")
    print("Using CPU.\n")

# Load model
print("Model found at [%s]\n" % model_pth)
checkpoint = torch.load(model_pth)
start_epoch = checkpoint['epoch'] + 1
print("\nLoaded weights from epoch %d.\n" % start_epoch)
model = checkpoint['model']
model = model.to(device)
model.eval()

# Transforms
resize = transforms.Resize((300, 300))
to_tensor = transforms.ToTensor()
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])


def detect(original_image, min_score, max_overlap, top_k, suppress=None):
    """
    Detect objects in an image with a trained SSD300, and visualize the results.
    :param original_image: image, a PIL Image
    :param min_score: minimum threshold for a detected box to be considered a match for a certain class
    :param max_overlap: maximum overlap two boxes can have so that the one with the lower score is not suppressed via Non-Maximum Suppression (NMS)
    :param top_k: if there are a lot of resulting detection across all classes, keep only the top 'k'
    :param suppress: classes that you know for sure cannot be in the image or you do not want in the image, a list
    :return: annotated image, a PIL Image
    """

    # Transform
    image = normalize(to_tensor(resize(original_image)))

    # Move to default device
    image = image.to(device)

    # Forward prop.
    predicted_locs, predicted_scores = model(image.unsqueeze(0))

    # Detect objects in SSD output
    det_boxes, det_labels, det_scores = model.detect_objects(
        predicted_locs,
        predicted_scores,
        min_score=min_score,
        max_overlap=max_overlap, top_k=top_k
    )

    # Move detections to the CPU
    det_boxes = det_boxes[0].to('cpu')

    # Transform to original image dimensions
    original_dims = torch.FloatTensor([
        original_image.width,
        original_image.height,
        original_image.width,
        original_image.height
    ]).unsqueeze(0)
    det_boxes = det_boxes * original_dims

    # Decode class integer labels
    det_labels = [rev_label_map[l] for l in det_labels[0].to('cpu').tolist()]

    print("*************** DETECTED: ***************")

    # If no objects found, the detected labels will be set to ['0.'], i.e. ['background'] in SSD300.detect_objects() in model.py
    if det_labels == ['background']:
        # Just return original image
        print("==> nothing")
        print("*****************************************\n")
        return original_image

    # Annotate
    annotated_image = original_image
    draw = ImageDraw.Draw(annotated_image)
    font = ImageFont.truetype(font_pth, 15)

    # Suppress specific classes, if needed
    for i in range(det_boxes.size(0)):
        if suppress is not None:
            if det_labels[i] in suppress:
                continue

        # Boxes
        box_location = det_boxes[i].tolist()
        draw.rectangle(xy=box_location, outline=label_color_map[det_labels[i]])
        draw.rectangle(xy=[l + 1. for l in box_location], outline=label_color_map[
            det_labels[i]])  # a second rectangle at an offset of 1 pixel to increase line thickness
        # draw.rectangle(xy=[l + 2. for l in box_location], outline=label_color_map[
        #     det_labels[i]])  # a third rectangle at an offset of 1 pixel to increase line thickness
        # draw.rectangle(xy=[l + 3. for l in box_location], outline=label_color_map[
        #     det_labels[i]])  # a fourth rectangle at an offset of 1 pixel to increase line thickness

        # Text
        text_size = font.getsize(det_labels[i].upper())
        text_location = [box_location[0] + 2., box_location[1] - text_size[1]]
        textbox_location = [box_location[0], box_location[1] - text_size[1], box_location[0] + text_size[0] + 4.,
                            box_location[1]]
        draw.rectangle(xy=textbox_location, fill=label_color_map[det_labels[i]])
        draw.text(xy=text_location, text=det_labels[i].upper(), fill='white',
                  font=font)

        print("==> %s" % det_labels[i].lower())

    print("*****************************************\n")
    del draw

    return annotated_image


if __name__ == '__main__':
    original_image = Image.open(img_pth, mode='r')
    original_image = original_image.convert('RGB')
    detect(original_image, min_score=0.2, max_overlap=0.5, top_k=200).show()