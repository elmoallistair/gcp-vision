# docs: https://cloud.google.com/vision/docs/detecting-web
from google.cloud import vision
import argparse
import io
import os

def detect_web(source_image, max_results):
    """Detects Web references to an image"""
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    # Loads the image from local
    with io.open(source_image, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform web detection
    response = client.web_detection(
        image=image, max_results=max_results)
    annotations = response.web_detection

    # Best label
    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print("best guess label: {}".format(label.label))

    # Web Entities
    if annotations.web_entities:
        print("\nWeb entities found:")
        for entity in annotations.web_entities:
            if entity.description:
                print("\t{} (Score: {:.2f})".format(
                    entity.description, entity.score))
    
    # Full matching images
    if annotations.full_matching_images:
        print("\nFull Matches found:")
        for image in annotations.full_matching_images:
            print("\tUrl: {}".format(image.url))

    # Partial matching images
    if annotations.partial_matching_images:
        print("\nPartial Matches found:")
        for image in annotations.partial_matching_images:
            print("\tUrl: {}".format(image.url))

    # Pages with matching images
    if annotations.pages_with_matching_images:
        print("\nPages with matching images:")
        for page in annotations.pages_with_matching_images:
            print("\tUrl: {}".format(page.url))

    # Similiar images
    if annotations.visually_similar_images:
        print("\nSimilar images found:")
        for image in annotations.visually_similar_images:
            print("\tUrl: {}".format(image.url))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message))

if __name__ == "__main__":
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="perforn web entities and pages detection")
    parser.add_argument("-i", "--source_image", required=True, 
        help="source image path")
    parser.add_argument("-r", "--max_results", default=5, type=int,
        help="max output results, default is 5")
    args = vars(parser.parse_args())
    
    source_image = args["source_image"]
    max_results = args["max_results"]

    print("Detecting web entities and pages from {}...".format(
        os.path.basename(source_image)), end=" ")
    detect_web(source_image, max_results)