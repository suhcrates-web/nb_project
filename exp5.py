import requests
from bs4 import BeautifulSoup

url0 = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20210901800227'
content = requests.get(url0)  # .content.decode('utf-8')
content = BeautifulSoup(content.text, 'html.parser')
print(content)