import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

import anki_vector


def say(item):
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        print("Say 'Hello World'...")
        robot.say_text(item)

def getAnalysis():
    client = vision.ImageAnnotatorClient()
    file_name = os.path.join(
        os.path.dirname(__file__),
        '../face_images/target.bmp')
    
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('labels:')
    if len(labels) == 0:
        say('I don\'t know what this is about.')
    elif len(labels) == 1:
        say('I think this may be about {0}'.format(labels[0].description))
    else:
        say('This looks like {0} or {1}'.format(labels[0].description, labels[1].description))

def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(enable_camera_feed=True) as robot:
        
        
        #robot.motors.set_head_motor(-5.0)
        robot.motors.set_lift_motor(-5.0)
        if len(robot.photos.photo_info) == 0:
            print('\n\nNo photos found on Vector. Ask him to take a photo first by saying, "Hey Vector! Take a photo."\n\n')
            return
        else:
            photo = robot.photos.photo_info[len(robot.photos.photo_info) - 1]
            print(f"Opening photo {photo.photo_id}")
            val = robot.photos.get_photo(photo.photo_id)
            image = robot.camera.latest_image #Image.open(io.BytesIO(val.image))
            image.save("../face_images/target.bmp")
            getAnalysis()


if __name__ == "__main__":
    main()