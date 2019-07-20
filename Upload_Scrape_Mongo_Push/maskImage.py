def startModel():
    import os
    import sys
    ROOT_DIR = os.path.abspath("Upload_Scrape_Mongo_Push/Mask_RCNN")
    sys.path.append(ROOT_DIR)
    import mrcnn.model as modellib
    
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")
    sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
    import coco
    class InferenceConfig(coco.CocoConfig):
        # Set batch size to 1 since we'll be running inference on
        # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    config.display()
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
    return model

def maskImage(image_path, model, file_name = ''):
    import os
    import sys
    import random
    import math
    import numpy as np
    import skimage.io
    import matplotlib
    import matplotlib.pyplot as plt

    # Root directory of the project
    ROOT_DIR = os.path.abspath("Upload_Scrape_Mongo_Push/Mask_RCNN")

    # Import Mask RCNN
    sys.path.append(ROOT_DIR)  # To find local version of the library
    from Mask_RCNN.mrcnn import utils
    from Mask_RCNN.mrcnn import visualize
    # import colorPercentage function
    from colorDetect import colorPercentage
    # Import COCO config
    sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
    import coco

    # Directory to save logs and trained model

    # Local path to trained weights file
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    # Download COCO trained weights from Releases if needed
    if not os.path.exists(COCO_MODEL_PATH):
        utils.download_trained_weights(COCO_MODEL_PATH)
    # Create model object in inference mode.

    # Load weights trained on MS-COCO
    try:
        model.load_weights(COCO_MODEL_PATH, by_name=True)
    except:
        print('already loaded')
    # COCO Class names
    # Index of the class in the list is its ID. For example, to get ID of
    # the teddy bear class, use: class_names.index('teddy bear')
    class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                'kite', 'baseball bat', 'baseball glove', 'skateboard',
                'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                'teddy bear', 'hair drier', 'toothbrush']
                
    #%%
    # Load a random image from the images folder
    # file_names = next(os.walk(IMAGE_DIR))[2]
    # image = skimage.io.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
    image = skimage.io.imread(image_path)
    # Run detection
    results = model.detect([image], verbose=1)
    # [image]
    # Visualize results

    r = results[0]
    color_percentages = colorPercentage(image)
    if file_name:
        visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                    class_names, r['scores'], file_name=file_name)

    # get english-word for each index in r['class_ids']
    classes_detected = [class_names[ind] for ind in r['class_ids']]
    # read in the outputted file as a matrix so that it can be uploaded to mongoDB
    # output_image_matrix = skimage.io.imread(output_name)
    # get scores for processed image
    scores = r['scores']
    mask_locations = r['rois']
    image_shape = list(image.shape[0:2])
    # tuple to return from this function
    # IMAGE is the matrix of the image, see above
    # from skimage.transform import rescale, resize, downscale_local_mean
    # image_rescaled = rescale(image, 1.0 / 40.0, anti_aliasing=False)
    to_return = (classes_detected, scores, mask_locations, color_percentages, image_shape)    

    return to_return
