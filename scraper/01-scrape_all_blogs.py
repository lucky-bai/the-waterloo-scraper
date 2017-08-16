# This script scrapes each blog once and passes result through html2text

import os

SCRAPE_CMD = "wget %s; html2text index.html > data/%d.txt; rm index.html"

def main():
  blog_urls = map(lambda x:x[:-2], open('blogs.txt').readlines())

  blog_ix = 0
  for blog_url in blog_urls:
    blog_ix += 1

    # Skip all medium blogs because medium is blocked in Malaysia
    if 'medium.com' in blog_url:
      continue

    print "SCRAPING:", blog_url
    os.system(SCRAPE_CMD % (blog_url, blog_ix))
  

main()
