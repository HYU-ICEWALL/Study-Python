PATH_SPLIT = '\\'
PATH = {
  "RES": ['resources'],
  "UPL": ['resources', 'upload'],
  "VAL": ['resources', 'validation'],
  "ASS": ['resources', 'assignments'],
  "TES": ['resources', 'test']
}

def get_path(path, end=False):
  path = PATH_SPLIT.join(path)
  if end: path += PATH_SPLIT
  return path

from generator import generate
def generate_validation(pid, stamp):
  generate(pid, stamp)

from shutil import copyfile
def pretreatment(filename):
  timestamp = get_path(PATH['TES'] + [get_timestamp()])
  copyfile(filename, timestamp + '.py')
  return timestamp

from os import remove
def aftertreatment(filename):
  remove(filename + '.py')
  remove(filename + '.in')
  remove(filename + '.vl')
  remove(filename + '.out')
  return 0

from filecmp import cmp
def isRight(obj, tar):
  return cmp(obj, tar)

COMPILER = {'PY3': 'python3', 'PY2': 'python'}
from subprocess import Popen, STDOUT
def process(stamp):
  command = [COMPILER['PY3'], stamp + '.py']
  proc = Popen(command, shell=True, stdin=open(stamp + '.in'), stdout=open(stamp + '.out' ,'w'), stderr=STDOUT)
  proc.communicate()[0]
  return proc.returncode == 0

def scoring(program, pid, debug=False):
  stamp = pretreatment(program)
  generate_validation(pid, stamp)
  res = process(stamp)
  res = res and (isRight(stamp + '.out', stamp + '.vl') and 3 or 2) or 1 
  if res == 1:
    with open(stamp + '.out', 'r') as fh:
      for line in fh:
        ret = str(line).replace('\'', '`')
        ret = ret.replace(stamp, 'uploaded code')
  if not debug:
    aftertreatment(stamp)
  return (res, res == 1 and ret or "None")

from random import randrange
import datetime
def get_timestamp():
  stamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')
  return str(randrange(100, 1000)) + '-' + stamp