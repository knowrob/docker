from webrob.pracinit import prac
from webrob.app_and_db import app
from prac.inference import PRACInference, PRACInferenceStep
from mln import readMLNFromFile, readDBFromFile
from mln.database import readDBFromString
from mln.methods import InferenceMethods
from mln.mln import readMLNFromString
from flask import render_template, redirect, request, jsonify, url_for
from wtforms import BooleanField, TextField, TextAreaField, validators, SelectField, FileField, SubmitField
from flask_wtf import Form
from webrob.pages.fileupload import upload
from webrob.pages.utils import updateKBList, updateMLNList, updateEvidenceList, LOGICS, FILEDIRS, MODULES, getFileContent, save_kb, add_wn_similarities
import os, sys
import pickle
import StringIO

INFMETHODS = [(InferenceMethods.byName(method),method) for method in InferenceMethods.name2value]


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
        
    elif data['module'] in prac.moduleManifestByName: # call module's inference method
        print 'Running Inference for module ', data['module']
        infer = PRACInference(prac, [])
        module = prac.getModuleByName(str(data['module']))
        inferenceStep = PRACInferenceStep(infer, module)

        mln = readMLNFromString(str(data['mln']),str( data['logic']))
        
        trainingDBs = readDBFromString(mln, str(data['evidence']), ignoreUnknownPredicates=True)
        inferenceStep.output_dbs = trainingDBs
        infer.inference_steps.append(inferenceStep)

        if 'kb' in data:
            kb = module.load_pracmt(str(data['kb']))
        else:
            kb = module.load_pracmt('default')

        params = {}
        params['queries'] = str(data['queries'])
        params['method'] = str(data['method'])
        params['cwPreds'] = str(data['cwPreds'])
        params['closedWorld'] = (1 if 'closedWorld' in data else 0)
        params['useMultiCPU'] = (1 if 'useMultiCPU' in data else 0)
        params['logic'] = str(data['logic'])
        params.update(eval("dict({})".format(str(data['parameters']))))

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

    else: # inference without module (no WN)
        print 'Running Inference w/o module'

    result = {}
    stpno = 0
    for stp in infer.inference_steps:
        stepx = []
        for db in stp.output_dbs:
            for ek in db.evidence:
                e = db.evidence[ek]
                src = ek.split('(')[1].split(',')[0]
                tar = ek.split('(')[1].split(',')[1].split(')')[0]
                val = ek.split('(')[0] # db.evidence[ek]?\
                arcStyle = 'default'
                stepx.append({'source': src, 'target': tar , 'value': val , 'arcStyle': arcStyle})
        result[stpno] = stepx
        stpno += 1

    return result

