__author__ = 'deepansh'

import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

# to get the absolute path of the current working directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# home root
@app.route("/")
def index():
    return render_template("upload.html")

# route for uploadning the files
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'files/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))

    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".csv") or (ext == ".tsv"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    return render_template("complete.html", image_name=filename)



@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("files", filename)

# route to view the uploaded files
@app.route('/uploadedfiles')
def get_gallery():
    files = os.listdir('./files')
    print(files)
    return render_template("uploadedfiles.html", files=files)


if __name__ == "__main__":
    app.run(port=8888, debug=True)

