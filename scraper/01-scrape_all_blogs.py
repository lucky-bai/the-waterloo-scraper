# This script scrapes each blog once and passes result through html2text

import os
import csv

SCRAPE_CMD = "wget '%s' -O index.html; html2text index.html > data/%d.txt; rm index.html"

def main():
  csvr = csv.reader(open('blogs.csv'))

  blog_ix = 0
  for blog_url, _, _, _ in csvr:
    blog_ix += 1

    print "SCRAPING:", blog_url
    os.system(SCRAPE_CMD % (blog_url, blog_ix))
  

main()
