#!/usr/bin/env python

"""
Used to start the image processing node.
Reads image data from a ROS topic, performs conversions, and sends to object detection model.
"""

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import numpy as np
import PIL.Image
import obj_detect
from static_params import use_webcam


def img_converter():
    # Read image from topic
    if use_webcam:
        ros_img = rospy.wait_for_message("/usb_cam/image_raw", Image)
    else:
        ros_img = rospy.wait_for_message("/front/image_raw", Image)
        #ros_img = rospy.wait_for_message("/camera/color/image_raw", Image)     # Different topic in realsense.bag

    # Convert to cv::Mat
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(ros_img, "rgb8")
    except CvBridgeError as err:
        print(err)

    # Convert to PIL through numpy
    np_img = np.asarray(cv_image)       # dim = (H, W, C) = (rows, cols, channels), dtype = uint8
    pil_img = PIL.Image.fromarray(np_img)

    return pil_img


if __name__ == "__main__":
    try:
        rospy.init_node("image_processor", anonymous=True)

        while True:
            # Raw image
            img_raw_pil = img_converter()

            # Annotated image
            img_pred_pil = obj_detect.detect(img_raw_pil, min_score=0.2, max_overlap=0.5, top_k=200)

            # Convert to cv::Mat and display
            img_pred_cv = np.array(img_pred_pil)
            img_pred_cv = img_pred_cv[:, :, ::-1].copy()
            cv2.imshow("Image window", img_pred_cv)
            cv2.waitKey(1)
            
            #time.sleep(1)
            
    except KeyboardInterrupt:
        print("Shutting down")
    
    print('***** Finished *****')