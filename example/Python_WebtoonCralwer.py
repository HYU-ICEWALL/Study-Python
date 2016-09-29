
# coding: utf-8

# # Python으로 웹툰 파싱하기

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

# 이 코드는 다른 요일의 웹툰 목록도 확인해보고 싶을때 사용할 수 있습니다.
weeks = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
week = weeks[0]


# In[3]:

res = urlopen('http://comic.naver.com/webtoon/weekdayList.nhn?week=' + week)
raw = bs(res, 'lxml')
res.close()


# ### 웹툰 목록을 담고있는 div를 가져옵니다.
# 웹툰이 들어있는 `div`들을 잘 살펴보면 모든 웹툰 목록을 감싸는 `div`는 아래의 `div`입니다.
# ```
# <div class="list_area daily_img">
# ```
# 따라서 class이름이 list_area인것을 골라옵니다.

# In[9]:

div = raw.body.findAll('div', {'class': 'list_area'})[0]


# ### 각 웹툰을 가져오기
# `<li>`태그가 웹툰 하나를 감싸고 있는것을 확인할 수 있습니다.
# 
# 따라서 위에서 구한 div에서 li들을 모두 찾으면 각 웹툰 정보를 감싸는 li태그들이 담긴 리스트를 반환받을 수 있습니다.

# In[10]:

toons = div.findAll('li')


# ### 각 웹툰정보에서 이름만 가져오기
# 이제 각 줄을 반복하면서 이름을 가져오면 됩니다.
# 
# 웹툰 이름은 `li`태그 안에 `dl`태그 안에 `dt`태그 안에 `a`태그로 감싸져 있는 것을 알 수 있습니다.
# 이렇게 하나하나 접근해도 되지만 너무 귀찮고 `li`태그안에 `dt`태그가 여럿 있지 않으므로 바로 `dt`태그로 가져오겠습니다.

# In[13]:

for toon in toons:
    dt = toon.findAll('dt')[0]
    print (dt.string)


# In[ ]:



