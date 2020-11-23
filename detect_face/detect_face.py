from google.cloud import vision
from PIL import Image, ImageDraw
import argparse
import io
import os

def detect_face(source_image, max_results):
    """Detects multiple faces within an image"""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image from local
    with io.open(source_image, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    # Perform face detection
    response = client.face_detection(
        image=image, max_results=max_results)
    faces = response.face_annotations
    
    # Count detected faces
    if faces:
        print("Found {} face{}".format(
            len(faces), "" if len(faces) == 1 else "s")) 
    else:
        print("No face detected")
        return None

    # Show face informations
    for counter, face in enumerate(faces):
        confidence = int(face.detection_confidence * 100)
        vertices = (["({},{})".format(vertex.x, vertex.y) 
                    for vertex in face.bounding_poly.vertices])
        print("Face {} ({}% confidence)".format(counter+1, confidence))
        print("\tBounds: {}".format(", ".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message))

    return faces

def highlight_object(source_img, objects):
    """Draw polygons around the objects."""
    im = Image.open(source_img)
    draw = ImageDraw.Draw(im)
    
    for counter, object in enumerate(objects):
        box = [(vertex.x, vertex.y)
               for vertex in object.bounding_poly.vertices]
        # draw polygon
        draw.line(box + [box[0]], width=2, fill='#00FF00')
        # confidence score
        confidence = int(object.detection_confidence * 100)
        draw.text((
            (object.bounding_poly.vertices)[0].x,
            (object.bounding_poly.vertices)[0].y - 15),
            "Face {} ({}%)".format(counter+1, confidence), fill='#00FF00')
    
    return im

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="detects multiple faces within an image")
    parser.add_argument("-i", "--image_path", required=True, 
        help="Source image path")
    parser.add_argument("-o", "--output_path", required=True,
        help="Output image path")
    parser.add_argument("-r", "--max_results", default=5, type=int,
        help="Max output results, default is 5")

    args = vars(parser.parse_args())
    image_path = args["image_path"]
    output_path = args["output_path"]
    max_results = args["max_results"]

    print("Detecting face from {}...\n".format(
        os.path.basename(image_path)))
    faces = detect_face(image_path, max_results)

    if faces:
        print("\nWriting output image to {}...".format(
            output_path), end=" ")
        image = highlight_object(image_path, faces)
        image.save(output_path)
        print("Done")
