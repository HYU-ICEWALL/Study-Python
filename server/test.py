from score import scoring
PATH_SPLIT = '\\'
def test(obj, tar):
	print (scoring("resources" + PATH_SPLIT + "test" + PATH_SPLIT + obj + ".py", "resources" + PATH_SPLIT + "inspections" + PATH_SPLIT + tar, True))

from shutil import copyfile
def test_get(obj, tar):
  copyfile("resources" + PATH_SPLIT + "upload" + PATH_SPLIT + obj, "resources" + PATH_SPLIT + "test" + PATH_SPLIT + tar + ".py")

import sys
if __name__ == '__main__':
	if len(sys.argv) == 1:
		print ("""
-c copy uploaded file to test
-t test test file
""")
	elif sys.argv[1] == "-c":
		test_get(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "-t":
		test(sys.argv[2], sys.argv[3])