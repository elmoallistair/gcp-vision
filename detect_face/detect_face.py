# docs: https://cloud.google.com/vision/docs/detecting-faces
from google.cloud import vision
from PIL import Image, ImageDraw
import argparse
import io
import os

def detect_face(source_image, max_results):
    """Detects multiple faces within an image along with the 
    associated key facial attributes such as emotional state"""

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
        print("found {} face{}\n".format(
            len(faces), "" if len(faces) == 1 else "s")) 
    else:
        print("no face detected")
    
    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
    # Show face informations
    for counter, face in enumerate(faces):
        confidence = int(face.detection_confidence * 100)
        vertices = (["({},{})".format(vertex.x, vertex.y) 
                    for vertex in face.bounding_poly.vertices])
        print("Face {} ({}% confidence)".format(counter+1, confidence))
        print("\tBounds : {}".format(",".join(vertices)))
        print("\tLikelihood")
        print("\t\tAnger    : {}".format(likelihood_name[face.anger_likelihood]))
        print("\t\tJoy      : {}".format(likelihood_name[face.joy_likelihood]))
        print("\t\tSurprise : {}".format(likelihood_name[face.surprise_likelihood]))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message))

    return faces

def highlight_object(source_img, objects):
    """Draw polygons around the objects"""
    im = Image.open(source_img)
    draw = ImageDraw.Draw(im)
    
    for counter, object in enumerate(objects):
        # draw polygon
        box = [(vertex.x, vertex.y)
               for vertex in object.bounding_poly.vertices]        
        draw.line(box + [box[0]], width=2, fill="#00FF00")
        
        # confidence score
        confidence = int(object.detection_confidence * 100)
        draw.text((
            (object.bounding_poly.vertices)[0].x,
            (object.bounding_poly.vertices)[0].y - 15),
            "Face {} ({}%)".format(counter+1, confidence), fill="#00FF00")
    
    return im

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="perform face detection")
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

    print("Detecting face from {}...".format(
        os.path.basename(image_path)), end=" ")
    faces = detect_face(image_path, max_results)

    if faces:
        print("\nWriting output image to {}...".format(
            output_path), end=" ")
        image = highlight_object(image_path, faces)
        image.save(output_path)
        print("Done")