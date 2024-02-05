#!/usr/bin/env python3

import sys
import requests
import argparse
import libtorrent as lt


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



def download_torrent(json: dict, choice: int):
    pass
    # TORRENT_HASH = json['data']['movies']


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

# print("What movie do you want to download?: ")
# choice = int(input())

# qu_choice = input()
# if qu_choice not in 
# download_torrent(choice)





#TODO: ADD QUALITY CHOICE AFTER MOVIE CHOICE
#TODO: FINISH download_torrent fn
#TODO: DESKTOP NOTIFICATION BUTTON
    

#TODO: FIX -w -- > UPDATE; JUST CANT FUCKING FIND IT , GOING TO LEAVE THIS TODO HERE ANYWAY
