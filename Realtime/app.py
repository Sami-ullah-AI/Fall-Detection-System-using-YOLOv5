from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
#from fall_detection import falldetection
#from notification import notify
#import keys

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index1.html')

@app.route("/opencam", methods=['GET'])
def opencam():
    print("here")
    subprocess.run(['python', 'fall_detection.py'])
    return "File processed"


if __name__ == '__main__':
    app.run(debug=True)