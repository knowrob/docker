from webrob.pracinit import prac
from webrob.app_and_db import app
from mln.methods import InferenceMethods, LearningMethods
import os

INFMETHODS = [(InferenceMethods.byName(method),method) for method in InferenceMethods.name2value]
LEARNMETHODS = [(LearningMethods.byName(method),method) for method in LearningMethods.name2value]
LOGICS = [('FirstOrderLogic','FOL'),('FuzzyLogic','Fuzzy')]
MODULES = [(module,module) for module in prac.moduleManifestByName]
GRAMMAR = [('PRACGrammar','PRAC Grammar'), ('StandardGrammar','Standard Grammar')]
MODULES = [('None','None')] + [(module,module) for module in prac.moduleManifestByName]
new_usage = {
    "openWorld": "-ow",
    "maxSteps": "-maxSteps",
    "numChains": "-numChains"}

ENGINES = [ ('PRACMLNs', "PRACMLNs"),
            ({"path": r"/usr/wiss/jain/work/code/alchemy-2009-07-07/bin", "usage": new_usage},"Alchemy - July 2009 (AMD64)"),
            ({"path": r"/usr/wiss/jain/work/code/alchemy-2008-06-30/bin/amd64", "usage": new_usage},"Alchemy - June 2008 (AMD64)"),
            ({"path": os.getenv("ALCHEMY_HOME"), "usage": new_usage},"Alchemy - August 2010 (AMD64)"),
            ({"path": r"c:\users\Domini~1\Research\code\alchemy-2010-08-23\bin", "usage": new_usage},"Alchemy (Win32 desktop)"),
            ({"path": r"c:\research\code\alchemy\bin", "usage": new_usage},"Alchemy (Win32 laptop)")]

POSSIBLEPROPS = ['color', 'size', 'shape', 'hypernym', 'hasa']


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

    for path in os.listdir(app.config['UPLOAD_FOLDER']):
        if path.endswith('.mln'):
            mlns.append(path[0:path.rfind('.mln')])

    return [('{}.mln'.format(mln),'{}.mln'.format(mln)) for mln in mlns]


def updateEvidenceList(modulename):
    evidence = []
    if modulename in prac.moduleManifestByName:
        module_path = prac.moduleManifestByName[modulename].module_path

        if not os.path.isdir(os.path.join(module_path, 'db')): return []
        for path in os.listdir(os.path.join(module_path, 'db')):
            print path
            if os.path.isdir(path): continue
            if path.endswith('.db'):
                evidence.append(path[0:path.rfind('.db')])

    for path in os.listdir(app.config['UPLOAD_FOLDER']):
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
