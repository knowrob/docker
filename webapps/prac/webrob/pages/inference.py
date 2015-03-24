from webrob.pracinit import prac
from webrob.app_and_db import app
from prac.inference import PRACInference, PRACInferenceStep
from prac.core import PRACKnowledgeBase
from mln import readMLNFromFile, readDBFromFile
from mln.database import readDBFromString
from mln.mln import readMLNFromString
from flask import render_template, redirect, request, jsonify, url_for
from wtforms import BooleanField, TextField, TextAreaField, validators, SelectField, FileField, SubmitField
from flask_wtf import Form
from webrob.pages.fileupload import upload
from webrob.pages.utils import updateKBList, updateMLNList, updateEvidenceList, INFMETHODS, LEARNMETHODS, LOGICS, MODULES, getFileContent, save_kb, add_wn_similarities
import os, sys
import pickle
import StringIO


class PRACInferenceForm(Form):
    description = TextField('Description', [validators.optional()])
    module = SelectField('Module', validators=[validators.optional()], coerce=str)
    logic = SelectField('Logic', validators=[validators.optional()], coerce=str)
    kb = SelectField('KB', validators=[validators.optional()], coerce=str)
    kbName = TextField('Save KB', [validators.optional()])
    saveKB = BooleanField('save')
    mln_dd = SelectField('MLN', validators=[validators.optional()], coerce=str)
    mlnFile = FileField('')
    mln = TextAreaField('')
    evidence_dd = SelectField('Evidence', validators=[validators.optional()], coerce=str)
    evidenceFile = FileField('')
    evidence = TextAreaField('')
    method =  SelectField('Method', validators=[validators.optional()], coerce=str)
    queries = TextField('Queries', [validators.optional()])
    parameters = TextField('Parameters', [validators.optional()])
    senses = TextField('WN Senses', [validators.optional()])
    cwPreds = TextField('CW Preds', [validators.optional()])
    useWn = BooleanField('Add similarities', [validators.optional()], default='')
    closedWorld = BooleanField('Apply CW assumption', [validators.optional()], default='')
    useMultiCPU = BooleanField('Use all CPU\'s', [validators.optional()], default='')
    submit = SubmitField('')
    uploadMLNFile = SubmitField('')

    def updateChoices(self):
        self.module.choices = MODULES
        self.method.choices = INFMETHODS
        self.logic.choices = LOGICS
        self.kb.choices = updateKBList(self.module.data)
        self.mln_dd.choices = updateMLNList(self.module.data)
        self.evidence_dd.choices = updateEvidenceList(self.module.data)


@app.route('/prac/updateModule/', methods=['GET'])
def updateModule():
    module = request.args.get('moduleName')
    kbList = [kb[0] for kb in updateKBList(module)]
    mlnList = [mln[0] for mln in updateMLNList(module)] 
    evidenceList = [ev[0] for ev in updateEvidenceList(module)] 
    ret_data = {'value': module,'kblist': kbList, 'mlnlist': mlnList, 'evidencelist': evidenceList}

    return jsonify(ret_data)


@app.route('/prac/updateUploadedFiles/', methods=['GET'])
def updateUploadedFiles():
    mlnList = [mln[0] for mln in updateMLNList(None)] 
    evidenceList = [ev[0] for ev in updateEvidenceList(None)] 
    ret_data = {'mlnlist': mlnList, 'evidencelist': evidenceList}

    return jsonify(ret_data)


@app.route('/prac/updateText/', methods=['GET'])
def updateText():

    # look for file in upload folder
    filePathUpload = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('fName'))
    if os.path.isfile(filePathUpload):
        return jsonify({'text': getFileContent(filePathUpload)})
    
    # look for file in module path
    if request.args.get('module') in prac.moduleManifestByName:
        module_path = prac.moduleManifestByName[request.args.get('module')].module_path
        filePathModule = os.path.join(os.path.join(module_path, request.args.get('field')), request.args.get('fName'))
        if os.path.isfile(filePathModule):
            return jsonify({'text': getFileContent(filePathModule)})

    return jsonify({'text': ''})


@app.route('/prac/updateKB/', methods=['GET'])
def updateKB():
    if not request.args.get('module') in prac.moduleManifestByName or not request.args.get('kb'): 
        return jsonify({})
    module = prac.getModuleByName(request.args.get('module'))
    kb = module.load_pracmt(request.args.get('kb'))
    res = kb.query_params
    res['mln'] = kb.query_mln_str
    return jsonify(res)


def infer(data, files):
    result = ''
    if data['description']: # extract properties from NL descriptions
        print 'Running NL Parsing'
        infer = PRACInference(prac, [str(data['description'])])
        parser = prac.getModuleByName('nl_parsing')
        prac.run(infer, parser)

        # property inference from parsed input
        propExtract = prac.getModuleByName('prop_extraction')
        prac.run(infer,propExtract,kb=propExtract.load_pracmt('default'))
        
        step = infer.inference_steps[-1]
        for db in step.output_dbs:
            result += 'Inferred properties:\n'
            for ek in sorted(db.evidence):
                e = db.evidence[ek]
                if e == 1.0 and any(ek.startswith(p) for p in ['color', 'size', 'shape', 'hypernym', 'hasa', 'dimension', 'consistency', 'material']):
                    result += '{}({}, {}\n'.format(ek.split('(')[0], ek.split('(')[1].split(',')[0], ek.split('(')[1].split(',')[1])
    elif data['module'] in prac.moduleManifestByName: # call module's inference method
        print 'Running Inference for module ', data['module']
        infer = PRACInference(prac, [])
        module = prac.getModuleByName(str(data['module']))
        inferenceStep = PRACInferenceStep(infer, module)

        # mln = readMLNFromFile(data['mln_dd'], data['logic'])
        mln = readMLNFromString(str(data['mln']),str( data['logic']))
        
        trainingDBs = readDBFromString(mln, str(data['evidence']), ignoreUnknownPredicates=True)
        # trainingDBs = readDBFromFile(mln, inputdbs, ignoreUnknownPredicates=True) #remove
        inferenceStep.output_dbs = trainingDBs
        infer.inference_steps.append(inferenceStep)

        if 'kb' in data:
            kb = module.load_pracmt(str(data['kb']))
        else:
            kb = module.load_pracmt('default')

        params = {}
        params['queries'] = str(data['queries'])
        params['method'] = str(data['method'])
        params['cwPreds'] = list(data['cwPreds'])
        params['closedWorld'] = (1 if 'closedWorld' in data else 0)
        params['useMultiCPU'] = (1 if 'useMultiCPU' in data else 0)
        params['logic'] = str(data['logic'])

        kb.query_params = params
        kb.set_querymln(str(data['mln']), path=os.path.join(module.module_path, 'mln'))
        kb.dbs = list(readDBFromString(kb.query_mln, str(data['evidence'])))

        prac.run(infer, module, mln=mln, kb=kb)
        step = infer.inference_steps[-1]

        if 'saveKB' in data:
            if 'kbName' in data:
                module.save_pracmt(kb, str(data['kbName']))
            else:
                module.save_pracmt(kb, str(data['kb']))

        for db in step.output_dbs:
            db.write(sys.stdout, color=True)
            result += '\nInferred possible concepts:\n'
            for ek in sorted(db.evidence, key=db.evidence.get, reverse=True):
                e = db.evidence[ek]
                if e > 0.001 and ek.startswith('object'):
                    result += '{} {}({}, {})\n'.format('{:.4f}'.format(e), 'object', ek.split(',')[0].split('(')[1], ek.split(',')[1].split(')')[0])
    else: # inference without module (no WN)
        print 'Running Inference w/o module'
        mln = readMLNFromString(str(data['mln']),str( data['logic']))
        trainingDBs = readDBFromString(mln, str(data['evidence']), ignoreUnknownPredicates=True)
        kb = PRACKnowledgeBase(prac)

        params = {}
        params['queries'] = str(data['queries'])
        params['method'] = str(data['method'])
        params['cwPreds'] = list(data['cwPreds'])
        params['closedWorld'] = (1 if 'closedWorld' in data else 0)
        params['useMultiCPU'] = (1 if 'useMultiCPU' in data else 0)
        params['logic'] = str(data['logic'])
        kb.query_params = params

        kb.set_querymln(str(data['mln'])) # TODO: path=uploadfolder?
        
        kb.dbs = list(readDBFromString(kb.query_mln, str(data['evidence'])))
            
        # infer and update output dbs
        output_dbs = []
        dbStr = StringIO.StringIO()
        for db in kb.dbs:
            if 'useWN' in data:
                wn = prac.wordnet
                output_db = add_wn_similarities(db, data['concepts'].replace(' ', '').split(','), wn)
            else:
                output_db = db
            inferred_dbs = list(kb.infer(output_db))
            output_dbs.extend(inferred_dbs)

        if 'saveKB' in data:
            if 'kbName' in data:
                save_kb(kb, str(data['kbName']))
            else:
                save_kb(kb, 'default')

        for db in inferred_dbs:
                for ek in sorted(db.evidence):
                    e = db.evidence[ek]
                    if e == 1.0 and any(ek.startswith(p) for p in kb.query_params['queries'].replace(' ', '').split(',')):
                        result += '{} {}\n'.format(e, ek)



    return result

