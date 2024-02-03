import sys
import requests


def usage():
    print("Usage: temp.py [ARGS]...")
    print("""Options:\nList Movies:

  -l, --list  The limit of results per page that has been set 1-50 (inclusive)
  -p, --page  Used to see the next page of movies, eg limit=15 and page=2 will show you movies 15-30 
  -q, --quality   Used to filter by a given quality => String (480p, 720p, 1080p, 1080p.x265, 2160p, 3D) 
  -mr, --minimun-rating   Used to filter movie by a given minimum IMDb rating => 0-9
  -qt, --query-term  Used for movie search, matching on: Movie Title/IMDb Code, Actor Name/IMDb Code, Director Name/IMDb Code 
  -g, --genre  Used to filter by a given genre (See http://www.imdb.com/genre/ for full list) 
  -s, --sort  Sorts the results by choosen value => string (title, year, rating, peers, seeds, download_count, like_count, date_added) 
  -o, --order-by   Orders the results by either Ascending or Descending order => (desc, asc)
  -t, --tomato-rating  Returns the list with the Rotten Tomatoes rating included => bool 
        """
        )

if '-h' in sys.argv or '--help' in sys.argv:
    usage()
    sys.exit(0)


