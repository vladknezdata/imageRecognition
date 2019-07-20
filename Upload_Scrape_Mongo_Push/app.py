from flask import Flask, render_template, request, jsonify, redirect
import pymongo
import os
from maskImage import *
from videoToImage import videoToImage


app = Flask(__name__)
stored_object = {}
output_images = []
APP_ROOT = os.path.abspath("Upload_Scrape_Mongo_Push/")

target = os.path.join(APP_ROOT, 'static','images')
output_dir = os.path.join(APP_ROOT, 'static','output')
videos_out = os.path.join(APP_ROOT, 'static','processedVideoImage')
# output_dir = 'static/output'

if not os.path.isdir(target):
    os.mkdir(target)
else:
    print("Couldn't create upload directory: {}".format(target))
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
else:
    print("Couldn't create output directory: {}".format(output_dir))

@app.route("/")
def uploadfiles():
    output_images = ['static/output/' + img for img in os.listdir(output_dir)]
    print(output_images)
    output_videos = ['static/processedVideoImage/' + img for img in os.listdir(videos_out)]
    return render_template('upload.html', output_images=output_images, output_videos=output_videos)

@app.route('/saveimages', methods=["POST"])
def saveimages():
    model = startModel()
    for upload in request.files.getlist("file"):
        print("{} is the filename".format(upload.filename))
        filename = upload.filename
        destination = os.path.join(target, filename)
        # destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        # image_path = target + upload.filename
        # print("Save it to:", destination)
        upload.save(destination)
        file_name_root = upload.filename.split('.')[0]
        # create an output file name 
        file_output_name = file_name_root + '_output.png'
        # append file output name for later
        output_images.append(file_output_name)
        # run ML function
        output_name = os.path.join(output_dir, file_output_name)
        maskImage(destination, model, output_name)
        # os.remove(destination)
    
    return redirect("/")
    
@app.route('/savevideos', methods=['POST'])
def savevideos():
    # redirect to home page
    target = os.path.join(APP_ROOT, 'static', 'videoToImage')
    for upload in request.files.getlist("file"):
        print("{} is the filename".format(upload.filename))
        filename = upload.filename
        destination = os.path.join(target, filename)
        print("Accept incoming file:", filename)
        # image_path = 'static/videoToImage/' + upload.filename
        # print("Save it to:", destination)
        upload.save(destination)
        # file_name_root = upload.filename.split('.')[0]
        # create an output file name 
        # file_output_name = file_name_root + '_output.png'
        # append file output name for later
        # output_images.append(file_output_name)
        # run videoToImage
        videoToImage(destination)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)