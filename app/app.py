from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import json
UPLOAD_FOLDER = 'save_file/'
ALLOWED_EXTENSIONS = {'txt','pdf','jpg','jpeg','gif','png','vir'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from museum import MUSEUM
import os
from requests import get

ES_HOST = get("https://api.ipify.org").text
ES_PORT = 9200
INDEX = 'app_server'
#ES_HOST = '203.246.112.139'
#ES_PORT = 49200
#INDEX = 'experimental_group'

def search(path, threshold=0.1, limit=75):
    ms = MUSEUM(host=ES_HOST, port=ES_PORT, use_caching=False)
    result = ms.search(INDEX, path, limit=limit)
    return result

def allowed_files(filename) :
    if filename.split('.')[1].lower() in ALLOWED_EXTENSIONS :
        return True
    else :
        return False
@app.route('/')
def main():
    return render_template('main/index.html')

@app.route('/uploader',methods=['GET','POST'])
def upload_file() :
    if request.method == 'POST' :
        if 'file' not in request.files :
            flash('File is not Selected')
            return redirect(request.url)
        file = request.files['file']
        if allowed_files(file.filename) :
            filename = secure_filename(file.filename)
            path = os.path.join(os.getcwd(),os.path.join(app.config['UPLOAD_FOLDER'],filename))
            file.save(path)
            return redirect(url_for('result',filename=str(filename)))

@app.route('/result/<filename>')
def result(filename) :
    folder = os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'])
    if filename in os.listdir(folder) :
        result = search(os.path.join(folder,filename))
        return render_template('result/result.html', result=result)

if __name__ == '__main__' :
    app.run()