import os
import markdown
from flask import Flask, render_template, Markup, request, flash, redirect, url_for

PATH_SPLIT = '\\'
RESOURCES = 'resources'

app = Flask(__name__)

@app.route("/")
def _home():
  return render_template('home.html', now="home")

@app.route("/login")
def _login():
  return "login"

@app.route("/logout")
def _logout():
  return redirect('/')

@app.route("/problems")
def _problems():
  return render_template('problems.html', now="problem", problems=get_problems())

@app.route("/problems/<int:problem_id>")
def _problem(problem_id):
  content = get_problem_content(problem_id)
  content = Markup(markdown.markdown(content))
  return render_template('problem.html', now="problem", id=problem_id, content=content)

from utility import VERSIONS
@app.route("/submit", methods=['GET', 'POST'])
def _submit():
  if request.method == 'POST':
    file = request.files['file']
    user_name = request.form['name']
    problem = request.form['problem']
    version = request.form['version']
    opensource = request.form.getlist('opensource') and True or False 
    if file and user_name.strip() and problem and allowed_file(file.filename):
      nowstamp = get_timestamp()
      file_name = secure_filename(file. filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], nowstamp))
      file_size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'] + nowstamp))
      problem_id = int(get_problem_id(problem))
      query_db('INSERT INTO submissions (user_name, file_name, problem_id, size, process, score, stamp, open, version) VALUES (\'%s\', \'%s\', %d, %d, %d, %d, \'%s\', %d, \'%s\')' % (user_name, file_name, problem_id, file_size, 0, 0, nowstamp, opensource and 1 or 0, version ), (), True)
      push_submission(get_submission(nowstamp))
      return redirect(url_for('_results'))
    else:
      if not user_name.strip():
        flash('input name must')
      else:
        flash('file upload error')
  return render_template('submit.html', now="submit", versions=VERSIONS, problems=get_problems(['title']))

RESULT_PER_PAGE = 15
@app.route("/results")
def _results():
  page = request.args.get('page')
  page = page and int(page) or 1
  if not page or page < 1: page = 1
  name = request.args.get('name')
  pages = [str(each + 1) for each in range(int((int(get_results_cnt(name)) - 1) / RESULT_PER_PAGE + 1))]
  results = get_results(page * RESULT_PER_PAGE, name)[-RESULT_PER_PAGE:]
  return render_template('results.html', now="result", name=name, results=results, pages=pages, page=str(page))

@app.route("/results/<int:result_id>")
def _result(result_id):
  result = get_result(result_id)
  if result['open'] or (result['process'] == "E" or result['process'] == "X"):
    content = get_result_content(result_id)
    result['content'] = content
    result['problem_ref'] = "/problems/" + str(result['problem_id'])
    return render_template('result.html', now="result", id=result_id, result=result)
  return redirect(url_for('_results'))
    
# for results
SUBMISSION_COLUMN = ['id', 'user_name', 'file_name', 'problem_id', 'size', 'process', 'score', 'stamp', 'open', 'result', 'version']
SUBMISSION_COLOR = ['warning', 'danger', 'danger', 'success']
SUBMISSION_MARK = ['...', 'E', 'X', 'O']
def get_results(n=0, name=None):
  fetch_process()
  query = 'SELECT id FROM submissions'
  if name:
    query += ' WHERE user_name = \'%s\'' % name
  query += ' ORDER BY id DESC LIMIT %d' % n
  results = [get_result(result) for result in query_db(query)]
  return results

def get_result(id):
  result_dic = {}
  result = query_db('SELECT * FROM submissions WHERE id=%d' % (id), (), False, True)
  for (column, value) in zip(SUBMISSION_COLUMN, result):
    result_dic[column] = value
  result_dic = pre_result(result_dic)
  return result_dic

def pre_result(result_dic):
  result_dic['problem_name'] = get_problem_name(result_dic['problem_id'])
  result_dic['result_class'] = SUBMISSION_COLOR[result_dic['process']]
  result_dic['process'] = SUBMISSION_MARK[result_dic['process']]
  result_dic['open'] = result_dic['open'] == 1
  result_dic['href'] = '/results/' + str(result_dic['id'])
  if result_dic['result'] == "None": result_dic['result'] = "Wrong Answer"
  result_dic['name_search'] = '/results?name=' + str(result_dic['user_name'])
  return result_dic

