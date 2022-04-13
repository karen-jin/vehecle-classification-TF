from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from google.cloud import vision, translate_v2 as translate
import os, six, io

# Initialise Flask
app = Flask(__name__)

# Provide credentials to authenticate to a Google Cloud API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'

# Temporary storage for uploaded pictures
# to be able to display uploaded pictures they should locate in static directory
UPLOAD_FOLDER = 'static/tmp' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Maximum Image Uploading size
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Image extension allowed
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

# Google Cloud Vision CLient
client = vision.ImageAnnotatorClient()

# Google Cloud Transalte Client
translate_client = translate.Client()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/translate', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         file.save(filepath)
         text_detected = search(filepath)
         translation, language = translate(text_detected)
         return render_template('search_results.html',
                    original=filepath,
                    text=text_detected,
                    translation=translation,
                    language=language)

def search(f):
    with io.open(f, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    text_detected = ""
    if texts:
        text_detected = texts[0].description
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return text_detected

def translate(text):
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text)

    return result["translatedText"], result["detectedSourceLanguage"]

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)