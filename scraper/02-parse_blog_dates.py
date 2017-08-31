# This script looks for dates in scraped blog posts, using the datefinder package.

import os
import csv
import datetime
import operator
import datefinder


def process_file(blog_num):
  contents = open('data/%d.txt' % blog_num).read()
  contents = contents.replace('_', ' ')
  for year in xrange(2010, 2020):
    contents = contents.replace(str(year), str(year) + '. ')

  dates_found = list(datefinder.find_dates(contents, strict=True))
  latest_post_date = most_recent_date(dates_found)

  return latest_post_date


def most_recent_date(dates):
  """Look for the most recent date that's not in the future and less than 1 year old"""
  best_found = None
  for d in dates:
    if d > datetime.datetime.now():
      continue
    
    if not best_found:
      best_found = d
    else:
      if d > best_found:
        best_found = d

  return best_found


def main():
  csvw = csv.writer(open('parse_results.csv', 'w'))
  csvw.writerow(['blog_id', 'latest_post_date'])

  results = []
  
  # Look at every file in ./data/ directory which contains scraped pages
  for filename in os.listdir('./data'):
    if filename.endswith('.txt'):
      blog_num = int(filename[:-4])
      latest_post_date = process_file(blog_num)

      if latest_post_date:
        results.append((blog_num, latest_post_date))
      elif os.stat('data/' + filename).st_size == 0:
        results.append((blog_num, 'empty'))
      else:
        results.append((blog_num, 'no_date'))

  results = sorted(results)
  for row in results:
    csvw.writerow(row)
      

main()
