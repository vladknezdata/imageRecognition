def scrape_images():
    from google_images_download2.google_images_download import google_images_download
    # redirect sys.stdout to a buffer
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
                'teddy bear', 'hair drier', 'toothbrush','london','paris','new york','tour de france']
    class_names_arg = ', '.join(class_names)

    response = google_images_download.googleimagesdownload()
    args = {"keywords":class_names_arg, "limit":100,"print_urls":True}
    absolute_image_paths, errors, image_urls = response.download(args)
    # print(image_urls)
    # temporarily place into .csv 
    import pandas as pd
    try:
        # iterate over dict items b/c arrays of different length
        df = pd.DataFrame({ key:pd.Series(value) for key, value in image_urls.items() })
        df.to_csv('scrape_urls.csv')
    except:
        print('could not build build df/csv using image_url.items()')

    return df
