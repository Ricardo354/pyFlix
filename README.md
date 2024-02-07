# PyrateFlix

   Download movies via torrent from yts.mx API


## Installation

1.Clone the git repository
```bash
git clone https://github.com/Ricardo354/pyratedFlix.git
``` 

2.Install the requirements.txt.

```bash
pip install -r /path/to/requirements.txt
```
**If you cant install libtorrent, try to downgrade your python to 3.9!**

3.Give Read, Write and Execute permissions to pyrateFlix
```bash
chmod +rwx pyrateFlix.py
```
## Usage

```bash
./pyrateFlix.py -h                                                                                                                                                                            ✔ 
usage: pyrateFlix [-h] [-l LIMIT] [-q QUALITY] [-m MINIMUN_RATING] [-g GENRE] [-s SORT_BY] [-o ORDER_BY] [-w WITH_RT_RATINGS] [-v]

options:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        Limit the number of results per page
  -q QUALITY, --quality QUALITY
                        Filter by quality (480p, 720p, 1080p, 1080p.x265, 2160p, 3D)
  -m MINIMUN_RATING, --minimun_rating MINIMUN_RATING
                        Filter by minimum IMDb rating
  -g GENRE, --genre GENRE
                        Filter by genre (See http://www.imdb.com/genre/ for full list)
  -s SORT_BY, --sort_by SORT_BY
                        Sort results by (title, year, rating, peers, seeds, download_count, like_count, date_added)
  -o ORDER_BY, --order_by ORDER_BY
                        Order results by ascending or descending (asc, desc)
  -v, --verbose         Display verbose output (title, id, imdb_code, lang, qualities)
```

![](https://github.com/Ricardo354/pyrateFlix/edit/main/example.gif)

The program is not completely idiotproof, so please use it carefully, and open a issue if you find a dumb bug.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.



## License

[MIT](https://choosealicense.com/licenses/mit/)
