from flask import Flask, url_for, request, redirect, render_template
from  werkzeug.debug import get_current_traceback
from werkzeug import secure_filename
import os
import subprocess

UPLOAD_FOLDER = '/home/abbey/Documents/python/image_auth/templates/public/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/auth', methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        files = request.files['file']
        #size = os.stat(files).st_size
        filename = secure_filename(files.filename)
        fullpath = os.path.dirname(os.path.realpath(__file__)) + '/static/public/'
        files.save(os.path.join(fullpath, filename))
        #return "<img src='static/public/"+filename+"' border='0'>"
        command = "cd tensorflow-for-poets-2 && python tf_files/label_image.py --image="+fullpath+"/"+filename+" --graph=tf_files/retrained_graph.pb --label=tf_files/retrained_labels.txt"
        try:
            result_success = subprocess.check_output([command], shell=True)
        except subprocess.CalledProcessError as e:
            return "An error occured !"
        return "success %s" % (result_success)
    else:
        return "error occured"


@app.errorhandler(500)
def internal_error(error):
    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error", 404

if __name__ == "__main__":
    app.run(debug=True)
