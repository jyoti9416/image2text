import os
from flask import Flask, render_template, request

from main import imgtotxt



extensions = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = '\\upload\\'


def check_file_typ(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/')
def home_page():
    return render_template('index.html')


# upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='Please upload a file')
        file = request.files['file']


        # if no file selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        elif file and check_file_typ(file.filename):
            file.save(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], file.filename))

            extracted_text = imgtotxt(file)

            return render_template('upload.html', msg='upload processed', extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)

    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
