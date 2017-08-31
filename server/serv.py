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


# This should probably be called only on startup, but it's tricky to invalidate
# the cache when the scraper re-runs. For now, load it on every request.
def load_recent_posts():
  blogs = []
  recent_posts = []

  # Read metadata
  csvr = csv.reader(open(PATH_TO_BLOG_METADATA))
  blogs.append(None)
  for url, author, program, tags in csvr:
    blogs.append((url, author, program, tags))

  # Read parse results
  csvr = csv.reader(open(PATH_TO_PARSE_RESULTS))
  csvr.next()
  for blog_num, ts in csvr:
    blog_num = int(blog_num)
    if ts not in ['empty', 'no_date']:
      dt = dateutil.parser.parse(ts)
      recent_posts.append((blog_num, dt))

  recent_posts = sorted(recent_posts, key=operator.itemgetter(1))
  recent_posts = list(reversed(recent_posts))
  
  last_updated = datetime.datetime.fromtimestamp(
    os.path.getmtime(PATH_TO_PARSE_RESULTS)
  ).strftime('%a, %e %b %Y %H:%M:%S %z')

  return blogs, recent_posts, last_updated


def load_all_blogs():
  blogs = []
  data = []

  # Read metadata
  csvr = csv.reader(open(PATH_TO_BLOG_METADATA))
  blogs.append(None)
  for url, author, program, tags in csvr:
    blogs.append((url, author, program, tags))

  # Read parse results
  csvr = csv.reader(open(PATH_TO_PARSE_RESULTS))
  csvr.next()
  csvr.next()
  for blog_num, ts in csvr:
    blog_num = int(blog_num)
    if ts in ['empty', 'no_date']:
      datestr = ts
    else:
      dt = dateutil.parser.parse(ts)
      datestr = dt.strftime('%B %d, %Y')

    data.append((blogs[blog_num][0], blogs[blog_num][1], datestr))

  last_updated = datetime.datetime.fromtimestamp(
    os.path.getmtime(PATH_TO_PARSE_RESULTS)
  ).strftime('%a, %e %b %Y %H:%M:%S %z')

  return data, last_updated


@app.route('/')
def index():
  blogs, recent_posts, last_updated = load_recent_posts()

  data = []
  for blog_id, day in recent_posts:
    blog = blogs[blog_id]
    dayf = day.strftime('%B %d, %Y')
    blog_url = blog[0]
    author = blog[1]
    program = blog[2]
    data.append((dayf, blog_url, author, program))

  return render_template('index.html', data=data, last_updated=last_updated)


@app.route('/blogs')
def blogs():
  data, last_updated = load_all_blogs()
  return render_template('blogs.html', data=data, last_updated=last_updated)


if __name__ == '__main__':
  app.run('0.0.0.0', port = 80, debug = True)
