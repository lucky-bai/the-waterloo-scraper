# This script looks for dates in scraped blog posts, using the datefinder package.

import os
import datetime
import operator
import datefinder


def process_file(blog_num):
  contents = open('data/%d.txt' % blog_num).read()
  contents = contents.replace('_', ' ')

  dates_found = list(datefinder.find_dates(contents, strict=True))
  latest_post_date = most_recent_date(dates_found)

  return latest_post_date


def most_recent_date(dates):
  """Look for the most recent date that's not in the future and less than 1 year old"""
  best_found = None
  for d in dates:
    if d > datetime.datetime.now():
      continue
    if d < datetime.datetime.now() - datetime.timedelta(days = 365):
      continue
    
    if not best_found:
      best_found = d
    else:
      if d > best_found:
        best_found = d

  return best_found


def main():
  blogs_and_post_dates = []

  # Look at every file in ./data/ directory which contains scraped pages
  for filename in os.listdir('./data'):
    if filename.endswith('.txt'):
      blog_num = int(filename[:-4])
      latest_post_date = process_file(blog_num)
      if latest_post_date:
        blogs_and_post_dates.append((blog_num, latest_post_date))

  blogs_and_post_dates = sorted(blogs_and_post_dates, key=operator.itemgetter(1))
  print blogs_and_post_dates
      

main()
