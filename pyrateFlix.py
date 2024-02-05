#!/usr/bin/env python3

import sys
import requests
import argparse
import urllib
import libtorrent as lt
import time 
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


arguments = {
'-limit' : 'Limit the number of results per page',
'-quality' : 'Filter by quality (480p, 720p, 1080p, 1080p.x265, 2160p, 3D)',
'-minimun_rating' : 'Filter by minimum IMDb rating',
'-query_term' : 'Search for movies by title/IMDb code, actor/director name/IMDb code, put TITLE between quotes for the love of god',
'-genre' : 'Filter by genre (See http://www.imdb.com/genre/ for full list)',
'-sort_by' : 'Sort results by (title, year, rating, peers, seeds, download_count, like_count, date_added)',
'-order_by' : 'Order results by ascending or descending (asc, desc)',
'-with_rt_ratings' : 'Include Rotten Tomatoes rating (true, false)',
'-verbose' : 'Display verbose output (title, id, imdb_code, lang, qualities)',

}

def fetch_info(json: dict, i: int):
    title_long = json['data']['movies'][i]['title_long']
    movie_id = f'id: {json["data"]["movies"][i]["id"]}'
    movie_imdb = f'imbd_code: {json["data"]["movies"][i]["imdb_code"]}'
    movie_lang = f'language: {json["data"]["movies"][i]["language"]}'


    return [title_long, movie_id, movie_imdb, movie_lang]

def verbose_out(json: dict, i: int):
    info_list = fetch_info(json, i)
    qualities = set()

    for i in range(len(info_list)):
        print(info_list[i])

    '''
    I COULD NOT FIGURE OUT A PRECISE AND EFFICIENT AND PRECISE WAY TO PRINT THE QUALITIES, 
    SO I JUST THREW IN A SET. IF A FUTURE USER/CONTRIBUTOR KNOWS A WAY TO ENHANCE
    THIS, FOR THE LOVE OF GOD MAKE THE COMMIT.

    IF YOU USE AN ARRAY FOR THIS IT APPENDS 720p LIKE 20 TIMES, IT IS TERRIFYING.
    '''

    for movie in range(json['data']['movie_count']):
        for torrent in range(len(json['data']['movies'][movie]['torrents'])):
            qualities.add(json['data']['movies'][movie]['torrents'][torrent]['quality'])

    print(f'{qualities}\n')



def download_torrent(json: dict, choice: int, quality_choice: str, path: str):
    for torrent in json['data']['movies'][choice]['torrents']:
        if torrent['quality'] == quality_choice:
            TORRENT_HASH = torrent['hash']
            break
    magnet_link = f'magnet:?xt=urn:btih:{TORRENT_HASH}&dn={urllib.parse.quote(fetch_info(json, choice)[0])}&tr=http://tracker.opentrackr.org:1337/announce&tr=udp://tracker.openbittorrent.com:80'

    ses = lt.session()

    params = {
        'save_path': path  
    }
    h = lt.add_magnet_uri(ses, magnet_link, params)
        
    while not h.status().is_seeding:
        time.sleep(1)

    info = h.get_torrent_info()

    # Save the .torrent file
    torrent_file_path = info.name() + ".torrent"
    with open(torrent_file_path, "wb") as f:
        f.write(lt.bencode(info))
    

def remove_dash(text: str):
    return text.replace('-', '')

parser = argparse.ArgumentParser(prog='pyrateFlix')

url = 'https://yts.mx/api/v2/list_movies.json?'

for arg_name, arg_desc in arguments.items():
    if arg_name == '-quality':
        parser.add_argument(f'-qu', f'-{arg_name}', help=f'{arg_desc}')
    elif arg_name == '-verbose':
        parser.add_argument(f'-{arg_name[1]}', f'-{arg_name}', help=f'{arg_desc}', action='store_true')
    else:
        parser.add_argument(f'-{arg_name[1]}', f'-{arg_name}', help=f'{arg_desc}')
        

args = parser.parse_args()


for arg_name, arg_desc in arguments.items():
    arg_value = getattr(args, remove_dash(arg_name))
    if arg_value is not None:
        if '?' not in url:
            url += f'?{remove_dash(arg_name)}={arg_value}'
        else:
            url += f'&{remove_dash(arg_name)}={arg_value}'

GET = requests.get(url).json()


# check if there is -l in agrs
n = int(GET['data']['movie_count'] if not args.limit else args.limit)

for i in range(n):
    print(f'{i} - ', end='')
    if args.verbose:
        verbose_out(GET, i)
    else:
        print(fetch_info(GET, i)[0])



choice = int(input("What movie do you want to download?: "))
PATH = input("Do you want to choose a path to download your torrents?: (default .)")

while True:
    quality_choice = input("Enter the quality you want to download (e.g., 720p): ")
    if quality_choice in {t['quality'] for t in GET['data']['movies'][choice]['torrents']}:
        download_torrent(GET, choice, quality_choice, PATH)
        break
    else:
        print("Invalid quality choice. Please choose from the available qualities.")

#TODO: ENABLE MULTIPLE TORRENT DOWNLOADING.

#TODO: DESKTOP NOTIFICATION BUTTON

#TODO: FIX -w -- > UPDATE; JUST CANT FUCKING FIND IT , GOING TO LEAVE THIS TODO HERE ANYWAY
