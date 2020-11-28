from google.cloud import vision
import argparse
import io
import os

def detect_properties(source_image):
    """Detects general attributes of the image, 
    such as dominant color"""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    # Loads the image from local
    with io.open(source_image, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform properties detection
    response = client.image_properties(image=image)
    properties = response.image_properties_annotation
    
    # Store color to dict
    sum_frac = 0
    colors = {}
    for color in properties.dominant_colors.colors:
        coverage = color.pixel_fraction * 100
        col = color.color
        rgb = tuple(map(int, (col.red, col.green, col.blue)))
        hex = '#%02x%02x%02x' % rgb
        colors[hex] = coverage
        sum_frac += coverage

    # Sort by color coverage
    sort_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
    
    # Show the result
    print('Dominant Colors:')
    for color in sort_colors:
        hex, coverage = color
        print("{} ({:.1f}% coverage)".format(hex, coverage))
    if 1-sum_frac > 0:
        print("Unknown ({:.1f}% coverage)".format(1-sum_frac))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description="detects image properties in an image")
    parser.add_argument("-i", "--source_image", required=True, 
        help="source image path")

    args = vars(parser.parse_args())
    source_image = args["source_image"]

    print("Detecting image properties from {}...\n".format(
        os.path.basename(source_image)))
    detect_properties(source_image)