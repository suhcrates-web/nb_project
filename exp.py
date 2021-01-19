from datetime import date, datetime
import math, re

from banolim import banolim
import pandas
import time
import re
from toolBox import jongsung, word_to_date, siljeok_gigan, inc_rate,  bodo_hm, dadum_tong_mun, dangsa
from kospi200_list import kospi200
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
cmd = []
bogoNm= '조회공시요구(풍문또는보도)에대한답변(미확정)'
def johwae_ans(f=None, fs=None, crpNm=None, sou_html=None, cmd =None, bogoNm=None, **kwargs):
    cmd = re.findall(r'(?<=\()[^\(\)]+(?=\))', bogoNm)
    subject = cmd[0]
    point = cmd[1]
    today =date.today().day
    crpNm = crpNm
    answer_0 = f[3] #답변문
    #####현저한시황변동######
    list_sentences =  dadum_tong_mun(answer_0)
    if subject in ['현저한시황변동']:
          # 2021.01.01 을 2021년1월1일 로 바꿔줌.  '.'과 '-'을 기준으로 분리. -123 ,
        # 1.4%  는 놔둠.

        if point in ['미확인', '미확정']:
          title = f'{crpNm}, 현저한 시황변동에 "확정된 사항 없어"'
          article = f"""{crpNm}{jongsung(crpNm,'은는')} 최근 나타난 현저한 시황변동과 관련해 확정된 사항이 없다고 {today}일 공시했다."""
          result = dangsa(list_sentences)['result'] #없으면 false 나옴

          if result != False:
              article += f'<br><br>최근 제기된 풍문 또는 보도와 관련해서는 "{result}"{jongsung(result,"했다고")} 밝혀다.'

        else:
            if point in ['중요공시대상없음']:
                title = f'{crpNm}, 현저한 시황변동에 "주요 공시대상 없어"'
                article = f"""{crpNm}{jongsung(crpNm,'은는')} 최근 나타난 현저한 시황변동과 관련해 이에 영향을 미칠만 사항으로서 현재 진행중이거나 확정된 공시 규정상 중요한 공시대상이 없다고 {today}일 공시했다."""
            if point in ['중요정보없음']:
                title = f'{crpNm}, 현저한 시황변동에 "공시할 중요 정보 없어"'
                article = f"""{crpNm}{jongsung(crpNm,'은는')} 최근 나타난 현저한 시황변동과 관련해 별도로 공시할 중요한 정보가 없다고 {today}일 공시했다."""

            result_bodo_hm = bodo_hm(list_sentences)
            text_bodo_hm = result_bodo_hm['result']  # false가 나오거나 문장이 나옴.
            if text_bodo_hm != False: #보도해명이 나왔다면
              title +="...보도에 해명"
              if not result_bodo_hm['relation']:
                  title += """ "관련 없어" """
              article += f""" <br><br>{text_bodo_hm} """

    elif subject in ['풍문또는보도']:
        if point in ['미확정']:
            #####풍문 내용을 찾는 구간 ####
            reason =False
            pung = f[1]
            if bool(re.search(r'(?<=\()[^\(\)]+설\s?(?=\))',pung)):
                reason = re.findall(r'(?<=\()[^\(\)]+설\s?(?=\))',pung)[0]
            else:
                for i in ['설','보도','관련']:
                    if i in pung:
                        reason = pung[:pung.index(i)+len(i)]
            if not reason:
                reason = '풍문 또는 보도'
            result = dangsa(list_sentences)['result']
            article = ''
            if result ==False:
                raise Exception("풍문보도- 답변 문장 못찾음")

            title = f"""{crpNm}, '{reason}'에 "미확정\""""
            article = f"""{crpNm}은 최근의 {reason}{jongsung(reason,'와과')} 관련해 '{result}'{jongsung(result,'했다고')} {today}일 공시했다.  """
    return {'title':title, 'article':article, 'table':['제목','내용']}
# answer_0 = fr[3]
# 
# 
# try:
#     sentence = make_sentence(answer_0)
# except:
#     raise Exception("문장을 못만듦")
# 
# print(sentence)

end_time = time.time()
print((end_time-start_time))

if __name__ == "__main__":
    crpNm= '비비안'
    johwae_ans(f=f , crpNm=crpNm, bogoNm=bogoNm)

    # temp = juju_byun(f=f, crpNm=crpNm)
    # print(temp['title'])
    # print(temp['article'])