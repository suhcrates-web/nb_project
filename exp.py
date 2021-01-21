from datetime import date, datetime
import math, re

from exp4 import banolim
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

def juju_byun(f=None, crpNm=None, sou_html=None, stock_code= None, **kwargs):
    corpNm = crpNm
    today = date.today().day
    ####구자영씨 등 최대주주 친인척 6명######
    #'성명'을 경계로  매도자가 나뉨. 마지막 성명은 '5.주식소유현황' 첫머리.
    n = 0
    n_list =[]
    for i in f:
        if i == '성명':
            n_list.append(n)
        n +=1
    #개인 리스트
    gain_list = []
    for i in range(0, len(n_list)-1):
        start = n_list[i]
        end = n_list[i+1]
        gain_list.append(f[start:end])

    gain_dict = [] #개인별 정보
    relate_list = {} #관계별로 묶음
    for i in gain_list:
        #gain_dict 작성구간
        temp = {}
        temp['성명'] =  i[i.index('성명')+1]
        temp['관계'] = i[i.index('최대주주 및 발행회사와의 관계')+1]
        gain_dict.append(temp)

        #relate_list 작성구간
        if temp['관계'] not in relate_list.keys():
            relate_list[temp['관계']] =  [temp['성명']]
        else:
            relate_list[temp['관계']] =relate_list[temp['관계']] +  [temp['성명']]
        #예) relate_list = {'친인척': ['구자영', '이재원', '이욱진', '유웅선', '유준선', '유희영']}

    #매도·매수자
    relate_ment = ''
    for i in  relate_list.keys():
        temp_ment=''
        if i not in ['본인', '기타']:
            temp_ment = '{} 관계인 '.format(i)
        list = relate_list[i]
        if len(list)>1:

            relate_ment += list[0]+' 등 '+ temp_ment + ' 최대주주 ' +  str(len(list))+'명, '
        else:
            relate_ment += temp_ment + '최대주주 ' + list[0]+ ', '
    relate_ment = relate_ment[:-2]
    #구자영 등 친인척 관계의 최대주주 6명


    ####보통주 28만9272주 #######
    jusic = {}

    if float(f[f.index('증감')+2]) !=0:
        jusic['보통주'] =  float(f[f.index('증감')+2])  #보통주
    if float(f[f.index('증감')+5]) != 0:
        jusic['종류주'] = float(f[f.index('증감')+5]) #종류주
    if float(f[f.index('증감')+8]) != 0:
        jusic['증권예탁증권'] = float(f[f.index('증감')+8]) #증권예탁증권
    jusic_tot = float(f[f.index('증감')+11]) #합계
    su_do = '매수' if jusic_tot>=0 else '매도'

    jusic_ment = ''
    if len(jusic.keys()) ==1:   ##################
        jusic_ment = jusic_ment + [*jusic][0] + ' '+ banolim(abs(jusic[[*jusic][0]]), '원', '일' ) +'주를 ' + su_do
    else:
        for i in jusic.keys():
            jusic_ment += i + ' ' + banolim(abs(jusic[i]),'원','일') +'주, '
        jusic_ment += '총 ' + banolim(abs(jusic_tot),'원','일') + '주를 ' + su_do
    #보통주 28만9272주를 매도


    ####소유주식이 456만5106 보통주에서 455만9951보통주로 5155주 감소####

    #직전 합계
    jeon = float(f[f.index('직전보고서제출일')+12])
    hu =  float(f[f.index('이번보고서제출일')+12])
    cha = hu - jeon   ##
    plma = '감소' if cha <0 else '증가'

    hap_ment = '소유주식이 {}주에서 {}주로 {}주 {}했다'.format(banolim(jeon,'원','일'), banolim(hu,'원','일'), banolim(abs(cha), '원', '일') ,
                                                  plma)
    #소유주식이 456만5106 보통주에서 455만9951보통주로 5155주 감소했다

    ###이번 최대주주 등 소유주식 감소로 최대주주 등이 보유한 전체 지분은 35.11%에서 35.08%로 변동됐다.###
    jeon_jibun = float(f[f.index('직전보고서제출일')+13])
    hu_jibun =  float(f[f.index('이번보고서제출일')+13])

    jibum_ment = "이번 소유주식 {}로 최대주주 등이 보유한 전체 지분은 {}%에서 {}%로 변동됐다".format(plma, jeon_jibun, hu_jibun)


    title = "{}, {} 등 소유주식 지분 {}% → {}%".format(crpNm, '최대주주', jeon_jibun, hu_jibun)
    article = """
    {}{} {}{} {}했다고 {}일 공시했다. <br><br>{} 
    """.format(crpNm, jongsung(crpNm, '은는'), relate_ment, jongsung(relate_ment, '이가'), jusic_ment, today, jibum_ment)


    ###필터 구간 ####
    force = False #송고 디폴트값.


    #코스피 200 안에 들거나,  지분 전후차이가 1이 넘거나

    if (stock_code in kos_list()['all_num']) or \
            (abs(float(jeon_jibun) - float(hu_jibun))>1) :
        force = True


    if force:
        return {'title':title, 'article':article, 'table':['보고일자','증감']}
    else:
        raise Exception("필터에서 걸러짐.")



end_time = time.time()
print((end_time-start_time))

if __name__ == "__main__":
    crpNm= '비비안'
    stockcode = '123'
    print(juju_byun(f=f, crpNm=crpNm))
    # temp = juju_byun(f=f, crpNm=crpNm)
    # print(temp['title'])
    # print(temp['article'])