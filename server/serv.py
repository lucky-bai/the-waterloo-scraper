import csv
import datetime
import operator
import os
import dateutil.parser
from flask import Flask
from flask import render_template

app = Flask(__name__)

PATH_TO_BLOG_METADATA = '../scraper/blogs.csv'
PATH_TO_PARSE_RESULTS = '../scraper/parse_results.csv'

BLOGS = []
RECENT_POSTS = []
LAST_UPDATED = None


@app.before_first_request
def load_data():
  """Load all the data structures into memory when Flask app starts"""
  global RECENT_POSTS
  global LAST_UPDATED

  # Read metadata
  csvr = csv.reader(open(PATH_TO_BLOG_METADATA))
  BLOGS.append(None)
  for url, author, program, tags in csvr:
    BLOGS.append((url, author, program, tags))

  # Read parse results
  csvr = csv.reader(open(PATH_TO_PARSE_RESULTS))
  csvr.next()
  for blog_num, ts in csvr:
    blog_num = int(blog_num)
    if ts not in ['empty', 'no_date']:
      dt = dateutil.parser.parse(ts)
      RECENT_POSTS.append((blog_num, dt))

  RECENT_POSTS = sorted(RECENT_POSTS, key=operator.itemgetter(1))
  RECENT_POSTS = list(reversed(RECENT_POSTS))
  
  LAST_UPDATED = datetime.datetime.fromtimestamp(
    os.path.getmtime(PATH_TO_PARSE_RESULTS)
  ).strftime('%a, %e %b %Y %H:%M:%S %z')


@app.route('/')
def index():
  data = []
  for blog_id, day in RECENT_POSTS:
    blog = BLOGS[blog_id]
    dayf = day.strftime('%B %d, %Y')
    blog_url = blog[0]
    author = blog[1]
    program = blog[2]
    data.append((dayf, blog_url, author, program))

  return render_template('index.html', data=data, last_updated=LAST_UPDATED)


if __name__ == '__main__':
  app.run('0.0.0.0', debug = True)
