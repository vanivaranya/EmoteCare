# from flask import Flask, render_template, request, jsonify
# import cv2
# import numpy as np
# from keras.models import load_model
# import threading

# app = Flask(__name__)

# # Load emotion detection model
# model = load_model('C:\\Users\\tanya\\Downloads\\my_model.h5')

# label2category = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

# def capture_emotion_webcam():
#     try:
#         cap = cv2.VideoCapture(0)

#         if not cap.isOpened():
#             return None

#         emotions = []

#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 break

#             gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
#             resized_frame = cv2.resize(gray_frame, (48, 48))
#             img = np.expand_dims(resized_frame, axis=0)
#             img = np.expand_dims(img, axis=3)
#             img /= 255.0

#             predicted_class_index = model.predict(img).argmax()
#             predicted_category = label2category[predicted_class_index]
#             emotions.append(predicted_category)

#             cv2.imshow('frame', frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cap.release()
#         cv2.destroyAllWindows()

#         if emotions:
#             predicted_emotion = max(set(emotions), key=emotions.count)
#             return predicted_emotion
#         else:
#             return None

#     except Exception as err:
#         return None

# @app.route('/')
# def index():
#     predicted_emotion = capture_emotion_webcam()
#     return render_template('prediction.html', predicted_emotion=predicted_emotion or 'Error capturing video and predicting emotion.')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from keras.models import load_model
import cv2
import numpy as np

# Load your trained model
model = load_model('C:\\Users\\tanya\\OneDrive\\Desktop\\extras\\classroom\\EmoteCare2\\Emote-Care-main\\my_model.h5')

# Configure the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\tanya\\OneDrive\\Desktop\\extras\\classroom\\EmoteCare2\\Emote-Care-main\\interfaceIntegration\\database\\emotion_data.db'
db = SQLAlchemy(app)

# Define the EmotionData model
class EmotionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    predicted_emotion = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Define the label2category dictionary (customize based on your model)
label2category = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

# Function to capture video from webcam and predict emotion
def capture_emotion_webcam():
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return None

        emotions = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
            resized_frame = cv2.resize(gray_frame, (48, 48))
            img = np.expand_dims(resized_frame, axis=0)
            img = np.expand_dims(img, axis=3)
            img /= 255.0

            predicted_class_index = model.predict(img).argmax()
            predicted_category = label2category[predicted_class_index]
            emotions.append(predicted_category)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if emotions:
            predicted_emotion = max(set(emotions), key=emotions.count)
            return predicted_emotion
        else:
            return None

    except Exception as err:
        return None

# Define routes
@app.route('/')
def index():
    predicted_emotion = capture_emotion_webcam()
    if predicted_emotion:
        # Store data in the database
        new_emotion_data = EmotionData(predicted_emotion=predicted_emotion)
        db.session.add(new_emotion_data)
        db.session.commit()

    return render_template('prediction.html', predicted_emotion=predicted_emotion or 'Error capturing video and predicting emotion.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
