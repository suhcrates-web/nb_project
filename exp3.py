from datetime import date, datetime
import math, re

from banolim import banolim
import pandas
import time
import re
from toolBox import jongsung, word_to_date, siljeok_gigan, inc_rate

start_time= time.time()

with open('test.txt', 'r', encoding= 'utf-8') as file:
    f = [x.rstrip() for x in file.readlines()]
    file.seek(0)
    fs = [x.rstrip().replace(' ','') for x in file.readlines()]




def juju_state(f=None, crpNm=None, sou_html=None, **kwargs):

    #보고자 한글명칭
    bogoja = f[f.index('한글')+1]


    #국민연금공단꺼 아니면 안냄.

    if bogoja in ['국민연금공단']:
        songgo =True
        bogoja = re.sub(r'공단$','',bogoja)
    else:
        raise Exception('중요한 회사가 아님')

    opCorp = f[f.index('회 사 명')+1].replace('(주)','').replace('㈜','')
    today = date.today().day

    jeung_su = f[f.index('증감')+3]
    jeung_bi = f[f.index('증감')+4]
    if float(jeung_bi) >0:
        do_su = '매수'
        plma = '확대'
    else:
        do_su = '매도'
        plma = '축소'

    def to_date(date_word):
        if bool(re.search('월',date_word)):
            date_word = datetime.strptime(date_word, '%Y년%m월%d일')
        else:
            date_word = datetime.strptime(date_word, '%Y.%m.%d')
        return date_word

    if f[f.index('직전보고서')+1] not in ['-', '']:
        new = False
    else:
        new = True #주식 새로 확보

    date_ment = ''

    eebeon= to_date(f[f.index('이번보고서')+1].replace(' ',''))
    if not new:
        jikjeon= f[f.index('직전보고서')+1].replace(' ','')
        jikjeon = to_date(jikjeon)

        date_ment += '지난 '
        before = False
        if jikjeon.year != eebeon.year:
            date_ment += str(jikjeon.year) +'년 '
            before = True
        if jikjeon.month != eebeon.month:
            date_ment += str(jikjeon.month) +'월'
            before = True
        date_ment += str(jikjeon.day) +'일에서 '


        if before:
            date_ment +='이번 '
        date_ment += str(eebeon.day)+'일 사이'
    else:
        date_ment += eebeon.day +'일 기준으로'

    bi_ment = ''
    ee_su = f[f.index('이번보고서')+4]
    ee_bi = f[f.index('이번보고서')+5]
    if not new:
        jeon_su = f[f.index('직전보고서')+4]
        jeon_bi = f[f.index('직전보고서')+5]
        bi_ment = '{}%({}주)에서 {}%({}주)로 {}됐다'.format(jeon_bi, banolim(jeon_su,'원','일'), ee_bi ,banolim(ee_su,'원','일'),
                                                     plma)
    else:
        bi_ment = '{}%({})이 됐다'.format(ee_bi ,banolim(ee_su,'원','일'))

    title =''
    if bogoja in ['국민연금']:
        title += '['+bogoja+']'
    else:
        title += bogoja +', '

    if not new:
        title += '{} 주식 {}% {}...지분 {}% → {}%'.format(opCorp, jeung_bi, do_su, jeon_bi, ee_bi)

    else:
        title += '{} 주식 {} {}...지분 {}%'.format(opCorp, banolim(jeung_su,'원','만'), ee_bi)

    article = """
    {}{} {}의 총 주식 수의 {}%({}주)를 장내 {}했다고 {}일 공시했다.<br><br>
    이에 따라 지분은 {} {}.
    """.format(bogoja, jongsung(bogoja,'은는'), opCorp, jeung_bi, banolim(jeung_su,'원','일'), do_su, today, date_ment,
               bi_ment )

    return {'title':title, 'article':article, 'table': ['보고서<br/>', '이번보고서']}



if __name__ == "__main__":
    print(f)
    a = juju_state(f=f, fs=fs, crpNm='금호산업')

    end_time = time.time()

    print(a['title'])
    print(a['article'])
    print(end_time-start_time)
