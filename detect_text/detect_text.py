from google.cloud import vision
from PIL import Image, ImageDraw
import argparse
import io
import os

def detect_text(source_image, max_results):
    """Detects and extracts text from image."""
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image from local
    with io.open(source_image, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(
        image=image, max_results=max_results)
    annotation = response.full_text_annotation
    texts = annotation.text

    if texts:
        print("found {} character{}\n".format(
            len(texts), "" if len(texts) == 1 else "s")) 
        print("Detected text : {}".format(repr(texts.rstrip())))
    else:
        print("no text detected")

    return annotation

def highlight_object(source_img, object):
    """Draw polygons around the objects."""
    im = Image.open(source_img)
    draw = ImageDraw.Draw(im)
    
    for block in object.pages[0].blocks:
        box = [(vertex.x, vertex.y)
               for vertex in block.bounding_box.vertices]
        draw.line(box + [box[0]], width=2, fill='#00FF00')

    return im

if __name__ == "__main__":
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="perform logo detection")
    parser.add_argument("-i", "--image_path", required=True, 
        help="source image path")
    parser.add_argument("-o", "--output_path", required=True,
        help="output image path")
    parser.add_argument("-r", "--max_results", default=5, type=int,
        help="max output results, default is 5")

    args = vars(parser.parse_args())
    image_path = args["image_path"]
    output_path = args["output_path"]
    max_results = args["max_results"]

    print("Detecting text from {}...".format(
        os.path.basename(image_path)), end=" ")
    texts = detect_text(image_path, max_results)

    if texts:
        print("\nWriting output image to {}...".format(
            output_path), end=" ")
        image = highlight_object(image_path, texts)
        image.save(output_path)
        print("Done")