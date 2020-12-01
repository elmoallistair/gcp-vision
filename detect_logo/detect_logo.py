# docs: https://cloud.google.com/vision/docs/detecting-logos
from google.cloud import vision_v1 as vision
from PIL import Image, ImageDraw
import argparse
import os
import io

def detect_logo(source_image, max_results):
    """Detects popular product logos within an image"""

    client = vision.ImageAnnotatorClient()

    with io.open(source_image, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.logo_detection(image=image)
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    logos = response.logo_annotations

    # Count detected logo
    if logos:
        print("found {} logo{}\n".format(
            len(logos), "" if len(logos) == 1 else "s")) 
    else:
        print("no logo detected.")

    for logo in logos:
        confidence = int(logo.score * 100)
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in logo.bounding_poly.vertices])
        print("{} ({}% confidence)".format(logo.description, confidence))
        print("\tBounds : {}".format(','.join(vertices))) 

    return logos

def highlight_object(source_img, objects):
    """Draw polygons around the objects."""
    im = Image.open(source_img)
    draw = ImageDraw.Draw(im)
    
    for object in objects:
        name = object.score
        confidence = int(object.score * 100)
        vertices = [(vertex.x, vertex.y)
               for vertex in object.bounding_poly.vertices]
        draw.line(vertices + [vertices[0]], width=2, fill='#00FF00')
        draw.text((
            (object.bounding_poly.vertices)[0].x, 
            (object.bounding_poly.vertices)[0].y - 15),
            str("{} ({}%)".format(name, confidence)), fill="#00FF00")

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
    parser.add_argument("-r", "--max_results", default=2, type=int,
        help="max output results, default is 2")

    args = vars(parser.parse_args())
    image_path = args["image_path"]
    output_path = args["output_path"]
    max_results = args["max_results"]

    print("Detecting logo from {}...".format(
        os.path.basename(image_path)), end=" ")
    logos = detect_logo(image_path, max_results)

    if logos:
        print("\nWriting output image to {}...".format(
            output_path), end=" ")
        image = highlight_object(image_path, logos)
        image.save(output_path)
        print("Done")