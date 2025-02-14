#!/usr/bin/env python3

import sys
import requests
import argparse
import urllib
import time 
import warnings

import libtorrent as lt
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
    

    return [title_long, movie_id, movie_imdb, movie_lang, qualities] 

def verbose_out(json: dict, i: int):
    info_list = fetch_movie_info(json, i)

    for i in range(len(info_list)):
        print(info_list[i])

def download_torrent(json: dict, choice: int, quality_choice: str, path: str):
    TORRENT_HASH = None
    torrents = json['data']['movies'][choice]['torrents']
    for torrent in torrents:
        if torrent['quality'] == quality_choice:
            TORRENT_HASH = torrent['hash']
            break
            
    magnet_link = f'magnet:?xt=urn:btih:{TORRENT_HASH}&dn={urllib.parse.quote(fetch_movie_info(json, choice)[0])}&tr=http://tracker.opentrackr.org:1337/announce&tr=udp://tracker.openbittorrent.com:80'

    ses = lt.session()
    params = {
        'save_path': path  
    }
    h = lt.add_magnet_uri(ses, magnet_link, params)

    

    while (not h.status().is_seeding):
        
        print('\r%.2f%% complete (down: %.1f mB/s up: %.1f mB/s peers: %d) %s' % (
            h.status().progress * 100, h.status().download_rate / 1000000, h.status().upload_rate / 1000000,
            h.status().num_peers, h.status().state), end=' ')
        
        time.sleep(1)
    print(f"\n{fetch_movie_info(GET, i)[0]} has finished downloading!")
        
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

GET = requests.get(url).json()

if(check_query(GET)):
    sys.exit()

# check if there is -l in agrs
n = int(GET['data']['movie_count'] if not args.limit else args.limit)
names = []

for i in range(n):
    names.append(fetch_movie_info(GET, i)[0])

#funçãozinha recursiva dnv pra lidar com a opção back do qualities

choice = fzf.prompt(names)
choice = names.index(choice[0])
# why do i [0] on choice and quality? bc fucking fzf.prompt returns an array (?) and i'm too lazy to not use a wrapper , sorry.
quality = fzf.prompt(fetch_movie_info(GET, choice)[4])[0]

magnet_links = []
magnet_links.append([GET, choice, quality, './'])

for magnet in magnet_links:
    download_torrent(magnet[0], magnet[1], magnet[2], magnet[3])

