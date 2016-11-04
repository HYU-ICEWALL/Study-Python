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
  ret = cmp(obj, tar)
  return ret

COMPILER = {'PY3': 'python3', 'PY2': 'python'}
VERSIONS = ['PY3', 'PY2']
import codecs
from subprocess import Popen, STDOUT, PIPE
def process(stamp, version):
  command = [COMPILER[version], stamp + '.py']
  with Popen(command, shell=True, stdin=open(stamp + '.in'), stdout=PIPE, stderr=PIPE) as p:
    ret, out = p.communicate()
  lines = len(out) and out.splitlines() or ret.splitlines()
  outfile = codecs.open(stamp + '.out', 'w', 'utf-8')
  for line in lines:
    if version=='PY3':
      outfile.write(line.decode('cp949'))
    else:
      outfile.write(line.decode('utf-8'))
    outfile.write('\r\n')
  outfile.close()
  return len(out) == 0

def scoring(program, pid, version='PY3', debug=False):
  stamp = pretreatment(program)
  generate_validation(pid, stamp)
  res = process(stamp, version)
  res = res and (isRight(stamp + '.out', stamp + '.vl') and 3 or 2) or 1 
  if res == 1:
    with open(stamp + '.out', 'r') as fh:
      for line in fh:
        ret = str(line).replace('\'', '`')
        ret = ret.replace(stamp, 'uploaded code')
  if not debug:
    aftertreatment(stamp)
  return (res, res == 1 and ret or "None")

def debug(program, pid, version):
  return scoring(get_path(PATH['UPL'] + [program]), pid, version, True)


from random import randrange
import datetime
def get_timestamp():
  stamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S')
  return str(randrange(100, 1000)) + '-' + stamp