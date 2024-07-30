from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
socketio = SocketIO(app)

segmentor = SelfiSegmentation()

def process_image(background_path):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    background = cv2.imread(background_path)
    background = cv2.resize(background, (640, 480))
    print("Started video capture and background replacement")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame from camera")
            break

        img_out = segmentor.removeBG(img, background, cutThreshold=0.8)
        ret, buffer = cv2.imencode('.jpg', img_out)
        frame = base64.b64encode(buffer).decode('utf-8')
        print("Emitting frame")
        socketio.emit('frame', frame)
        socketio.sleep(0.03)

    cap.release()
    print("Video capture released")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part in the request")
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        print(f"File saved to {filepath}")
        socketio.start_background_task(process_image, filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    socketio.run(app, debug=True)
