#!/usr/bin/env python3

import sys
import requests
import argparse
import urllib
import time 
import warnings

import libtorrent as lt


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

def get_user_input():

    global continue_flag # --> recursion flag

    continue_flag = bool
    while True:
        choice = int(input("What movie do you want to download?: "))
        if choice < 0 or choice > (n-1):
            print(f"Please choose a number between 0 and {n-1}")
        else:
            break

    PATH = input("Do you want to choose a path to download your torrents (e.g., ./)?: ")

    while True:
        quality_choice = input("Enter the quality you want to download (e.g., 720p): ")
        if quality_choice in {t['quality'] for t in GET['data']['movies'][choice]['torrents']}:
            break
        else:
            print("Invalid quality choice. Please choose from the available qualities.")
    while True:
        option = input("Do you want to download another movie?: [Y/n]")
        if option.lower() == 'n':
            continue_flag = False
            break
        elif option.lower() != 'y':
            option = input("Please select Y(yes) or N(no)")
            continue
        else:
            continue_flag = True
            break

    return [choice, quality_choice, PATH]


def fetch_movie_info(json: dict, i: int):
    title_long = json['data']['movies'][i]['title_long']
    movie_id = f'id: {json["data"]["movies"][i]["id"]}'
    movie_imdb = f'imbd_code: {json["data"]["movies"][i]["imdb_code"]}'
    movie_lang = f'language: {json["data"]["movies"][i]["language"]}'


    qualities = set()
    '''
    I COULD NOT FIGURE OUT A PRECISE AND EFFICIENT WAY TO PRINT THE QUALITIES, 
    SO I JUST THREW IN A SET. IF A FUTURE USER/CONTRIBUTOR KNOWS A WAY TO ENHANCE
    THIS, FOR THE LOVE OF GOD MAKE THE COMMIT.

    IF YOU USE AN ARRAY FOR THIS IT APPENDS 720p LIKE 20 TIMES, IT IS TERRIFYING.
    '''
    for movie in range(json['data']['movie_count']):
        for torrent in range(0, len(json['data']['movies'][movie]['torrents'])):
            qualities.add(json['data']['movies'][movie]['torrents'][torrent]['quality'])


    return [title_long, movie_id, movie_imdb, movie_lang, qualities] 

def verbose_out(json: dict, i: int):
    info_list = fetch_movie_info(json, i)

    for i in range(len(info_list)):
        print(info_list[i])

def download_torrent(json: dict, choice: int, quality_choice: str, path: str):
    for torrent in json['data']['movies'][choice]['torrents']:
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

def recursive_query(magnet_links: list):
    query = input("Search: ")
    url = f'https://yts.mx/api/v2/list_movies.json?query_term={query}'
    GET = requests.get(url).json()
    check_query(GET)
    n = min(args.limit, GET['data']['movie_count']) if args.limit else GET['data']['movie_count']
    for i in range(n):
        print(f'\n{i} - ', end='')
        if args.verbose:
            verbose_out(GET, i)
        else:
            print(f'{fetch_movie_info(GET, i)[0]} - {fetch_movie_info(GET, i)[-1]}')

    user_input = get_user_input()

    magnet_links.append([GET, user_input[0], user_input[1], user_input[2]])

    if not continue_flag: 
        for i in range(len(magnet_links)):
            download_torrent(magnet_links[i][0], magnet_links[i][1], magnet_links[i][2], magnet_links[i][3])
    else:
        recursive_query(magnet_links)

def check_query(json: dict):
    global query
    global url
    global GET
    if json['data']['movie_count'] == 0:
        print("No movies found, search again. (TYPE THE EXACT NAME OF THE MOVIE!)\n")
        query = input("Search: ")
        url = f'https://yts.mx/api/v2/list_movies.json?query_term="{query}"'
        GET = requests.get(url).json()
        check_query(GET)


parser = argparse.ArgumentParser(prog='pyrateFlix')


for arg_name, arg_desc in arguments.items():
    if arg_name == '-verbose':
        parser.add_argument(f'-{arg_name[1]}', f'-{arg_name}', help=f'{arg_desc}', action='store_true')
    else:
        parser.add_argument(f'-{arg_name[1]}', f'-{arg_name}', help=f'{arg_desc}')
        

args = parser.parse_args()

query = input("Search: ")

url = f'https://yts.mx/api/v2/list_movies.json?query_term="{query}"'

for arg_name, arg_desc in arguments.items():
    arg_value = getattr(args, remove_dash(arg_name))
    if arg_value is not None:
        if '?' not in url:
            url += f'?{remove_dash(arg_name)}={arg_value}'
        else:
            url += f'&{remove_dash(arg_name)}={arg_value}'

GET = requests.get(url).json()
check_query(GET)


# check if there is -l in agrs
n = int(GET['data']['movie_count'] if not args.limit else args.limit)

for i in range(n):
    print(f'\n{i} - ', end='')
    if args.verbose:
        verbose_out(GET, i)
    else:
        print(f'{fetch_movie_info(GET, i)[0]} - {fetch_movie_info(GET, i)[-1]}')

user_input = get_user_input()


magnet_links = []
magnet_links.append([GET, user_input[0], user_input[1], user_input[2]])

if not continue_flag:
    for magnet in magnet_links:
        download_torrent(magnet[0], magnet[1], magnet[2], magnet[3])
else:
    recursive_query(magnet_links)

#TODO: Work on error handling < - - NOW THAT is the las todo

#TODO: put size in -v < - - last todo :)
# 4 torrents
    # for i in movie_count
    #   for j in len(['data']['movies'][i]['torrents'])
           # pegar ['data']['movies'][i]['torrents'][i]['size']

# the input 'avengers' is buggy, it says 28 movies but it shows only 19 and after that i raises an IndexError
# my guess is that the API is faulty with some searches, i cant actually know.




