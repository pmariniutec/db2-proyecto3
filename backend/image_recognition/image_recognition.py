import os
import math
import face_recognition

from django.conf import settings
from rtree import index


IMAGE_DB_LOCATION = os.path.join(settings.MEDIA_ROOT, 'images')
OUTPUT_IMAGE_LOCATION = '/media/images/'


MAX_DISTANCE = 10000
NUM_IMAGES = 5


def euclidean_distance(x, y):
    if len(y) == 0:
        return MAX_DISTANCE
    return math.sqrt(sum((i - j) ** 2 for i, j in zip(x, y)))


def knn_search(query, image_idx, num_neighbors):
    return image_idx.nearest(query, num_neighbors, True)


# TODO: This should only be executed once.
#       Create en R-TREE with the encodings and store to disk.
#       The application should load the tree to memory when started, if present, else compute it.

def create_tree():
    image_files = os.listdir(IMAGE_DB_LOCATION)
    idx_name  = IMAGE_DB_LOCATION + '/' + 'image_rtree'
    idx_property = index.Property()
    idx_property.dimension = 64

    image_idx = index.Index(idx_name, properties=idx_property)
    print(image_idx.properties)
    img_id = 0
    for image_file in image_files:
        if image_file[0] != '.':
            print(f'Processing {image_file}')
            image = face_recognition.load_image_file(IMAGE_DB_LOCATION + '/' + image_file)
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                image_idx.insert(img_id, encoding[0], image_file)
                img_id += 1
    return image_idx


def load_images():
    idx_name  = IMAGE_DB_LOCATION + '/' + 'image_rtree.idx'
    try:
        file_idx = open(idx_name)
        image_idx = index.Index(idx_name)
    except IOError:
        print("File not found")
        image_idx = create_tree()

    return image_idx    


def do_query(query_image_path, num_neighbors):
    print ("QUERY IS CALLED")
    query_image = face_recognition.load_image_file(query_image_path)
    query_encoding = face_recognition.face_encodings(query_image)[0]

    images = os.listdir(IMAGE_DB_LOCATION)
    output = []
    for image in images:
        if image[0] != '.':
            output.append(image)
    # List of Enconding (vector caracteristico)
    image_idx = load_images()

    results = knn_search(query_encoding, image_idx, num_neighbors)
    print(results)
    return [{'url': OUTPUT_IMAGE_LOCATION + output[element], 'title': output[element]} for element in results]
