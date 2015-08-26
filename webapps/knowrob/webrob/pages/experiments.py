
def get_experiment_url(category, episode):
    if category is not None and episode is not None:
        episode_url = '/knowrob/'
        if __is_video__(): episode_url += 'video/'
        episode_url += 'episode/'
        if len(category)>0: episode_url += category + '/'
        episode_url += episode
        return episode_url
    else:
        return None

def get_experiment_download_url():
    if 'episode-category' in session and 'episode' in session:
        episode_url = '/knowrob/episode_data/'
        if len(session['episode-category'])>0: episode_url += session['episode-category'] + '/'
        episode_url += session['episode']
        return episode_url
    else:
        return None
 
def get_experiment_list():
    out = []
    root_path = "/episodes"
    
    for category in os.listdir(root_path):
        p = os.path.join(root_path, category)
        if not os.path.isdir(p): continue
        
        for experiment in os.listdir(p):
            out.append((category,experiment))
    
    return out

def get_experiment_path(category, episode):
    return "/episodes/"+category+"/"+episode

def experiment_load_queries(category, episode):
    episode_file = "/episodes/"+category+"/"+episode+"/queries.json"
    if not os.path.isfile(episode_file): return None
    data = None
    with open(episode_file) as data_file: data = json.load(data_file)
    return data

def experiment_save_queries(category, episode, data):
    episode_file = "/episodes/"+category+"/"+episode+"/queries.json"
    if not os.path.isfile(episode_file): return None
    app.logger.info("Saving " + episode_file)
    with open(episode_file, 'w') as data_file: json.dump(data, data_file)
