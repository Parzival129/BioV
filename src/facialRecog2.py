import math
from sklearn import neighbors
import os
import os.path
import pickle
import boto3
import botocore
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import time
import cv2
import sys

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BUCKET_NAME = 'bioauthfacedb2'
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

def faceRegistered(obj: str) -> bool:
    '''
    Checks if a face with a certain name has been registered already and returns true or false
    Ival: obj: str
    Rval: bool
    '''
    sys.path.append("/tempImageCache/model/")
    try:
        s3_resource.Object(BUCKET_NAME, obj).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
    else:
        return True

def downloadFace(obj: str):
    '''
    Takes hashed name and downloads the face with that name from the DB
    Ival: obj: str
    Rval: None
    '''
    if faceRegistered(obj):
        with open('tempImageCache/model/' + obj, 'wb') as f:
            s3_client.download_fileobj(BUCKET_NAME, obj, f)
        print(f"Successfully downloaded face for obj: {obj}")
        return True
    else:
        print("Error occured! Could not find face in DB")
        return False

def takephotos(path: str):
    '''
    Takes photo from device camera and stores it in the inputed path
    Ival: path: str
    Rval: None
    '''
    print("1")
    time.sleep(0.8)
    print("2")
    time.sleep(0.8)
    print("3")
    time.sleep(0.8)
    print("CHEESE!")

    if sys.platform.startswith("darwin") or sys.platform.startswith("win32"):
        camera = cv2.VideoCapture(0)
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path,image)
    else:

        store = os.system(f"fswebcam -r 1080x970 --jpeg 100 -D 1 --no-banner {path}")
        #os.system(shlex.quote(f"fswebcam -r 1080x970 --jpeg 100 -D 1 --no-banner {path}"))

    print("1")
    time.sleep(0.8)
    print("2")
    time.sleep(0.8)
    print("3")
    time.sleep(0.8)
    print("CHEESE!")

    if sys.platform.startswith("darwin") or sys.platform.startswith("win32"):
        camera = cv2.VideoCapture(0)
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path.replace('temp.jpg', 'othertemp.jpeg'),image)
        cv2.destroyAllWindows()
    else:

        store = os.system(f"fswebcam -r 1080x970 --jpeg 100 -D 1 --no-banner {path.replace('temp.jpg', 'othertemp.jpg')}")
        #os.system(shlex.quote(f"fswebcam -r 1080x970 --jpeg 100 -D 1 --no-banner {path.replace('temp.jpg', 'othertemp.jpg')}"))
def takephoto(path: str):
    '''
    Takes photo from device camera and stores it in the inputed path
    Ival: path: str
    Rval: None
    '''
    print("1")
    time.sleep(0.8)
    print("2")
    time.sleep(0.8)
    print("3")
    time.sleep(0.8)
    print("CHEESE!")

    if sys.platform.startswith("darwin") or sys.platform.startswith("win32"):
        camera = cv2.VideoCapture(0)
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path,image)
    else:

        store = os.system(f"fswebcam -r 1080x970 --jpeg 100 -D 1 --no-banner {path}")
        #os.system(shlex.quote(f"fswebcam -r 1080x970 --jpeg 100 -D 1 --no-banner {path}"))
def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False, amount=3000):
    """
     Structure:
        <train_dir>/
        ├── <person1>/
        │   ├── <somename1>.jpeg
        │   ├── <somename2>.jpeg
        │   ├── ...
        ├── <person2>/
        │   ├── <somename1>.jpeg
        │   └── <somename2>.jpeg
        └── ...
    """
    X = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                    if ((amount - 1) - 1) == 1 or ((amount - 1) - 1) == 0:
                        return False

            else:
                # Add face encoding for current image to the training set
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    for f in os.listdir('tempImageCache/new/person/'):
        os.remove(os.path.join('tempImageCache/new/person/', f))
    return knn_clf


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    """
    predicting faces in an image using a pre-made model
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    percentage = float(face_distance_to_conf(closest_distances[0][0][0]))
    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, percentage) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    '''
    conversion function for getting confidance percentage
    '''
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

def createModel(hashname):
    '''
    Creates a model based off a number of training images
    '''
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    takephotos('tempImageCache/new/person/temp.jpg')

    print("Training KNN classifier...")
    classifier = train("tempImageCache/new", model_save_path=f"tempImageCache/model/{hashname}.clf", n_neighbors=2, verbose=True)
    print("Training complete!")

def create(hashname, picspath):
    '''
    also creates a model though without taking photos
    '''
    print("Training KNN classifier...")
    try:
        classifier = train(picspath, model_save_path=f"testimgs/person/person/{hashname}.clf", n_neighbors=2, verbose=True)
        if classifier == False:
            return False
    except Exception as e:
        return False
    print("Training complete!")
    return True

def checkFace(hashedname):
    '''
    Checks the face of a face with model
    '''
    takephoto('tempImageCache/new/temp.jpg')
    predictions = predict('tempImageCache/new/temp.jpg', model_path=f"tempImageCache/model/{hashedname}")
    os.remove(f"tempImageCache/model/{hashedname}")
    # Print results on the console
    for name, percentage in predictions:
        if name != "person":
            return False

        print("Confidence %: " + str(percentage * 100.00))
        return True

def comparemodel2img(path, model, personname):
    '''
    comapres a model to an image
    '''
    predictions = predict(path, model_path=model)
    for name, percentage in predictions:
        if name != personname:
            print("Confidence %: " + str(percentage))
            return False
        print("Confidance %: " + str(percentage))
        return True
    return "somethin went"

def comparemodel2img2(path, model, distance=0.6):
    '''
    comapres a model to an image
    '''
    predictions = predict(path, model_path=model, distance_threshold=distance)
    for name, percentage in predictions:
        # if its a tuple, then its detecting a face just not matching
        if type(percentage) != tuple:
            return True

    return False

def compare2(hashedname):
    '''
    compares more stuff
    '''
    if downloadFace(hashedname) == False:
        return False
    return checkFace(hashedname)

