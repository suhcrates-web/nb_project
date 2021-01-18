import requests
from datetime import date
import time, re
from bs4 import BeautifulSoup
import os, glob



def kospi200():
    today = date.today().strftime('%Y%m%d')
    filename = 'kos'+str(today)+'.csv'
    if not os.path.isfile('data/kospi200/'+filename):
        with open('data/kospi200/'+filename,'w') as f:
            for i in [1,2,3,4]:
                url = 'https://finance.naver.com/sise/sise_market_sum.nhn?page='+str(i)
                data = requests.get(url)
                content = BeautifulSoup(data.text, 'html.parser')
                trs = content.find('caption', text='코스피').find_next_sibling('tbody').find_all('tr')
                for i in trs:
                    try:
                        href= i.find('a', {'class':'tltle'})['href']

                        crpNumber = re.findall(r'(?<==)\d*$', href)[0]
                        crpName =i.find('a', {'class':'tltle'}).text
                        f.writelines([crpName, ',', crpNumber, '\n'])


                    except :
                        pass
                time.sleep(5)
    try:
        with open('data/kospi200/'+filename) as f:
            name_list= []
            num_list = []
            result = f.readlines()
            for i in result:
                i = i.split(',')
                name_list.append(i[0])
                num_list.append(i[1].strip())

    except:
        list = glob.glob('data/kospi200/*')
        latest = max(list, key= os.path.getctime)
        with open(latest) as f:
            name_list= []
            num_list = []
            result = f.readlines()
            for i in result:
                i = i.split(',')
                name_list.append(i[0])
                num_list.append(i[1].strip())
    return ({'name_list':name_list, 'num_list':num_list})

if __name__=="__main__":
    print(kospi200()["name_list"])