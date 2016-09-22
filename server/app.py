import os
import markdown
from flask import Flask, render_template, Markup, request, flash, redirect, url_for

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

@app.route("/submit", methods=['GET', 'POST'])
def _submit():
  if request.method == 'POST':
    file = request.files['file']
    user_name = request.form['name']
    problem = request.form['problem']
    if file and user_name and problem and allowed_file(file.filename):
      nowstamp = get_timestamp()
      file_name = secure_filename(file. filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], nowstamp))
      file_size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'] + nowstamp))
      problem_id = int(get_problem_id(problem))
      query_db('INSERT INTO submissions (user_name, file_name, problem_id, size, process, score, stamp) VALUES (\'%s\', \'%s\', %d, %d, %d, %d, \'%s\')' % (user_name, file_name, problem_id, file_size, 0, 0, nowstamp), (), True)
      return redirect(url_for('_results'))
    else:
      if not user_name:
        flash('input name must')
      else:
        flash('file upload error')
  return render_template('submit.html', now="submit", problems=get_problems(['title']))

@app.route("/results")
def _results():
  return render_template('results.html', now="result", results=get_results())

@app.route("/results/<int:result_id>")
def _result(result_id):
  return render_template('result.html', now="result", id=result_id)
  
# for results
RESULT_COLUMN = ['id', 'user_name', 'file_name', 'problem_id', 'size', 'process', 'score']
def get_results():
  results = []
  for result in query_db('select * from submissions order by id desc'):
    result_dic = {}
    for (column, value) in zip(RESULT_COLUMN, result):
      result_dic[column] = value
    result_dic['problem_name'] = get_problem_name(result_dic['problem_id'])
    result_dic['result'] = result_dic['process'] == 1 and 'success' or 'danger'
    results.append(result_dic)
  return results

def make_submission(args):
  submission = {}
  return submission

# for problems
PROBLEM_FOLDER = 'resources/assignments/'
PROBLEM_ARGS = ['id', 'week', 'title', 'flag']
def get_problems(args=PROBLEM_ARGS):
  problems = []
  for each in os.listdir(PROBLEM_FOLDER):
    problem = {}
    for (arg, value) in zip(PROBLEM_ARGS, each.split('.')):
      if arg in args:
        problem[arg] = value
    problems.append(problem)
  return problems

def get_problem(id):
  return os.listdir(PROBLEM_FOLDER)[id]

def get_problem_name(id):
  return get_problem(id).split('.')[2]

def get_problem_content(id):
  problem = open(PROBLEM_FOLDER + get_problem(id), 'r')
  content = problem.read()
  problem.close()
  return content

def get_problem_id(name, target='title', find='id'):
  for problem in get_problems():
    if problem[target] == name:
      return problem[find]
  return -1

# for file process
from queue import Queue
qu = Queue()

def append_file(file_id):
  qu.put(file_id)

def process_file():
  id = qu.get()

# for file upload
from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['py'])
UPLOAD_FOLDER = 'resources/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# for utility
import datetime
def get_timestamp():
  return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')

# main
if __name__ == "__main__":
  app.secret_key = 'ICEWALL@PYTHON2016#'
  app.run(host='0.0.0.0', debug=False)
