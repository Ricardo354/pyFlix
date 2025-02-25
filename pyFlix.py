#!/usr/bin/env python3

import sys
import requests
import argparse
import urllib
import time 
import warnings
import xmlrpc.client

import subprocess
import os

from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()

warnings.filterwarnings("ignore", category=DeprecationWarning)

arguments = {
'-limit' : 'Limit the number of results per page',
'-quality' : 'Filter by quality (480p, 720p, 1080p, 1080p.x265, 2160p, 3D)',
'-minimun_rating' : 'Filter by minimum IMDb rating',
'-genre' : 'Filter by genre (See http://www.imdb.com/genre/ for full list)',
'-sort_by' : 'Sort results by (title, year, rating, peers, seeds, download_count, like_count, date_added)',
'-order_by' : 'Order results by ascending or descending (asc, desc)',
'-verbose' : 'Display verbose output (title, id, imdb_code, lang, qualities)',
}

def fetch_movie_info(json: dict, movie_index: int):
    movie = json['data']['movies']
    title_long = movie[movie_index]['title_long']
    movie_id = f'id: {movie[movie_index]["id"]}'
    movie_imdb = f'imbd_code: {movie[movie_index]["imdb_code"]}'
    movie_lang = f'language: {movie[movie_index]["language"]}'
    large_cover = movie[movie_index]["large_cover_image"]
    qualities = set()
    
    '''

    * this snippet of code may return false data, as in qualities = {'3D','1080p'...} while not 
    having 3D torrent hash available

    for movie in json['data']['movies']:
        for torrent in movie['torrents']:
            qualities.add(torrent['quality'])
    '''

    # * this one doesn't, so yea im fuckinng using this

    torrents = json['data']['movies'][movie_index]['torrents']
    for torrent in torrents:
        qualities.add(torrent['quality'])
    

    return [title_long, movie_id, movie_imdb, movie_lang, qualities, large_cover] 

def download_torrent(json: dict, choice: int, quality_choice: str, path: str):
    TORRENT_HASH = None
    torrents = json['data']['movies'][choice]['torrents']
    for torrent in torrents:
        if torrent['quality'] == quality_choice:
            TORRENT_HASH = torrent['hash']
            break
    magnet_link = f'magnet:?xt=urn:btih:{TORRENT_HASH}&dn={urllib.parse.quote(fetch_movie_info(json, choice)[0])}&tr=http://tracker.opentrackr.org:1337/announce&tr=udp://tracker.openbittorrent.com:80'
    
    pwd = os.getcwd()
    download_dir = os.path.join(pwd, 'movies')
    os.makedirs(download_dir, exist_ok=True)
    
    aria2c = subprocess.Popen(
        ['aria2c', '--enable-rpc', '--rpc-listen-all', '--rpc-listen-port=6800', '--seed-time=0', '--allow-overwrite=true', '--daemon=true', f'--dir={download_dir}'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )

    for _ in range(10): 
        try:
            s = xmlrpc.client.ServerProxy('http://localhost:6800/rpc')
            s.aria2.getGlobalStat()
            break
        except:
            time.sleep(1)
    else:
        print("ei n coisou n e agora")
        return

    gid = s.aria2.addUri([magnet_link])


    #exiting and initializing background downloa monitor
    pid = os.fork()
    if pid == 0:
        monitor_download()
        sys.exit() 
    #blz mas isso aq é do caralho viu, sabia disso n
    

def monitor_download():
    
    s = xmlrpc.client.ServerProxy('http://localhost:6800/rpc')

    while True:
        active_downloads = s.aria2.tellActive()
        for task in active_downloads:
            if '[METADATA]' in task['files'][0]['path'] or task['status'] == 'removed':
                continue
            else:       
                if task['completedLength'] == task['totalLength']:
                    movie_name = task['bittorrent']['info']['name']
                    subprocess.run(['notify-send', '-a', 'pyFlix', f'{movie_name} finished downloading!', '--urgency=critical'])
                    s.aria2.forceRemove(task['gid'])
        if len(active_downloads) == 0: # Se não tiver mais download...
            s.aria2.forceShutdown()
            return
        time.sleep(5) 
    

def remove_dash(text: str):
    return text.replace('-', '')

def check_query(json: dict):
    if json['data']['movie_count'] == 0:
        print("No movies found, search again. (TYPE THE EXACT NAME OF THE MOVIE!)")
        return 1
    else:
        return 0

parser = argparse.ArgumentParser(prog='pyrateFlix')
for arg_name, arg_desc in arguments.items():
    if arg_name == '-verbose':
        parser.add_argument(f'-{arg_name[1]}', f'-{arg_name}', help=f'{arg_desc}', action='store_true')
    else:
        parser.add_argument(f'-{arg_name[1]}', f'-{arg_name}', help=f'{arg_desc}')

parser.add_argument('query', type=str, nargs="+", help="Your query for the movie you want to find.")

args = parser.parse_args()

query = args.query 
query = " ".join(args.query)

url = f'https://yts.mx/api/v2/list_movies.json?query_term="{query}"'

for arg_name, arg_desc in arguments.items():
    arg_value = getattr(args, remove_dash(arg_name))
    if arg_value is not None:
        if '?' not in url:
            url += f'?{remove_dash(arg_name)}={arg_value}'
        else:
            url += f'&{remove_dash(arg_name)}={arg_value}'

try:
    GET = requests.get(url)
    GET.raise_for_status()
    GET = GET.json()
except Exception as err:
    print(f"An error occurred: {err}")
    sys.exit()

if(check_query(GET)):
    sys.exit()

# check if there is -l in agrs
n = int(GET['data']['movie_count'] if not args.limit else args.limit)

movies = {}

for i in range(n):
    movies[fetch_movie_info(GET, i)[0]] = fetch_movie_info(GET, i)[-1]

#should probably turn this into an argument

for movie_name, movie_cover_url in movies.items():
    res = requests.get(movie_cover_url)
    if res.status_code == 200:
         with open(f'/tmp/{movie_name}.jpg', 'wb') as fp:
            fp.write(res.content)

def prompt():
    try:
        movies['exit'] = "exit"
        movie_choice = fzf.prompt(movies, "--prompt='Select Movie: ' --reverse --preview='chafa /tmp/{}.jpg --view-size 57x55 2>/dev/null' --preview-window=34%")        

        if movie_choice[0] == "exit":   
            sys.exit()

        #This method builds a dictionary using dictionary comprehension that maps each key to its index, allowing O(1) lookups.
        # (i stole it from the internet)
        idx_map = {key: i for i, key in enumerate(movies)}
        movie_choice = idx_map.get(movie_choice[0])

    except IndexError:  
        print("fucking index error, what did you do")
        sys.exit()
    
    # why do i [0] on choice and quality? bc fucking fzf.prompt returns an array (?) and i'm too lazy to not use a wrapper , sorry.
    quality_prompt = [quality for quality in fetch_movie_info(GET, movie_choice)[4]]
    quality_prompt.insert(len(quality_prompt), 'back')
    quality = fzf.prompt(quality_prompt, "--reverse ")[0]

    if quality == 'back':
        prompt()

    magnet_links = []
    magnet_links.append([GET, movie_choice, quality, './'])

    for magnet in magnet_links:
        download_torrent(magnet[0], magnet[1], magnet[2], magnet[3])

    for movie_name in movies.keys():
        if movie_name != 'exit':
            try:
                os.remove(f'/tmp/{movie_name}.jpg')
            except FileNotFoundError:
                continue

prompt()
