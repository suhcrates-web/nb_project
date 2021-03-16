from datetime import date, datetime
import math, re

from banolim import banolim
import pandas
import time
import re
from toolBox import jongsung, word_to_date, siljeok_gigan, inc_rate,  bodo_hm, dadum_tong_mun, dangsa
from kospi200_list import kos_list
import csv
start_time= time.time()
f = open('temp_con.html', 'r', encoding= 'utf-8')
f = f.read()

#
with open('test.txt', 'r', encoding= 'utf-8') as file:
    f = [x.rstrip() for x in file.readlines()]
    file.seek(0)
    fs = [x.rstrip().replace(' ','') for x in file.readlines()]
#
csv.register_dialect('pipes', delimiter = '|')
fr = []


print(f)

def saeop_bogoseo_alarm(f=None, fs=None, crpNm=None, sou_html=None, stock_code= None, url=None, **kwargs):
    list = ['은행','증권', '보험', '금융', '투자', '카드']
    ok = False
    for i in list:
        if bool(re.search(i, crpNm)):
            ok = True
    if ok:
        title = f'{crpNm} 사업보고서'
        article = ''

        #카카오 신호

        return {'title':title, 'article':article, 'table': ['사업연도', '모형등급']}
    else:
        raise Exception('증권 관련 아님')

end_time = time.time()
print((end_time-start_time))

if __name__ == "__main__":
    crpNm= '이마트'
    stockcode = '123'

    # print(result['title'])
    # print(result['article'])
    # temp = juju_byun(f=f, crpNm=crpNm)
    # print(temp['title'])
    # print(temp['article'])