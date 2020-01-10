import face_recognition
from PIL import Image, ImageDraw
import time
import praw
import urllib
import yaml
import config



# detect the faces in an image and export a new image file
# with boxes around the faces
def detect_faces(image):

    # load the image file
    loaded_image = face_recognition.load_image_file(image)

    # locate all faces in the image file
    face_locations = face_recognition.face_locations(loaded_image)

    # open the image
    im = Image.open(image)

    # get drawing context
    draw = ImageDraw.Draw(im)

    if len(face_locations) != 1:
        print(str(len(face_locations)) + " faces found")
    else:
        print("1 face found")

    # iterate through face locations
    for i, rect in enumerate(face_locations):
        top, right, bottom, left = rect
        draw.rectangle((left, top, right, bottom), outline=(0,255,0), width=3)

    # clean up
    del draw

    # save new image
    im.save("output.png", "PNG")

    # wait
    time.sleep(5)

# use reddit API to download the most recent posts from
# /r/epsteinandfriends
def check_reddit():

    # get the reddit config values from the yaml file
    client_id = config.CLIENT_ID
    client_secret = config.CLIENT_SECRET
    user_agent = config.USER_AGENT

    # initialize praw
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

    # loop through the submissions
    for submission in reddit.subreddit('epsteinandfriends').new(limit=20):

        # get the url
        url = submission.url

        # download the image from the post
        if "png" in url or "jpg" in url:
            urllib.request.urlretrieve(str(submission.url), "tmp.png")
        else:
            # this post is not an image post
            continue

        # detect the faces in the photo
        detect_faces("tmp.png")


check_reddit()

