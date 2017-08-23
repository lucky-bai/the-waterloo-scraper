#!/bin/bash
# This script is called from cron to scrape everything.

SCRAPER_ROOT=`dirname $(realpath $0)`
cd $SCRAPER_ROOT

rm -r data
rm parse_results.csv

mkdir data

python 01-scrape_all_blogs.py
python 02-parse_blog_dates.py
