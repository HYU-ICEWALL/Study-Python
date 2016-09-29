from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
url = 'http://comic.naver.com/webtoon/weekdayList.nhn?week='
weeks = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

n = int(input())
for _ in range(n):
	q = input()
	r = urlopen(url + q)
	t = bs(r, 'lxml')
	r.close()
	print(", ".join([ tt.findAll('dt')[0].string for tt in t.body.findAll('div', {'class': 'list_area'})[0].findAll('li') ]))
