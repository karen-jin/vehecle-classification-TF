from app import app, CATEGORIES, allowed_file, IMG_HEIGHT, IMG_WIDTH #, model

import os
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
# from PIL import Image

# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.preprocessing.image import ImageDataGenerator

# image_generator = ImageDataGenerator(rescale=1./255) 

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/classify', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         file.save(filepath)
         prediction, label = predict(filepath)
         return render_template('classified.html', 
            probabilities=prediction, 
            label=label, 
            classes=CATEGORIES,
            image=os.path.join("/static/tmp/", filename))

def predict(f):
   # img = image.load_img(f, target_size=(IMG_HEIGHT, IMG_WIDTH))
   # x = image.img_to_array(img)
   # x = np.expand_dims(x, axis=0)
   # use image_generator to preprocess input only if you used it for training
   # prediction = model.predict(image_generator.flow(x)) 
   # prediction = prediction[0]
   # class_label = CATEGORIES[np.argmax(prediction)]

   prediction = [0.02, 0.9, 0.01, 0.01, 0.01, 0.001] # mock data
   class_label = CATEGORIES[np.argmax(prediction)]
   return prediction, class_label
		
if __name__ == '__main__':
   print(("* Loading Keras model and Flask starting server..."
         "please wait until server has fully started"))
   app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)