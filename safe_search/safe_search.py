from google.cloud import vision
import argparse
import io
import os

def detect_safe_search(source_image):
    """Detects explicit content 
    such as adult content or violent content within an image
    """

    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    
    # Loads the image from local
    with io.open(source_image, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Perform safe search detection
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ("UNKNOWN", "VERY_UNLIKELY", "UNLIKELY", 
                        "POSSIBLE", "LIKELY", "VERY_LIKELY")
    
    # Show the results
    print("Safe Search")
    print("Adult    : {}".format(likelihood_name[safe.adult]))
    print("Spoof    : {}".format(likelihood_name[safe.spoof]))
    print("Medical  : {}".format(likelihood_name[safe.medical]))
    print("Violence : {}".format(likelihood_name[safe.violence]))
    print("Racy     : {} ".format(likelihood_name[safe.racy]))
    print("Likeliness values are Unknown, Very Unlikely, Unlikely, Possible, Likely, and Very Likely")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(
                response.error.message))

if __name__ == '__main__':
    # Authenticating with a Service Account
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/key.json"
    
    parser = argparse.ArgumentParser(
        description='detect safesearch in an image')
    parser.add_argument("-i", "--source_image", required=True, 
        help="Source image path")

    args = vars(parser.parse_args())
    source_image = args["source_image"]

    print("Detecting SafeSearch from {}...\n".format(
        os.path.basename(source_image)))
    detect_safe_search(source_image)