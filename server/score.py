from shutil import copyfile

def pretreatment(filename):
  timestamp = get_timestamp()
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

from subprocess import call
def process(filename, input):
  output = filename + ".out"
  call(['python3', filename], stdin=open(input), stdout=open(output, 'w'))
  return output

def scoring(program, validate):
  py = pretreatment(program)
  out = process(py, validate + '.in')
  ret = isRight(out, validate + '.out')
  aftertreatment(py)
  return ret

from random import randrange
import datetime
def get_timestamp():
  stamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d-%H%M%S.py')
  return str(randrange(100, 1000)) + '-' + stamp

# main
if __name__ == "__main__":
  print (scoring("test.py", "resources\\inspections\\0"))
