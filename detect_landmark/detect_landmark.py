# https://cloud.google.com/vision/docs/detecting-landmarks
from google.cloud import vision
import argparse
import io
import os

def detect_landmark(source_image, max_results):
    """Detects popular natural and human-made structures within an image"""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image from local
    with io.open(source_image, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform landmark detection
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations
    
    # Count landmarks detected
    if landmarks:
        print("found {} landmark{}\n".format(
            len(landmarks), "" if len(landmarks) == 1 else "s")) 
    else:
        print("no landmark detected")

    # Show the results
    for landmark in landmarks:
        confidence = int(landmark.score * 100)
        vertices = (["({},{})".format(vertex.x, vertex.y) 
                    for vertex in landmark.bounding_poly.vertices])

        print("{} ({}% confidence)".format(
            landmark.description, confidence))
        print('\tBounds    : {}'.format(", ".join(vertices)))
        for location in landmark.locations:
            lat_lng = location.lat_lng
            print('\tLatitude  : {}'.format(lat_lng.latitude))
            print('\tLongitude : {}'.format(lat_lng.longitude))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="perform landmark detection")
    parser.add_argument("-i", "--image_path", required=True, 
        help="Source image path")
    parser.add_argument("-r", "--max_results", default=2, type=int,
        help="Max output results, default is 2")

    args = vars(parser.parse_args())
    image_path = args["image_path"]
    max_results = args["max_results"]

    print("Detecting landmark from {}...".format(
        os.path.basename(image_path)), end=" ")
    detect_landmark(image_path, max_results)