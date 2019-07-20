def db_push(classes_detected, scores, mask_locations, image_url, color_percentages, image_shape):
    
    import pymongo
    import pandas as pd
    import datetime
  
    client = pymongo.MongoClient("mongodb+srv://ecalzolaio:zynn4zz6@evancluster-cgyva.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.image_store

    # image_rescaled = image_rescaled.tolist()
    mask_locations = mask_locations.tolist()
    to_insert = {
        # "image_rescaled": image_rescaled,
        "classes_detected": classes_detected,
        "scores":[float(score) for score in scores],
        "mask_locations": mask_locations,
        "image_url": image_url,
        "color_percentages": color_percentages,
        "image_shape": image_shape,
        "date": datetime.datetime.now()
    }

    collection.insert_one(to_insert)


    # Issue the serverStatus command and print the results
    # serverStatusResult=db.command("serverStatus")
    # pprint(serverStatusResult)