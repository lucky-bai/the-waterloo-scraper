# The Waterloo Scraper

Website here: http://thewaterlooblogger.tk

This project scrapes the [list of blogs](https://github.com/rudi-c/the-waterloo-blogger) by Waterloo students once a day, and displays a feed of blogs that were recently updated.

Since I hastily put this together in a day or so, this website is not very robust. You are welcome to fix any bugs by submitting a pull request to this project.

## Deployment

This project can be run on an t2.nano instance on AWS. To set up:

1. Clone this github repository into the home directory `~`
2. In crontab, add: `0 8 * * * ~/the-waterloo-scraper/scraper/scrape_script.sh`
3. Open a tmux session, go to `/server/` and run `sudo make`
