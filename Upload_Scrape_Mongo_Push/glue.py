from maskImage import maskImage
from maskImage import startModel
from mongoPush import db_push
from googleImageScrape import scrape_images
import os 
import pandas as pd
from natsort import natsorted

model = startModel()
# scrape 100 images of each type 
df_urls = scrape_images()
# df_urls = pd.read_csv('scrape_urls.csv')

main_directory = os.getcwd()
downloads = os.path.join(main_directory, 'downloads')


for _, d, _ in os.walk(downloads):
    for folder in sorted(d):
        print(folder)
        current_folder = os.path.join(downloads, folder)
        print(current_folder)
        for _, _, f in os.walk(current_folder):
            for file in natsorted(f):
                try:
                    print(file)
                    # use this index embedded in the file name to prevent conflict with random, inexplicable nan values
                    index = int(file.split('.')[0]) - 1
                    current_file = os.path.join(current_folder, file)
                    # locate url in df based on folder name and index
                    img_url = df_urls[folder].iloc[index] 
                    print(img_url)
                    # return info from function
                    classes_detected, scores, mask_locations, class_percentages, image_shape = maskImage(current_file, model)
                    # pass into db
                    db_push(classes_detected, scores, mask_locations, img_url, class_percentages, image_shape)
                except:
                    print('error thrown for file: ', file)
            