def get_result_content(id):
  stamp = query_db('SELECT stamp FROM submissions WHERE id=%d' % (id), (), False, True)[0]
  file = open(get_path(PATH['UPL'] + [stamp]), 'r')
  result = file.read()
  file.close()
  return result

def get_results_cnt(name=None):
  query = 'SELECT COUNT(*) FROM submissions'
  if name:
    query += ' WHERE user_name = \'%s\'' % name
  cnt = query_db(query, (), False, True)[0]
  return cnt

def make_submission(args):
  submission = {}
  return submission

# for problems
PROBLEM_ARGS = ['id', 'week', 'title', 'flag']
def get_problems(args=PROBLEM_ARGS):
  problems = []
  for each in os.listdir(get_path(PATH['ASS'], True)):
    problem = {}
    for (arg, value) in zip(PROBLEM_ARGS, each.split('.')):
      if arg in args:
        problem[arg] = value
    problems.append(problem)
  return problems

def get_problem(id):
  return os.listdir(get_path(PATH['ASS'], True))[id]

def get_problem_name(id):
  return get_problem(id).split('.')[2]

def get_problem_content(id):
  problem = open(get_path(PATH['ASS'] + [get_problem(id)]), 'r', encoding="utf-8")
  content = problem.read()
  problem.close()
  return content

def get_problem_id(name, target='title', find='id'):
  for problem in get_problems():
    if problem[target] == name:
      return problem[find]
  return -1

# for submission
from utility import scoring, get_path, PATH
from queue import Queue
from threading import Thread
class validate(Thread):
  def __init__(self, submit, result):
    Thread.__init__(self)
    self.submit = submit
    self.result = result

  def run(self):
    while True:
      submission = self.submit.get()
      (ret, res)  = scoring(get_path(PATH['UPL'] + [submission['stamp']]), submission['problem_id'], submission['version'])
      self.submit.task_done()
      self.result.put({'id': submission['id'], 'process': ret, 'result': res})

queue_submit = Queue()
queue_result = Queue()
def fetch_process():
  while not queue_result.empty():
    result = queue_result.get()
    query = 'UPDATE submissions SET process=%d WHERE id=%d' % (result['process'], result['id'])
    query_db(query, (), True)
    query = 'UPDATE submissions SET result=\'%s\' WHERE id=%d' % (result['result'], result['id'])
    query_db(query, (), True)

def push_submission(submission):
  queue_submit.put(submission)
  thread = validate(queue_submit, queue_result)
  thread.start()

def get_submission(filename):
  result_dic = {}
  results = query_db('SELECT * FROM submissions WHERE stamp = \'%s\'' % (filename), (), False, True)
  for (column, result) in zip(SUBMISSION_COLUMN, results):
    result_dic[column] = result
  return result_dic

# for file upload
from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['py'])
app.config['UPLOAD_FOLDER'] = get_path(PATH['UPL'], True)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# for database 
import sqlite3
from flask import _app_ctx_stack

DATABASE = 'app.db'
SCHEMA = 'schema.sql'
def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource(SCHEMA, 'r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def get_db():
  top = _app_ctx_stack.top
  if not hasattr(top, 'sqlite_db'):
    top.sqlite_db = sqlite3.connect(DATABASE)
  return top.sqlite_db

def query_db(query, args=(), commit=False, one=False):
  db = get_db()
  cur = db.execute(query, args)
  if commit:
    db.commit()
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
  top = _app_ctx_stack.top
  if hasattr(top, 'sqlite_db'):
    top.sqlite_db.close()

def patch():
  l = query_db('SELECT id FROM submissions WHERE process=1')
  for e in l:  
    submission = {}
    results = query_db('SELECT * FROM submissions WHERE id = %d' % (e[0]), (), False, True)
    for (column, result) in zip(SUBMISSION_COLUMN, results):
      submission[column] = result
    validation = get_path(PATH['INS'] + [str(submission['problem_id'])])
    (ret, res)  = scoring(get_path(PATH['UPL'] + [submission['stamp']]), validation)
    queue_result.put({'id': submission['id'], 'process': res=="None" and 2 or 1, 'result': res})
  fetch_process()

# for utility
import datetime
from random import randrange
def get_timestamp():
  stamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')
  return str(randrange(100, 1000)) + '-' + stamp 

# main
if __name__ == "__main__":
  app.secret_key = 'ICEWALL@PYTHON2016#'
  app.run(host='0.0.0.0', debug=False)
