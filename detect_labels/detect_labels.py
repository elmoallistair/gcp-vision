from google.cloud import vision
import argparse
import io
import os

def detect_labels(source_image, max_results):
    """Detects labels such as general objects, locations, 
    activities, products, and more in an image"""
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    # Loads the image from local
    with io.open(source_image, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform label detection
    response = client.label_detection(
        image=image, max_results=max_results)
    labels = response.label_annotations

    # Count labels detected
    if labels:
        print("Found {} label{}".format(
            len(labels), "" if len(labels) == 1 else "s")) 
    else:
        print("No label detected")

    # Show the results
    for label in labels:
        description = label.description
        confidence = int(label.score * 100)
        print("{} ({}% confidence)".format(description, confidence))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message))

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(description='detect labels in an image')
    parser.add_argument("-i", "--source_image", required=True, 
        help="Source image path")
    parser.add_argument("-r", "--max_results", default=5, type=int,
        help="Max output results, default is 5")
    args = vars(parser.parse_args())
    
    source_image = args["source_image"]
    max_results = args["max_results"]

    print("Detecting labels from {}...\n".format(
        os.path.basename(source_image)))
    detect_labels(source_image, max_results)