# 2주차, 문자열 다루기

### 스터디 내용
오늘 스터디에서 사용한 패키지는 `BeautifulSoup4`와 `lxml`입니다.

아래의 코드로 설치할 수 있습니다.
```
  $ pip install bs4
  $ pip install lxml
```
*윈도우 사용자는 `lxml`이 제대로 설치되지 않을겁니다. [링크](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)에서 자신의 버전에 맞는 whl파일을 다운로드 한 후 pip으로 설치하면 됩니다.*

오늘은 웹페이지에서 원하는 데이터를 골라내는 작업을 했습니다.
사실 코딩을 한땀 한땀 사용해서 원하는 데이터를 골라내는 것도 파이썬과 함께 라면 그렇게 어려운 작업은 아닙니다. 하지만 파이썬을 더 쉽게 사용하기 위해 다른 사람들이 만들어 놓은 훌륭한 라이브러리들이 많이 있습니다. 오늘 우리는 그것들 중 beautifulsoup를 사용해 볼 것입니다.

[BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)를 참고해 더 많은 기능에 대해서 알아볼 수 도 있습니다.

웹페이지에서 우리가 원하는 내용을 빨리 찾아내기 위해서는 개발자도구를 잘 활용해야 합니다. 크롬을 사용하고 있다면 우클릭후 `검사`메뉴를 누름으로 간단하게 어떤 태그들로 감싸져있고 어떤 이름을 가지고 있는지 확인할 수 있습니다.

어떤 데이터를 가져올지 정했다면 그 데이터까지 어떻게 접근해야 하는지도 생각해보아야 합니다.

상위에는 어떤 태그가 있고 중복 되는 것은 없는지, 혹은 중복되는 것들을 이용하여 더 빠르고 간단한 처리 과정을 만들 수는 없는지는 많이 해보면 실력이 늘게 됩니다.

어떻게 접근할지 생각해 보았으면 코드로 옮기면 됩니다.
코드 내용은 무척 짧고 생각하는 부분이 더 중요하기 때문에 예제 코드를 보면서 실습을 많이 해보는것이 중요합니다.

- [파이썬 크롤러 예제 코드](https://gist.github.com/MaybeS/24e4473271db1e6770bb22f2a2b7e9cc)
- [파이썬 웹툰 크롤러 예제 코드](https://gist.github.com/MaybeS/33aecfcd82b5617c131c88797056726c)

### 숙제
- 네이버 웹툰 목록을 출력하는 프로그램을 만듭니다.
  - n이 주어지고 다음 n개의 줄에 `'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'`중 하나가 주어집니다. 주어진 요일에 맞는 웹툰 목록을 출력하면 됩니다.
  - 출력할 때 각 목록 사이에 ', ' 가 들어가도록 하면 됩니다.
  - 입력예시

  ```
    2
    mon
    tue
  ```
  - 출력예시

  ```
대학일기, 신의 탑, 뷰티풀 군바리, 소녀의 세계, 평범한 8반, 마이너스의 손, 여중생A, 썸남, 윈드브레이커, 이상하고 아름.., 윈터우즈, MZ, 하루 3컷, 부부생활, 가우스전자 시.., 첩보의 별, 203호 저승.., 생활의참견, 탈(TAL), 팀피닉스, 크리퍼스큘, 3P, 동토의 여명, 히어로메이커, 나의 인생샷을..
노블레스, 마음의소리, 하이브3, 귀도, 투명한 동거, 체크포인트, 오!주예수여, 놓지마 정신줄.., 신도림, 제로게임, 슈퍼 시크릿, 메달 브레이커, 차원이 다른 .., 모태솔로수용소.., 하루 3컷, 가우스전자 시.., 덴마, 심연의 하늘 .., 신의 언어, 미라클! 용사님, 윌유메리미, 죽은 마법사의.., 에이머, 패밀리 사이즈, 기로, 한국만화거장전.., 러브슬립 2부

  ```
