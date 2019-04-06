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

@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@app.route('/add', methods=['GET', 'POST'])
def add_folder():
    if request.method == 'POST':
        folder_name = request.form['name']
        folder_replace = folder_name.replace(' ', '_')
        fullpath = os.path.dirname(os.path.realpath(__file__)) + '/tensorflow-lib/tf_files/' + folder_replace
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        return folder_replace

@app.route('/auth', methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        files = request.files['file']
        #size = os.stat(files).st_size
        filename = secure_filename(files.filename)
        fullpath = os.path.dirname(os.path.realpath(__file__)) + '/static/public/'
        files.save(os.path.join(fullpath, filename))
        # return "<img src='static/public/"+filename+"' border='0'>"
        command = "cd tensorflow-for-poets-2 && python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image="+fullpath+"/"+filename
        try:
            result_success = subprocess.check_output([command], shell=True)
        except subprocess.CalledProcessError as e:
            return "An error occured !"
        return "success %s" % (result_success)
    else:
        return "error occured"

@app.route('/verify', methods=['GET','POST'])
def verify():
    entity_name = request.args.get('fd')
    dir_name = str(entity_name)

    if request.method == 'POST':
        files = request.files.getlist("files[]")
        for file in files:
            filename = secure_filename(file.filename)
            fullpath = os.path.dirname(os.path.realpath(__file__)) + '/tensorflow-lib/tf_files/' + dir_name
            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
                file.save(os.path.join(fullpath, filename))
            else:
                file.save(os.path.join(fullpath, filename))

        return "success"

@app.route('/train-engine', methods=['GET', 'POST'])
def train_engine():
    IMAGE_SIZE=224
    ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}"
    directory = str(request.form['folder_name'])
    dir_name = directory.replace(' ', '_')
    command = "cd tensorflow-for-poets-2 && python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500  --model_dir=tf_files/models/ --summaries_dir=tf_files/training_summaries/"+ARCHITECTURE+" --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --architecture="+ARCHITECTURE+" --image_dir=tf_files/"+ dir_name
    try:
        result_success = subprocess.check_output([command], shell=True)
    except subprocess.CalledProcessError as e:
        return "An error occured !"
    return "success %s" % (result_success)


@app.errorhandler(500)
def internal_error(error):
    return "500 error"

@app.errorhandler(404)
def not_found(error):
    return "404 error", 404

if __name__ == "__main__":
    app.run(debug=True)
