PATH_SPLIT = '\\'
PATH = {
  "RES": ['resources'],
  "INS": ['resources', 'inspections'],
  "UPL": ['resources', 'upload'],
  "VAL": ['resources', 'validation'],
  "ASS": ['resources', 'assignments'],
  "TES": ['resources', 'test']
}

def get_path(path, end=False):
  path = PATH_SPLIT.join(path)
  if end: path += PATH_SPLIT
  return path

from shutil import copyfile
def pretreatment(filename):
  timestamp = get_path(PATH['TES'] + [get_timestamp()])
  copyfile(filename, timestamp)
  return timestamp

from os import remove
def aftertreatment(filename):
  remove(filename)
  remove(filename+'.out')
  return 0

from filecmp import cmp
def isRight(obj, tar):
  return cmp(obj, tar)

COMPILER = {'PY3': 'python3', 'PY2': 'python'}
from subprocess import Popen, STDOUT
def process(filename, input):
  output = filename + ".out"
  command = [COMPILER['PY3'], filename]
  proc = Popen(command, shell=True, stdin=open(input), stdout=open(output ,'w'), stderr=STDOUT)
  proc.communicate()[0]
  exit = proc.returncode
  return (exit == 0, output)

def scoring(program, validate, debug=True):
  py = pretreatment(program)
  (res, out) = process(py, validate + '.in')
  res = res and (isRight(out, validate + '.out') and 3 or 2) or 1 
  if res == 1:
    with open(out, 'r') as fh:
      for line in fh:
        ret = str(line).replace('\'', '`')
        print(py)
        ret = ret.replace(py, 'uploaded code')
  if not debug:
    aftertreatment(py)
  return (res, res == 1 and ret or "None")

from random import randrange
import datetime
def get_timestamp():
  stamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S.py')
  return str(randrange(100, 1000)) + '-' + stamp

# main
if __name__ == "__main__":
  print (scoring("test.py", "resources/inspections/0"))
