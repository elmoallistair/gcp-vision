from google.cloud import vision
import argparse
import io
import os

def localize_objects(source_image, max_results):
    """Localize objects in the local image"""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image from local
    with open(source_image, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform object detection
    response = client.object_localization(
        image=image, max_results=max_results)
    objects = response.localized_object_annotations
    
    # Count object detected
    if objects:
        print("found {} object{}\n".format(
            len(objects), "" if len(objects) == 1 else "s"))
    else:
        print("no object detected")
    
    # Show the results
    for object in objects:
        confidence = int(object.score * 100)
        # vertices = (["({:.4f},{:.4f})".format(vertex.x, vertex.y) 
        #             for vertex in object.bounding_poly.normalized_vertices])
        print("{} ({}% confidence)".format(object.name, confidence))
        # print("\tNormalized bounds: {}".format(", ".join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="localize objects in an image")
    parser.add_argument("-i", "--source_image", required=True, 
        help="source image path")
    parser.add_argument("-r", "--max_results", default=5, type=int,
        help="Max output results, default is 5")

    args = vars(parser.parse_args())
    source_image = args["source_image"]
    max_results = args["max_results"]

    print("Detecting objects from {}...".format(
        os.path.basename(source_image)), end=" ")
    localize_objects(source_image, max_results)