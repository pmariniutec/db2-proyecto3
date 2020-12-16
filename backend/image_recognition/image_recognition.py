import os
import math
import face_recognition
import time

from django.conf import settings


IMAGE_DB_LOCATION = os.path.join(settings.MEDIA_ROOT, 'images')
OUTPUT_IMAGE_LOCATION = '/media/images/'


MAX_DISTANCE = 10000
NUM_IMAGES = 25


def euclidean_distance(x, y):
    if len(y) == 0:
        return MAX_DISTANCE
    return math.sqrt(sum((i - j) ** 2 for i, j in zip(x, y)))


def knn_search(query, data, num_neighbors):
    start = time.time()
    results = []
    for index, image_encoding in enumerate(data):
        distance = euclidean_distance(query, image_encoding)
        results.append((index, distance))
    results.sort(key=lambda x: x[1])
    results = [i[0] for i in results]
    end = time.time()
    print(f"[Images: {NUM_IMAGES}] Time: {end - start}")
    return results[:num_neighbors]


# TODO: This should only be executed once.
#       Create en R-TREE with the encodings and store to disk.
#       The application should load the tree to memory when started, if present, else compute it.
def load_images():
    image_files = os.listdir(IMAGE_DB_LOCATION)
    images = []
    for image_file in image_files[:NUM_IMAGES]:
        if image_file[0] != '.':
            image = face_recognition.load_image_file(IMAGE_DB_LOCATION + '/' + image_file)
            encoding = face_recognition.face_encodings(image)
            if len(encoding) > 0:
                images.append(encoding[0])
            else:
                images.append([])
    return images


def do_query(query_image_path, num_neighbors):
    query_image = face_recognition.load_image_file(query_image_path)
    query_encoding = face_recognition.face_encodings(query_image)[0]

    images = os.listdir(IMAGE_DB_LOCATION)
    output = []
    for image in images:
        if image[0] != '.':
            output.append(image)
    image_data = load_images()

    results = knn_search(query_encoding, image_data, num_neighbors)
    return [{'url': OUTPUT_IMAGE_LOCATION + output[element], 'title': output[element]} for element in results]
