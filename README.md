# WhiskyMetrics
## Tools for downloading whisky reviews from Reddit's r/Scotch

### Setup
1. Before you use WhiskyMetrics' tools you'll need to download [this](https://docs.google.com/spreadsheets/d/1X1HTxkI6SqsdpNSkSSivMzpxNT-oeTbjFFDdEkXD30o/edit#gid=695409533) Google spreadsheet as a CSV file named `whisky_reviews.csv`. (It's not worth my while to come up with a way to do this programmatically, but if you make one, I'll gladly accept your pull request!)

2. Next, we'll take the data in the csv file we have downloaded and put that into a SQLite database named `singlemalt.db`. Create the database using the script `populateDB.py`. The database consists of a single table called `review` created as
```
create table if not exists review(
                        name text, --whisky name
                        region text, --region in Scotland where it was produced
                        postID text, --reddit post ID
                        score integer --review score
                        );
```
The other WhiskyMetrics scripts interface with this database.

### Scrape, Scrub and Fextract
Whiskymetrics' key functionalities are implemented by these scripts.

`scrape.py` is an executable script which queries the database for post IDs associated with the distillery, region or whisky specified in the input, gets the reddit comment with said post IDs and stores the comment text in .txt files whose names are the same as the post IDs. The files are stored in a directory named`{whisky|distillery|region}_<whisky_name>`. 

Usage:
```
scrape.py [-h] [--type {1,2,3}] search_string
positional arguments:
  search_string   Whisky, region or ditillery you want to get reviews of.

optional arguments:
  -h, --help      show this help message and exit
  --type {1,2,3}  1, 2 or 3 depending on whether your search string specifies
                  a distillery name, a whisky producing region or the name of
                  a particular whisky. Is set to 3 by default.
```

`scrub.py` Processes the review files creates by the scrapereviews command of the Wiskymetrics toolkit. All text is converted to lowercase and special characters are removed. The script takes as its input a folder name, processes all text files in it and adds a SCRUBBED flag to the METADATA file.

Usage: 
```
scrub.py [-h] dir_name

positional arguments:
  dir_name    Name of the folder containing the review files created by scrape.py to be
              scrubbed.

optional arguments:
  -h, --help  show this help message and exit
```

`fextract.py` iterates through the files in the folder created by scrape.py and extracts term frequencies (TF) of words associated with four whisky characteristics, namely, colour, nose, taste and finish. The data are stored in JSON in a directory called JsonDumps. The JSON files have the same name as the folder specified in the command line argument.

Usage:
```
fextract.py [-h] dir_name

positional arguments:
  dir_name    Name of the folder containing the review files.

optional arguments:
  -h, --help  show this help message and exit
```
The above scripts can also be imported as modules. 
