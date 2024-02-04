#!/usr/bin/env python3
import sys
import requests
import argparse
import pprint as p
arguments = {
'-limit' : 'Limit the number of results per page',
'-quality' : 'Filter by quality (480p, 720p, 1080p, 1080p.x265, 2160p, 3D)',
'-minimun_rating' : 'Filter by minimum IMDb rating',
'-query_term' : 'Search for movies by title/IMDb code, actor/director name/IMDb code, put TITLE between quotes for the love of god',
'-genre' : 'Filter by genre (See http://www.imdb.com/genre/ for full list)',
'-sort_by' : 'Sort results by (title, year, rating, peers, seeds, download_count, like_count, date_added)',
'-order_by' : 'Order results by ascending or descending (asc, desc)',
'-with_rt_ratings' : 'Include Rotten Tomatoes rating (true, false)',
'-verbose' : 'Display verbose output (title, id, imdb_code, lang)',

}



def verbose_out(json: dict, i: int):
    qualities = set()
    print(json['data']['movies'][i]['title_long'])
    print(f'id: {json["data"]["movies"][i]["id"]}')
    print(f'imbd_code: {json["data"]["movies"][i]["imdb_code"]}')
    print(f'language: {json["data"]["movies"][i]["language"]}')

    '''
    I COULD NOT FIGURE OUT A PRECISE AND EFFICIENT AND PRECISE WAY TO DO THIS, 
    SO I JUST THREW IN A SET. IF A FUTURE USER/CONTRIBUTOR KNOWS A WAY TO ENHANCE
    THIS, FOR THE LOVE OF GOD MAKE THE COMMIT.
    '''
    for movie in range(json['data']['movie_count']):
        for torrent in range(len(json['data']['movies'][movie]['torrents'])):
            qualities.add(json['data']['movies'][movie]['torrents'][torrent]['quality'])

    print(f'{qualities}\n')



def download_torrent(choice: int):
    pass

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

for i in range(GET['data']['movie_count']):
    print(f'{i} - ', end='')
    if args.verbose:
        verbose_out(GET, i)
    else:
        print(GET['data']['movies'][i]['title_long'])

print("What movie do you want to download?: ")
choice = int(input())

download_torrent(choice)



#TODO: FINISH download_torrent fn
#TODO: SPECIFY PATH TO DOWNLOAD

#TODO: DESKTOP NOTIFICATION WITH OPEN FOLDER BUTTON
    

