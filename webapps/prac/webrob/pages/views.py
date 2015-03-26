from webrob.app_and_db import app

from flask import render_template, request, send_from_directory, session, url_for, jsonify
from flask_user import login_required

from webrob.pages.routes import ensure_prac_started
from webrob.pages.learning import learn, PRACLearningForm
from webrob.pages.inference import infer, PRACInferenceForm
from webrob.pages.fileupload import upload, saveMLN

from urlparse import urlparse
import os

@app.route('/prac/static/<path:filename>')
@login_required
def download_static(filename):
  return send_from_directory(os.path.join(app.root_path, "static"), filename)

@app.route('/prac/')
@login_required
def prac():
    if not ensure_prac_started():
        return redirect(url_for('user.logout'))
    
    error=""
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']

    return render_template('prac.html', **locals())


@app.route('/prac/menu', methods=['POST'])
def menu():
    menu_left = []
    
    selection = "Options"
    choices =  [('PracLEARN', url_for('prac')+'praclearn'),('PracINFER', url_for('prac')+'pracinfer')]
    
    menu_right = [
        ('CHOICES', (selection, choices))
    ]
    
    return jsonify(menu_left=menu_left, menu_right=menu_right)


@app.route('/prac/praclearn', methods=['GET', 'POST'])
@login_required
def praclearn():
    form = PRACLearningForm(csrf_enabled=False)
    form.updateChoices()
    result = {'res': ''}

    if request.method == 'POST' and form.validate_on_submit():
        if 'uploadMLNFile' in request.form or 'uploadDBFile' in request.form:
            upload(request)
        elif 'saveMLNFile' in request.form:
            saveMLN(request)
        elif 'submit' in request.form:
            data = request.form
            files = request.files
            result['res'] = learn(data, {str(files[x].name) : str(files[x].filename) for x in files})
            return render_template('learn.html', **locals())

    return render_template('learn.html', **locals())


@app.route('/prac/pracinfer', methods=['GET', 'POST'])
@login_required
def pracinfer():
    form = PRACInferenceForm(csrf_enabled=False)
    form.updateChoices()
    result = {'res': ''}

    if request.method == 'POST' and form.validate_on_submit():
        if 'uploadMLNFile' in request.form:
            upload(request)
        elif 'submit' in request.form:
            data = request.form
            files = request.files
            result['res'] = infer(data, {str(files[x].name) : str(files[x].filename) for x in files})
            return render_template('infer.html', **locals())

            # TODO: visualize
            # return render_template('result.html', form=form)
            # return result
    return render_template('infer.html', **locals())

