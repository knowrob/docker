
from flask import request, session, render_template, Markup, jsonify
from flask.ext.misaka import markdown
from flask_user import current_user
from urlparse import urlparse
import re

import json

from webrob.app_and_db import app
from webrob.models.tutorials import read_tutorial_page

@app.route('/tutorials/')
def tutorials():
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'tutorials'
    show_south_pane = False
    readonly = True
    authentication = False
    session['video'] = 0
    
    # Use the user container if user is authenticated
    if current_user.is_authenticated:
        container_name = session['user_container_name']
        authentication = True

    return render_template('knowrob_tutorial.html', **locals())

@app.route('/tutorials/get', methods=['POST'])
def get_tutorial():
    data = json.loads(request.data)
    return jsonify(read_tutorial(data['category'], data['page']))

def read_tutorial(cat_id, page):
    tut = read_tutorial_page(cat_id, page)
    content = markdown(tut.text, fenced_code=True)

    # automatically add event handler for highlighting DOM elements
    tmp = re.findall('<em>(.*?)</em>', str(content))
    for t in tmp:
        if 'hl_' in t:
            text = t.split(' hl_')[0]
            idname = t.split(' hl_')[1]
            content = re.sub('<em>{} hl_{}</em>'.format(text, idname), '<em onmouseover="highlightElement(&#39;{0}&#39;, &#39;id&#39;, true)" onmouseout="highlightElement(&#39;{0}&#39;, &#39;id&#39;, false)">{1}</em>'.format(idname, text), str(content))
        elif 'hlc_' in t:
            text = t.split(' hlc_')[0]
            classname = t.split(' hlc_')[1]
            content = re.sub('<em>{} hlc_{}</em>'.format(text, classname), '<em onmouseover="highlightElement(&#39;{0}&#39;, &#39;class&#39;, true)" onmouseout="highlightElement(&#39;{0}&#39;, &#39;class&#39;, false)">{1}</em>'.format(classname, text), str(content))

    # automatically add "ask as query" links after code blocks
    content = re.sub('</code>(\s)?</pre>', "</code></pre><div class='show_code'><a href='#' class='show_code'>Ask as query</a></div>", str(content))
    content = Markup(content)
    # check whether there is another tutorial in this category
    nxt  = read_tutorial_page(cat_id, int(page)+1)
    prev = read_tutorial_page(cat_id, int(page)-1)
    
    out = {}
    out['this'] = {
        'cat_id': tut.cat_title,
        'page': tut.page,
        'title': tut.title,
        'text': content
    }
    if(nxt != None):
        out['next'] = {
            'cat_id': nxt.cat_id,
            'page': nxt.page,
            'title': nxt.title
        }
    if(prev != None):
        out['prev'] = {
            'cat_id': prev.cat_id,
            'page': prev.page,
            'title': prev.title
        }
    
    return out
