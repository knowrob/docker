from webrob.pracinit import prac
from webrob.app_and_db import app
from flask import request, jsonify
import os

FILEDIRS = {'mln':'mln', 'pracmln':'bin', 'db':'db'}
LOGICS = [('FirstOrderLogic','FOL'),('FuzzyLogic','Fuzzy')]
MODULES = [(module,module) for module in prac.moduleManifestByName]
GRAMMAR = [('PRACGrammar','PRAC Grammar'), ('StandardGrammar','Standard Grammar')]
MODULES = [('None','None')] + [(module,module) for module in prac.moduleManifestByName]



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
    fdir = os.path.join(app.config['UPLOAD_FOLDER'], FILEDIRS.get(request.args.get('fName').rsplit('.', 1)[1], 'misc'))
    filePathUpload = os.path.join(fdir, request.args.get('fName'))
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


def updateKBList(modulename):
    kbs = []
    if modulename in prac.moduleManifestByName:
        module_path = prac.moduleManifestByName[modulename].module_path

        if not os.path.isdir(os.path.join(module_path, 'bin')): return []
        for path in os.listdir(os.path.join(module_path, 'bin')):
            if os.path.isdir(path): continue
            if path.endswith('.pracmln'):
                kbs.append(path[0:path.rfind('.pracmln')])

    if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], 'bin')):
        for path in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'bin')):
            if path.endswith('.pracmln'):
                kbs.append(path[0:path.rfind('.pracmln')])

    return [(kb,kb) for kb in kbs]


def updateMLNList(modulename):
    mlns = []
    if modulename in prac.moduleManifestByName:
        module_path = prac.moduleManifestByName[modulename].module_path

        for path in os.listdir(os.path.join(module_path, 'mln')):
            if os.path.isdir(path): continue
            if path.endswith('.mln'):
                mlns.append(path[0:path.rfind('.mln')])

    if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], 'mln')):
        for path in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'mln')):
            if path.endswith('.mln'):
                mlns.append(path[0:path.rfind('.mln')])

    return [('{}.mln'.format(mln),'{}.mln'.format(mln)) for mln in mlns]


def updateEvidenceList(modulename):
    evidence = []
    if modulename in prac.moduleManifestByName:
        module_path = prac.moduleManifestByName[modulename].module_path

        if not os.path.isdir(os.path.join(module_path, 'db')): return []
        for path in os.listdir(os.path.join(module_path, 'db')):
            if os.path.isdir(path): continue
            if path.endswith('.db'):
                evidence.append(path[0:path.rfind('.db')])

    if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], 'db')):
        for path in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'db')):
            if path.endswith('.db'):
                evidence.append(path[0:path.rfind('.db')])

    return [('{}.db'.format(ev),'{}.db'.format(ev)) for ev in evidence]


def getFileContent(fName):
    c = ''
    with open (fName, "r") as f:
        c=f.read()
    return c


def save_kb(kb, name=None):
    '''
    Pickles the state of the given kb in the uploadfolder.
    - kb:    instance of a PRACKnowledgeBase
    - name:  name of the PRACKnowledgeBase
    '''
    import pickle
    if name is None and not hasattr(kb, 'name'):
        raise Exception('No name specified.')
    binaryFileName = '{}.pracmln'.format(name if name is not None else kb.name)
    binPath = os.path.join(app.config['UPLOAD_FOLDER'], 'bin')
    if not os.path.exists(binPath):
        os.mkdir(binPath)
    f = open(os.path.join(binPath, binaryFileName), 'w+')
    pickle.dump(kb, f)
    f.close()


def add_wn_similarities(db, concepts, wn):
    known_concepts = [wn.synset(c) for c in db.mln.domains['concept']]
    evidence_concepts = [wn.synset(c) for c in concepts]

    for kc in known_concepts:
        for ec in evidence_concepts:
            sim = wn.wup_similarity(kc, ec)
            db.addGroundAtom('is_a({},{})'.format(kc.name, ec.name), sim)
