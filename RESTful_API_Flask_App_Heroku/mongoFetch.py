import pymongo
def mongoFetchClasses():
    client = pymongo.MongoClient("mongodb+srv://team123:team123@evancluster-cgyva.mongodb.net/test?retryWrites=true")
    db = client.test
    collection = db.image_store

    # retrieve object based on given class
    stored_objects = collection.find() #{'classes_detected': class_to_lookup}
    # remove the id since it is not json serializable
    cleaned_objects = []
    for obj in stored_objects:
        obj.pop('_id')
        cleaned_objects.append(obj)
    # grab image url
    # image_url = stored_object['image_url']
    # print(image_url)
    # return url for use in the html page
    return cleaned_objects






