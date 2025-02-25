# pyFlix

   **_pyFlix_ is a command-line tool that enables users to effortlessly download movies via torrent**

## Installation

1. Clone the git repository
```bash
git clone https://github.com/Ricardo354/pyFlix.git
``` 

2. Install python 3.10

```bash
sudo apt-get install python3.10
```

2.1. You can also use pyenv

```bash
curl -fsSL https://pyenv.run | bash
```

2.2. Documentation on how to set it up:\
https://github.com/pyenv/pyenv?tab=readme-ov-file#a-getting-pyenv


3. Create a virtual enviroment and activate it
```bash
python -m venv venv
source venv/bin/activate
```

4. Install the requirements
```bash
pip install -r requirements.txt
```

4.1. Install system dependencies
```bash
sudo apt update && sudo apt install -y fzf chafa aria2
```

5.Give Read, Write and Execute permissions to pyFlix
```bash
chmod +rwx pyFlix.py
```
## Usage

```bash
./pyFlix.py -h                                                                                                                                                                            
usage: pyFlix [-h] [-l LIMIT] [-q QUALITY] [-m MINIMUN_RATING] [-g GENRE] [-s SORT_BY] [-o ORDER_BY] [-w WITH_RT_RATINGS] [-v]

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

https://github.com/user-attachments/assets/ee174458-adce-464d-95bd-4248975f1505

## TODO:

- [ ] **How much time is left for downloading:** Display the remaining time for torrent downloads.
  
- [ ] **Multiple movie downloading:** Allow downloading multiple movies simultaneously.

- [ ] **Directly watching the movie:**
  - [ ] **Peerflix:** Stream the movie using **peerflix**.
  - [ ] **Making HTTP server for async downloading and uploading, then play with mpv:** Create an HTTP server to serve the file to **mpv** during async download/upload. needing PoC

- [ ] **Subtitle integration:** Add subtitle fetching as an argument to the command.


- [ ] **Dynamic resizing of fzf --preview-window (fucking impossible):** Make the `fzf` preview window dynamically resize based on the content.

- [ ] **Description, synopsis, and rating of movie in fzf --preview-window (fucking impossible):** Display detailed movie information (synopsis, description, and rating) inside the `fzf` preview window.


The program is not completely idiotproof, so please use it carefully, and open a issue if you find a dumb bug.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)
