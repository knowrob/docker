from webrob.pracinit import prac
from webrob.app_and_db import app
from prac.learning import PRACLearning
from mln.database import readDBFromString
from mln.mln import readMLNFromString
from mln.methods import LearningMethods
from flask import render_template, request
from wtforms import BooleanField, TextField, TextAreaField, validators, SelectField, FileField, SubmitField, HiddenField
from flask_wtf import Form
from webrob.pages.fileupload import upload
from webrob.pages.utils import updateKBList, updateMLNList, updateEvidenceList, GRAMMAR, LOGICS, MODULES, LEARNMETHODS, ENGINES, POSSIBLEPROPS
import os, sys
import StringIO

class PRACLearningForm(Form):
    engine = SelectField('Engine', validators=[validators.optional()], coerce=str)
    grammar = SelectField('Grammar', validators=[validators.optional()], coerce=str)
    module = SelectField('Module', validators=[validators.optional()], coerce=str)
    logic = SelectField('Logic', validators=[validators.optional()], coerce=str)
    mln_dd = SelectField('MLN', validators=[validators.optional()], coerce=str)
    mlnFile = FileField('')
    mln = TextAreaField('')
    trainedMLN = TextAreaField('')
    evidence_dd = SelectField('Databases', validators=[validators.optional()], coerce=str)
    evidenceFile = FileField('')
    evidence = TextAreaField('')
    parameters = TextField('Parameters', [validators.optional()])
    evidencePreds = TextField('Evidence Predicates', [validators.optional()])
    method =  SelectField('Method', validators=[validators.optional()], coerce=str)
    useMultiCPU = BooleanField('Use all CPU\'s', [validators.optional()], default='')

    submit = SubmitField('')
    uploadMLNFile = SubmitField('')
    uploadDBFile = SubmitField('')


    def updateChoices(self):
        self.engine.choices = ENGINES
        self.grammar.choices = GRAMMAR
        self.module.choices = MODULES
        self.method.choices = LEARNMETHODS
        self.logic.choices = LOGICS
        self.mln_dd.choices = updateMLNList(self.module.data)
        self.evidence_dd.choices = updateEvidenceList(self.module.data)


def learn(data, files):
    if all(x in data for x in ['mln','logic','evidence','module']):
        mln = readMLNFromString(str(data['mln']),str( data['logic']))
        trainingDBs = readDBFromString(mln, str(data['evidence']), ignoreUnknownPredicates=True)
        method = str(getattr(data, 'method', LearningMethods.DCLL))
        evidencePreds = list(getattr(data, 'evidencePreds', [])) or POSSIBLEPROPS
        params = eval("dict({})".format(str(data['parameters'])))

        trainedMLN = mln.learnWeights(trainingDBs, method, evidencePreds=evidencePreds, **params)

        mlnStr = StringIO.StringIO()
        trainedMLN.write(mlnStr)

        return mlnStr.getvalue()
    return None