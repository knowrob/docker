
from flask import request, render_template, jsonify, Markup
# FIXME
# Seems to be broken ?!? Err msg:
# File "/usr/local/lib/python2.7/dist-packages/flask_misaka.py", line 8, in <module>
#    from misaka import (EXT_AUTOLINK, EXT_FENCED_CODE,  # pyflakes.ignore
# ImportError: cannot import name EXT_LAX_HTML_BLOCKS
#from flask.ext.misaka import markdown
from flask_user import current_app
from urlparse import urlparse

import re
import json

from webrob.models.tutorials import Tutorial
from webrob.app_and_db import app
from webrob.utility import admin_required
from webrob.models.tutorials import read_tutorial_page

@app.route('/knowrob/tutorials/')
@app.route('/knowrob/tutorials/<cat_id>/')
@app.route('/knowrob/tutorials/<cat_id>/<page>')
def tutorials(cat_id='getting_started', page=1):
    session['video'] = 0
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'tutorials'
    show_south_pane = False
    readonly = True
    authentication = False

    tut = read_tutorial_page(cat_id, page)
    #content = markdown(tut.text, fenced_code=True)
    content = tut.text

    # automatically add event handler for highlighting DOM elements
    tmp = re.findall('<em>(.*?)</em>', str(content))
    for t in tmp:
        if 'hl_' in t:
            text = t.split(' hl_')[0]
            idname = t.split(' hl_')[1]
            content = re.sub('<em>{} hl_{}</em>'.format(text, idname), '<em onmouseover="knowrob.highlight_element(&#39;{0}&#39;, &#39;id&#39;, true)" onmouseout="knowrob.highlight_element(&#39;{0}&#39;, &#39;id&#39;, false)">{1}</em>'.format(idname, text), str(content))
        elif 'hlc_' in t:
            text = t.split(' hlc_')[0]
            classname = t.split(' hlc_')[1]
            content = re.sub('<em>{} hlc_{}</em>'.format(text, classname), '<em onmouseover="knowrob.highlight_element(&#39;{0}&#39;, &#39;class&#39;, true)" onmouseout="knowrob.highlight_element(&#39;{0}&#39;, &#39;class&#39;, false)">{1}</em>'.format(classname, text), str(content))

    # automatically add "ask as query" links after code blocks
    content = re.sub('</code>(\s)?</pre>', "</code></pre><div class='show_code'><a href='#' class='show_code'>Ask as query</a></div>", str(content))
    content = Markup(content)

    # check whether there is another tutorial in this category
    nxt  = read_tutorial_page(cat_id, int(page)+1)
    prev = read_tutorial_page(cat_id, int(page)-1)

    return render_template('knowrob_tutorial.html', **locals())

@app.route('/knowrob/admin/tutorials')
@admin_required
def admin_tutorials():
    return render_template('admin_tutorials.html', **locals())

@app.route('/knowrob/admin/tutorial_list', methods=['POST'])
@admin_required
def admin_tutorial_list():
    db_adapter = current_app.user_manager.db_adapter
    tutorials = db_adapter.find_all_objects(Tutorial)
    tut_list = map(lambda r:  {
        'id': str(r.id),
        'cat_id': str(r.cat_id),
        'cat_title': str(r.cat_title),
        'title': str(r.title),
        'text': str(r.text),
        'page': str(r.page)
    }, tutorials)
    return jsonify(tutorials=tut_list)

def find_cat_id(title):
    db_adapter = current_app.user_manager.db_adapter
    tutorials = db_adapter.find_all_objects(Tutorial)
    for t in tutorials:
        if str(t.cat_title) == title: return str(t.cat_id)
    return None

@app.route('/knowrob/admin/tutorial_save', methods=['POST'])
@admin_required
def admin_tutorial_save():
    db_adapter = current_app.user_manager.db_adapter
    tut_update = json.loads(request.data)
    tut_db = db_adapter.get_object(Tutorial, tut_update['id'])
    
    db_adapter.update_object(tut_db,
        cat_id = find_cat_id( tut_update['cat_title'] ),
        cat_title = tut_update['cat_title'],
        title = tut_update['title'],
        text = tut_update['text'],
        page = tut_update['page']
    )
    db_adapter.commit()
    
    return jsonify(result=None)

@app.route('/knowrob/admin/tutorial_new', methods=['POST'])
@admin_required
def admin_tutorial_new():
    db_adapter = current_app.user_manager.db_adapter
    new_tut = json.loads(request.data)
    
    app.logger.info("Creating tutorial with title: " + new_tut['title'] + "\n")
    
    db_adapter.add_object(Tutorial,
        cat_id = find_cat_id( new_tut['cat_title'] ),
        cat_title = new_tut['cat_title'],
        title = new_tut['title'],
        text = new_tut['text'],
        page = new_tut['page']
    )
    db_adapter.commit()
    return jsonify(result=None)

@app.route('/knowrob/admin/tutorial_remove', methods=['POST'])
@admin_required
def admin_tutorial_remove():
    db_adapter = current_app.user_manager.db_adapter
    tut_del = json.loads(request.data)
    tut_db = db_adapter.get_object(Tutorial, tut_del['id'])
    
    app.logger.info("Removing tutorial: " + str(tut_db.title) + "[" + str(tut_db.id) + "]."  + "\n")
    db_adapter.delete_object(tut_db)
    db_adapter.commit()
    
    return jsonify(result=None)
