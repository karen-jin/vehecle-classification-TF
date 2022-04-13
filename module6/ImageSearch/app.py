from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         file.save(filepath)
         best_guess_label, web_entities, image_urls = search(filepath)
         return render_template('search_results.html',
                    original=filepath,
                    best_guess_label=best_guess_label,
                    web_entities=web_entities,
                    image_urls=image_urls)

def search(f):
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(f, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.web_detection(image=image)
    annotations = response.web_detection
    
    best_guess_label = None
    if annotations.best_guess_labels:
        labels = [label.label for label in annotations.best_guess_labels]
        best_guess_label = ','.join(labels)

    web_entities = []
    if annotations.web_entities:
        web_entities = annotations.web_entities

    visually_similar_images = []
    if annotations.visually_similar_images:
        visually_similar_images = [image.url for image in annotations.visually_similar_images]

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return best_guess_label, web_entities, visually_similar_images

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)