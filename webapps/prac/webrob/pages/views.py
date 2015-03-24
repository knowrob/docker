from webrob.app_and_db import app
from flask import render_template, request
from webrob.pages.routes import ensure_knowrob_started
from webrob.pages.learning import learn, PRACLearningForm
from webrob.pages.inference import infer, PRACInferenceForm
from webrob.pages.fileupload import upload

@app.route('/prac/')
def prac():
    print 'prac'
    app.logger.error('/prac/')
    if not ensure_knowrob_started():
        return redirect(url_for('user.logout'))
    return render_template('base.html')


@app.route('/prac/praclearn', methods=['GET', 'POST'])
def praclearn():
    app.logger.error('praclearning...')
    form = PRACLearningForm(csrf_enabled=False)
    form.updateChoices()
    result = ''

    if request.method == 'POST' and form.validate_on_submit():
        app.logger.error("request post")
        if 'uploadMLNFile' in request.form or 'uploadDBFile' in request.form:
            app.logger.error("fileupload")
            upload(request)
        elif 'submit' in request.form:
            app.logger.error("form submit")
            data = request.form
            files = request.files
            result = learn(data, {str(files[x].name) : str(files[x].filename) for x in files})
            print result
            return render_template('learn.html', form=form, result={'res':result})
    app.logger.error("praclearn before render")

    return render_template('learn.html', form=form, result={'res': ""})


@app.route('/prac/pracinfer', methods=['GET', 'POST'])
def pracinfer():
    app.logger.error("pracinference...")
    
    form = PRACInferenceForm(csrf_enabled=False)
    form.updateChoices()

    if request.method == 'POST' and form.validate_on_submit():
        if 'uploadMLNFile' in request.form:
            upload(request)
        elif 'submit' in request.form:
            data = request.form
            files = request.files
            result = infer(data, {str(files[x].name) : str(files[x].filename) for x in files})
            print result
            return render_template('infer.html', form=form, result={'res':result})

            # TODO: visualize
            # return render_template('result.html', form=form)
            # return result
    return render_template('infer.html', form=form, result={'res': ""})    