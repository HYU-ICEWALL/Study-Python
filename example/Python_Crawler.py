
# coding: utf-8

# # Python으로 웹페이지 파싱하기

# ### 필요한 패키지들을 가져옵니다.
# bs4는 BeautifulSoup로 좀 더 간편하게 파싱을 도와줍니다.
# lxml은 beautifulsoup와 같이 사용됩니다.

# In[1]:

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
# from urllib import urlopen -for- python <= 2.7


# ### 데이터를 가져옵니다
# url에 request를 날려서 파싱할 데이터를 가져옵니다.

# In[2]:

res = urlopen('http://maynet.iptime.org:5000/results')
raw = bs(res, 'lxml')
res.close()


# ### 테이블을 가져옵니다.
# 랭킹이 들어있는 테이블을 잘 살펴보면 
# ```
# <table class="table table-hover" id="rank">
# ```
# 과 같은 형태를 발견할 수 있는데 class가 table 혹은 table-hover인걸로 찾아도 되지만 보통 id를 selector라고 해서 찾을 때 주로 사용합니다.
# 따라서 id가 'rank'인 태그를 가져옵니다.

# In[3]:

table = raw.body.find(id='rank')


# ### 각 줄을 가져오기
# `<tr>`태그는 마크업 언어에서 테이블의 각 줄을 나타내는데 사용됩니다. 우리는 한 줄에있는 이름을 가져오고 싶으므로 각줄에 먼저 접근해야 합니다.

# In[4]:

lines = table.findAll('tr')


# ### 각 줄에서 이름을 추려내기
# 이제 각 줄을 반복하면서 이름을 가져오면 됩니다.
# 한 줄에는 5개의 칼럼이 있고 이름은 그중에서 3번째 이므로 `td`태그들을 다 찾고 그중에서 3번째를 가져옵니다.
# 
# 이제 이름은 하나의 `td`태그안에 `a`태그 로 감싸져 있습니다. 이 때 `a`태그를 굳이 넣어서 찾는 이유는 그렇게 하지 않으면 맨 첫줄의 Name도 출력될 것이기 때문입니다.

# In[5]:

for line in lines:
    td = line.findAll('td')[2]
    a = td.findAll('a')
    if a:
        print(a[0].string)


# In[ ]:



