from flask import Flask,render_template,request,send_file
from werkzeug.utils import secure_filename
from helpers import generate_zip

app = Flask(__name__)

@app.route('/')
def uploader():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
    f = request.files['file']
    f.save(secure_filename('input.mp4'))
    code=generate_zip('input.mp4')
    return send_file(f'output_{code}.zip')

app.run()