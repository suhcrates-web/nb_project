from datetime import date, datetime
import math, re

from banolim import banolim
import pandas
import time
import re
from toolBox import jongsung, word_to_date, siljeok_gigan, inc_rate, make_sentence
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
with open('test_r.csv', 'r', encoding= 'utf-8') as file:
    line= file.readlines()[0].replace('\\r','\r').replace('\\n','\n')
    fr = line.split('|')

cmd = []
bogoNm= '조회공시요구(현저한시황변동)에대한답변(중요공시대상없음)'
def johwae_ans(f=None, fs=None, crpNm=None, sou_html=None, cmd =None, bogoNm=None, **kwargs):
    cmd = re.findall(r'(?<=\()[^\(\)]+(?=\))', bogoNm)
    subject = cmd[0]
    point = cmd[1]
    today =date.today().day
    crpNm = crpNm
    #####현저한시황변동######
    print(crpNm)
    if subject in ['현저한시황변동']:
        if point in ['중요공시대상없음']:
            title = f"""{crpNm}, 현저한 시황변동에 "주요 공시대상 없어" """
            print(title)
            article = f"""{crpNm}{jongsung(crpNm,'은는')} 최근 나타난 현저한 시황변동과 관련해 이에 영향을 미칠만 사항으로서 현재 진행중이거나 확정된 공시 규정상 중요한 
            공시대상이 
            없다고 {today}일 공시했다."""
            print(article)
# 
# 
# 
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
    johwae_ans(crpNm=crpNm, bogoNm=bogoNm)

    # temp = juju_byun(f=f, crpNm=crpNm)
    # print(temp['title'])
    # print(temp['article'])