from flask import Flask

# import tensorflow
# from tensorflow.python.keras.models import load_model
# from tensorflow.keras import backend as K

# Always clear session before start
# K.clear_session()
# tensorflow.keras.backend.clear_session()

## Initialise Flask
app = Flask(__name__)

## load model
@app.before_first_request
def load_model_keras_model():
    global model
    # model = load_model('./app//model.v2.h5')
    # print("=============================Model Loaded==========================")

global CATEGORIES
CATEGORIES = ['Motorcycle', 'Car', 'Pickup Truck', 'Bus', 'Truck', 'Tractor Trailer']
IMG_HEIGHT = 32 
IMG_WIDTH = 64

# Temporary storage for uploaded pictures
# to be able to display uploaded pictures they should locate in static directory
UPLOAD_FOLDER = 'app/static/tmp' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Maximum Image Uploading size
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Image extension allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# print("Loading keras model")
# load_model_keras_model()

from app import views

