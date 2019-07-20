import cv2
import numpy as np
import os
import sys
from maskImage import maskImage, startModel
def videoToImage(file_name):
    model = startModel()
    APP_ROOT = os.path.abspath("Upload_Scrape_Mongo_Push/")
    vid_image_dir = os.path.join(APP_ROOT,'static','videoToImage')

    print(vid_image_dir)
    if not os.path.isdir(vid_image_dir):
        os.mkdir(vid_image_dir)
    else:
        print("Couldn't create raw directory: {}".format(vid_image_dir))

    processed_video_dir = os.path.join(APP_ROOT,'static', 'processedVideoImage')

    if not os.path.isdir(processed_video_dir):
        os.mkdir(processed_video_dir)
    else:
        print("Couldn't create crop directory: {}".format(processed_video_dir))
    # def videoToFrames(video, everyNthFrame=30)
    # cap = cv2.VideoCapture(video)
    file_location = os.path.join(vid_image_dir, file_name)
    cap = cv2.VideoCapture(file_location)
    frameList = []
    currentFrame = 1
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == False:
            break
        # Saves every Nth frame as jpg file
        # if currentFrame % everyNthFrame == 0:
        if currentFrame % 30 == 0:

            name = str(currentFrame) + '.jpg'
            image_location = os.path.join(vid_image_dir, name) 
            print ('Creating...' + name)

            cv2.imwrite(image_location, frame)

            output_name = os.path.join(processed_video_dir, name)
            maskImage(image_location, model, output_name)
            # frameList.append(frame)
        # To stop duplicate images
        currentFrame += 1
        # return frameList
