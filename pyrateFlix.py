#!/usr/bin/env python3
import sys
import requests
import argparse

arguments = {
'-limit' : 'Limit the number of results per page',
'-quality' : 'Filter by quality (480p, 720p, 1080p, 1080p.x265, 2160p, 3D)',
'-minimun_rating' : 'Filter by minimum IMDb rating',
'-query_term' : 'Search for movies by title/IMDb code, actor/director name/IMDb code, put TITLE between quotes for the love of god',
'-genre' : 'Filter by genre (See http://www.imdb.com/genre/ for full list)',
'-sort_by' : 'Sort results by (title, year, rating, peers, seeds, download_count, like_count, date_added)',
'-order_by' : 'Order results by ascending or descending (asc, desc)',
'-with_rt_ratings' : 'Include Rotten Tomatoes rating (true, false)'

}
'''
#TODO: ADD VERBOSE ARGUEMENT FOR ENABLING
MOVIE1
    title_long
    id
    imdb_code
    language
OR 
TITLE_LONG

'''

def download_torrent():


def remove_dash(argument):
    return argument.replace('-', '')

parser = argparse.ArgumentParser(prog='pyrateFlix')

url = 'https://yts.mx/api/v2/list_movies.json?'

for arg_name, arg_desc in arguments.items():
    if arg_name == '-quality':
        parser.add_argument(f'-qu', f'-{arg_name}', help=f'{arg_desc}')
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

data = requests.get(url).json()
print(data['data']['movie_count'])
for i in range(data['movie_count']):
    print(data['data']['movies'][i]['title_long'])

#TODO: ENUMERATE MOVIES LIKE
'''
1 - MOVIE1
2 - MOVIE2...
WHAT MOVIE DO YOU WANT TO DOWNLOAD?
1
DOWNLOAD TORRENT...
'''