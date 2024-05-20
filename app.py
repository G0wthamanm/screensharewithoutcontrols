from flask import Flask, Response, render_template, request, jsonify
import json
from io import BytesIO
from PIL import Image, ImageGrab
import pyautogui
import logging
import opcode
import webbrowser
from threading import Timer


app = Flask(__name__, template_folder='templates')

ascii_art = """
 _ \                     |                        |        |                    | _)  |    |                 
 |  |   -_) \ \ /   -_)  |   _ \   _ \   -_)   _` |         _ \  |  |          \|   |   _|    \   |  |   _` | 
___/  \___|  \_/  \___| _| \___/  .__/ \___| \__,_|       _.__/ \_, |       _| _| _| \__| _| _| \_, | \__,_| 
                                 _|                 ____|       ___/  ____|                     ___/         
"""

@app.route('/')
def index():
    return render_template('index.html')

logging.basicConfig(level=logging.INFO)

@app.route('/mouse-control', methods=['POST'])
def mouse_control():
    data = request.get_json()
    command = data['command']
    if command == 'move':
        dx = data['dx']
        dy = data['dy']
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + dx, current_y + dy)
    elif command == 'click':
        button = data['button']
        pyautogui.click(button=button)
    return jsonify(status='success'), 200

@app.route('/feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        img_buffer = BytesIO()
        screenshot = ImageGrab.grab()
        screenshot = screenshot.convert('RGB')
        screenshot.save(img_buffer, 'JPEG', quality=85)
        img_buffer.seek(0)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + img_buffer.read() + b'\r\n\r\n')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    print(ascii_art)
    Timer(1, open_browser).start()
    app.run(host='0.0.0.0', debug=False)
