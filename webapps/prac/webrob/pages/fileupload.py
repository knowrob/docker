import os
from flask import request, send_from_directory
from werkzeug import secure_filename
from webrob.app_and_db import app

FILEDIRS = {'mln':'mln', 'pracmln':'bin', 'db':'db'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def upload(request):
    for f in request.files:
        file = request.files[f]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fpath = os.path.join(app.config['UPLOAD_FOLDER'], FILEDIRS.get(filename.rsplit('.', 1)[1], 'misc'))
            if not os.path.exists(fpath):
                os.mkdir(fpath)
            file.save(os.path.join(fpath, filename))


@app.route('/uploads/<filedir>/<filename>')
def uploaded_file(filedir, filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], filedir), filename)
