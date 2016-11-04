from random import randrange, choice

def write(f, text):
	f.write(text+'\n')

def isPrime(n):
    for i in range(2, int(n**0.5) + 1):
        if not n % i:
            return False
    return True

def primenumber(fin, fou):
	for i in range(2, 10000):
		if isPrime(i):
			write(fou, str(i))
	fin.close()
	fou.close()

def primedistinction(fin, fou):
	for _ in range(100):
		n = randrange(10, 10000)
		write(fin, str(n))
		write(fou, (isPrime(n) and '1' or '0'))
	fin.close()
	fou.close()

def thenumberoffruits(fin, fou):
	alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
	action = ['a', 'm', 's']
	n = randrange(88, 99)
	write(fin, str(n))
	s = {}
	for _ in range(n):
		name = "".join([alpha[randrange(0, len(alpha))] for _ in range(randrange(5, 10))])
		count = randrange(0, 100)
		s[name] = count
		write(fin, name + ' ' + str(count))
	m = randrange(8888, 9999)
	write(fin, str(m))
	k = list(s)
	for _ in range(m):
		act = choice(action)
		command = [act]
		if act == 'a':
			tar = choice(k)
			command.append(tar)
			obj = randrange(-100, 100)
			command.append(str(obj))
			s[tar] += obj
		elif act == 'm':
			tar = choice(k)
			command.append(tar)
			obj = randrange(-100, 100)
			command.append(str(obj))
			s[tar] -= obj
		elif act == 's':
			tar = choice(k)
			command.append(tar)
			write(fou, str(s[tar]))
		write(fin, " ".join(command))

def webtooncrawler(fin, fou):
	from bs4 import BeautifulSoup as bs
	from urllib.request import urlopen
	url = 'http://comic.naver.com/webtoon/weekdayList.nhn?week='
	weeks = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

	n = randrange(10, 15)
	write(fin, str(n))
	for _ in range(n):
		query = choice(weeks)
		write(fin, query)
		res = urlopen(url + query)
		txt = bs(res, 'lxml')
		res.close()
		write(fou, ", ".join([ t.findAll('dt')[0].string for t in txt.body.findAll('div', {'class': 'list_area'})[0].findAll('li') ]))

	fin.close()
	fou.close()

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
def gen_str(i):
    return "".join([alpha[randrange(0, len(alpha))] for _ in range(i)])
def gen_key(s, e, count):
    ret = set()
    while (len(ret) < count):
        ret.add(randrange(s, e))
    return ret
def insert(ks, s, p):
    for k in ks:
        s = s[k:] + p + s[:k]
    return s
def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)
def stringparser(fin, fou):
	n = randrange(45, 50)
	write(fin, str(n))
	for _ in range(n):
		word = gen_str(randrange(10, 20))
		text = gen_str(randrange(500, 750))

		text = insert(gen_key(1, len(text) - 1, randrange(200, 250)), text, ' ')
		text = insert(gen_key(0, len(text), randrange(10, 200)), text, ' ' + word + ' ')

		write(fin, word)
		write(fin, text)

		keys = sorted(list(find_all(text, ' ' + word + ' ')) + list(find_all(text, ' ' + word)) + list(find_all(text, word+' ')))
		
		if (text[:len(word)] != word):
			write(fou, '--'.join(text[:keys[0]].split()))
		else:
			write(fou, '')

		if (text[-len(word):] != word):
			write(fou, '--'.join(text[keys[-1] + len(word) + 1:].split()))
		else:
			write(fou, '')

	fin.close()
	fou.close()

def queue(fin, fou):
	action = ['put', 'get']
	n = randrange(8888, 9999)
	q = []
	qi = 0
	write(fin, str(n))
	for _ in range(n):
		act = choice(action)
		write(fin, act)
		if act == 'put':
			num = randrange(-10000, 10000)
			write(fin, str(num))
			q.append(num)
		elif act == 'get':
			if len(q) > qi:
				write(fou, str(q[qi]))
				qi+=1

	write(fou, str(len(q) - qi))
	fin.close()
	fou.close()

def stack(fin, fou):
	action = ['put', 'get']
	n = randrange(8888, 9999)
	q = []
	write(fin, str(n))
	for _ in range(n):
		act = choice(action)
		write(fin, act)
		if act == 'put':
			num = randrange(-10000, 10000)
			write(fin, str(num))
			q.append(num)
		elif act == 'get':
			if len(q):
				write(fou, str(q.pop()))

	write(fou, str(len(q)))
	fin.close()
	fou.close()

def prefix(fin, fou):
	return 0

def postfix(fin, fou):
	return 0

problems = [
	primenumber,
	primedistinction,
	thenumberoffruits,
	webtooncrawler,
	stringparser,
	queue,
	stack,
	prefix,
	postfix
]

def generate(pid, stamp):
	problems[pid](open(stamp + '.in', 'w'), open(stamp + '.vl', 'w', encoding = 'utf8'))