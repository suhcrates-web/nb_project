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
#### 영업실적 ######

#연결재무제표기준영업(잠정)실적(공정공시)
def yg_siljeok(f=None, fs=None, crpNm=None, sou_html=None, cmd=None, **kwargs):
    return siljeok(f=f, fs=fs, crpNm=crpNm, sou_html=sou_html, cmd='yeon')


#영업(잠정)실적(공정공시)
def siljeok(f=None, fs=None, crpNm=None, sou_html=None, cmd =None, **kwargs):

    if cmd == 'yeon':
        yeon_gyeol = True
    else:
        yeon_gyeol = False

    today =date.today().day
    #영업(잠정)실적(공정공시)
    j=0
    for i in fs:
        if bool(re.search(r'단위', i)):

            break
        j +=1
    danwi_kan = fs[j]
    danwi = re.findall('\w*(?=원)',danwi_kan)[0]

    ##별도재무제표인지 찾기####
    jepyo = ''
    tit_jepyo = ''
    if yeon_gyeol: #연결인지 확인
        jepyo= ' 연결재무제표'
        tit_jepyo = '연결 '
    else: #연결 아니면 별도인지 체크
        for i in fs:
            if bool(re.search(r'별도재무제표', i)):
                jepyo = ' 별도재무제표'
                break

    #####기간 뽑는 구간 ######
    try: #당기실적, 전기실적 아래에 기간표시 있다고 가정. 그것도 없을 경우 인덱스 에러가 나게 돼있음.
        dang_gi = fs[fs.index('매출액')-3]
        jeon_gi = fs[fs.index('매출액')-2]
        dang = siljeok_gigan(dang_gi, jeon_gi)['dang'] #당기가 언젠지
        gigan = siljeok_gigan(dang_gi, jeon_gi)['gigan'] #분기인지 월인지
    except IndexError: #	당기실적(20년10월) 이런식으로 당기실적 칸에, 그것도 연결재무제표의 경우 2차 칸에 놓이는 경우가 있음.
        def check(a):
            return (bool(re.search(r'\d\s?년',a)) and bool(re.search(r'\d\s?월',a))) or ((bool(re.search(r'[1234]\s?분기',
                                                                                                       a) or bool(
                re.search(r'[1234]\s?[Qq]',a))) and (len(a)<30) ))
        j =0
        for i in fs: #i는 일부러 안씀. 위에 j=0 보이제.
            if check(fs[j]) and check(fs[j+1]):
                dang_gi = fs[j]
                jeon_gi = fs[j+1]
                break
            j +=1
        dang = siljeok_gigan(dang_gi, jeon_gi)['dang'] #당기가 언젠지
        gigan = siljeok_gigan(dang_gi, jeon_gi)['gigan'] #분기인지 월인지


    #####1차 내용 뽑는 구간#######
    _1cha = {}

    #매출액, 당기, 현금액

    key_1cha = ['영업이익', '매출액' , '당기순이익']
    if yeon_gyeol:
        key_1cha += ['지배기업소유주지분순이익']

    for i in key_1cha:
        _1cha[i]= {}
        _1cha[i]['d_h']= fs[fs.index(i)+2] #당기, 현금액
        _1cha[i]['d_y_r']= inc_rate(fs[fs.index(i)+6]) #당기, 전년대비 비율
        _1cha[i]['d_g_r']= inc_rate(fs[fs.index(i)+4]) #당기, 전기대비 비율
        _1cha[i]['n_h']= fs[fs.index(i)+8] #누계, 현금액
        _1cha[i]['n_y_r']= inc_rate(fs[fs.index(i)+12]) #누계, 현금액
        if yeon_gyeol:
            #연결재무재표에서 '지배기업소유지~~'가 당기순이익과 똑같은 경우 d_h를 '-'로 맞추면 기사쓸때 배제됨.
            if i == '지배기업소유주지분순이익':
                if _1cha[i]['d_h'] ==_1cha['당기순이익']['d_h'] and _1cha[i]['d_y_r'] ==_1cha['당기순이익']['d_y_r']:
                    _1cha[i]['d_h'] = '-'
                if _1cha[i]['n_h'] ==_1cha['당기순이익']['n_h'] and _1cha[i]['n_y_r'] ==_1cha['당기순이익']['n_y_r']:
                    _1cha[i]['n_h'] = '-'


    #1차에 내용이 있는지 확인
    bool_1cha = True
    for i in key_1cha:
        if _1cha[i]['d_h'] in ['0', '-']:
            bool_1cha = False
        else:
            bool_1cha = True
            break
        #하나라도 0, -  아닌게 있으면 True가 되면서 for loop을 멈추고 나옴.


    #1차에 '지난해' '누계'수치 있는지 확인. 없으면 '지난해' 아님.
    #있고 당기가 '4분기'일 경우/ last_year=True , dang_gigan='지난해'


    for i in key_1cha:
        if _1cha[i]['n_h'] in ['0', '-']:
            last_year = False
        else:
            if (str(dang) == '4') and (gigan == '분기') and bool_1cha:  #누계값이 있고, 4분기에 해당할 경우. 당기간은 '지난해'. #그리고 1차가
                # 있어야함. 없으면 걍 대충 당기로 다 해버림.
                dang_gigan = '지난해'
                last_year = True
                break
            last_year = False
            dang_gigan = str(dang)+gigan


    ##text 작성구간##


    ###1차 (매출액, 영업이익, 당기순이익) 작성구간
    text_1cha = ''
    #이마트가 14일 공시한 바에 따르면 지난 {12}{월} 동안
    # 매출액은 1조3230억원으로 전년대비 17.5% 증가,

    #전' '대비 {   }, / '흑자전환', '~~프로 증가'
    #전년비 증가율 있을 경우 하고, 없으면 전기대비로 함. // '흑자전환' 멘트 있을 경우 넣고, 숫자면 숫자로 채워줌.
    def plma_func(data, yg_word, cmd=None):
        #data : d_y_r 이 들어옴
        #yg_word : '년' '기'가 들어옴
        if data not in ['0', '-','']:
            han= '한'
            if cmd == 'sonsil':
                if data == '적자전환':
                    pass
                elif float(data) >0:
                    data = '적자 축소'
                    han = '된'
                elif float(data) <0:
                    data = '적자 확대'
                    han = '된'


            if bool(re.search('전환', data)) | bool(re.search('적자',data)):
                plma_ment = '전{}대비 {}{}'.format(yg_word, data, han)
            else:
                plma = '증가' if float(data) >0 else '감소'
                plma_ment = '전{}대비 {}% {}{}'.format(yg_word, data.replace('-',''), plma, han)
            return plma_ment
        return '오류'

    bool_tit_ind = False  #제목에 넣을 값 뽑기
    bool_tit_plma = False # 제목에 들어갈 증감 뽑기
    tit_cmd = False # '손실'여부 기록

    #4분기 누계실적이 있을 경우. 이걸 우선적으로 작성.
    if last_year and bool_1cha:
        first_line = True
        text_1cha += f"{dang_gigan} "
        n_gak=0 #'각각' 붙이기 위한
        for i in key_1cha:
            n_h = _1cha[i]['n_h']
            n_y_r = _1cha[i]['n_y_r']
            if n_h not in ['0', '-']: #값이 있는 경우
                n_gak+=1
                if yeon_gyeol:  #연결재무제표일 경우 키값에 이게 포함됨.
                    if i =='지배기업소유주지분순이익':
                        i = '지배기업 소유주지분 순이익'
                cmd = None
                #'이익' 이면서 적자일 경우. 이익을 손실로, 숫자 증감 빼고 '적자 전환, 적자 확대, 적자 축소' 로 대체.
                if bool(re.search('이익',i)) and ( float(n_h) <0):
                    i = re.sub('이익','손실',i)
                    cmd = 'sonsil'

                plma_ment = plma_func(n_y_r, '년', cmd = cmd)
                if plma_ment == '오류': #d_y_r이 0이나 - 일 경우 '오류'를 내놓음.
                    raise Exception("'지난해' 증감 문장에서 이상 발생") #그것도 없으면 exception. 근데 없는건 애초에 1차에 넣지를 않기에 여기까지 안옴.

                if first_line:
                    hat = '했'
                    plma_ment_1 = plma_ment
                    if bool(re.search('축소|확대',plma_ment)):
                        hat ='됐'
                        plma_ment_1 = plma_ment.replace('적자','적자가')
                    temp_1cha = f"{i}{jongsung(i, '은는')} {banolim(n_h,danwi,danwi)}원으로 {plma_ment_1[:-1]}{hat}다. "
                    first_line = False
                else:
                    temp_1cha = f"{i}{jongsung(i, '은는')} {plma_ment} {banolim(n_h,danwi,danwi)}원, "

                #'손실' 이면 마이너스부호 떼기.
                if cmd == 'sonsil':
                    temp_1cha = temp_1cha.replace('-','')

                text_1cha += temp_1cha



                if not bool_tit_ind: #아직 안정해졌으면 정해줌
                    tit_ind = i

                    tit_d_h = n_h
                    if cmd == 'sonsil':
                        tit_d_h =tit_d_h.replace('-','')
                    bool_tit_ind =True


                if not bool_tit_plma:
                    tit_plma = plma_ment[:-1]
                    tit_plma = tit_plma.replace('대비','比')
                    bool_tit_plma = True

        if n_gak>=3:
            gak = '각각 '
        else:
            gak = ''
        text_1cha = text_1cha[:-2]+ f'을 {gak}기록했다.'
        text_1cha += '<br><br>'

    if bool_1cha:
        first_line = True
        text_1cha += f"{dang}{gigan} "
        n_gak=0
        for i in key_1cha:
            d_h = _1cha[i]['d_h']
            d_y_r = _1cha[i]['d_y_r']
            d_g_r = _1cha[i]['d_g_r']
            if d_h not in ['0', '-']: #값이 있는 경우
                n_gak += 1
                if yeon_gyeol:  #연결재무제표일 경우 키값에 이게 포함됨.
                    if i =='지배기업소유주지분순이익':
                        i = '지배기업 소유주지분 순이익'

                #
                cmd = None
                #'이익' 이면서 적자일 경우. 이익을 손실로, 숫자 증감 빼고 '적자 전환, 적자 확대, 적자 축소' 로 대체.
                if bool(re.search('이익',i)) and ( float(d_h) <0):
                    i = re.sub('이익','손실',i)
                    cmd = 'sonsil'
                plma_ment = plma_func(d_y_r, '년', cmd=cmd)

                if plma_ment == '오류': #d_y_r이 0이나 - 일 경우 '오류'를 내놓음.
                    plma_ment = plma_func(d_g_r, '기')  # 그럼 전년 이 아닌 전기대비 비율을 대입
                    if plma_ment == '오류':
                        raise Exception("1차 증감 문장에서 이상 발생") #그것도 없으면 exception. 근데 없는건 애초에 1차에 넣지를 않기에 여기까지 안옴.


                first_end = True #첫줄로 끝나는 경우
                if first_line:
                    hat = '했'
                    plma_ment_1 = plma_ment
                    if bool(re.search('축소|확대',plma_ment)):
                        hat ='됐'
                        plma_ment_1 = plma_ment.replace('적자','적자가')
                    temp_1cha = f"{i}{jongsung(i, '은는')} {banolim(d_h,danwi,danwi)}원으로 {plma_ment_1[:-1]}{hat}다. "
                    first_line = False
                else:
                    temp_1cha = f"{i}{jongsung(i, '은는')} {plma_ment} {banolim(d_h,danwi,danwi)}원, "
                    first_end = False
                # text_1cha = text_1cha[:-2]+'을 각각 기록했다.'


                #'손실' 이면 마이너스부호 떼기.
                if cmd == 'sonsil':
                    temp_1cha = temp_1cha.replace('-','')

                text_1cha += temp_1cha

                if not bool_tit_ind: #아직 안정해졌으면 정해줌
                    tit_ind = i
                    tit_d_h = d_h
                    bool_tit_ind =True
                    if cmd == 'sonsil':
                        tit_d_h =tit_d_h.replace('-','')


                if not bool_tit_plma:
                    tit_plma = plma_ment[:-1]
                    tit_plma = tit_plma.replace('대비','比')
                    bool_tit_plma = True

        if n_gak>=3:
            gak = '각각 '
        else:
            gak = ''

        if not first_end:
            text_1cha = text_1cha[:-2]+ f'을 {gak}기록했다.'



    ##2차. 당기순이익 아래로 더 쓸 게 있다면 쓰기.
    if yeon_gyeol: # 연결재무제표의 경우 '지배기업소유주지분순이익'을 경계로.  아닌 경우 '당기순이익'을 경계로 함.
        end = '지배기업소유주지분순이익'
    else:
        end = '당기순이익'


    start_2cha_num = fs.index(end)+13  # 당기순이익 끝 다음칸.
    n = start_2cha_num
    bool_2cha = False
    try: #1차 이후 가장 처음 나타나는 순수한 숫자의  리스트 내 번호를 찾아냄.
        for i in range(start_2cha_num, len(fs)):
            i = fs[i]
            if bool(re.search(r'[0-9]', i)) and not bool(re.search(r'[가-힣|%p]', i)) \
                    and not bool(re.search(r'-\d+-',i)) \
                    and not bool(len(re.findall(r'\.',i))>1): #	2021.01.18 이런게 걸리는 오류도 있어 수정.
                ## 숫자 포함해야함.  한글, 퍼센트기호, -숫자-(전화번호),p 포함하지 않아야함. 이 경우 break하고 n을 하나 깎아서 내놓음.
                n = n-1 #해당 숫자가 포함된 인덱스여서.
                break
            n +=1
        bool_2cha = True
        if n == len(fs): #마지막줄까지 간 경우
            bool_2cha = False
    except: #조건에 맞는 게 없어서 n이 범위를 넘어가버릴 경우  #이 경우는 사실상 없는듯. for 루프기때문.
        bool_2cha = False
    text_2cha=''
    if bool_2cha:  #2차 텍스트가 참인 경우
        _2cha = {}
        n_list = []
        #2차 구간 수집#
        end_2cha =False
        while end_2cha == False:
            if bool(re.search(r'[0-9]', fs[n+1])) and not bool(re.search(r'[가-힣|%]', fs[n+1])):
                n_list.append(n)
                n = n +6
            else:
                end_2cha = True
        #n_list는 이제 각 세부사항들의 인덱스의 번호임.


        for i in n_list:

            #항목이름이 전부 괄호처리돼있으면 괄호만 지움.  이름 끝에 괄호 있으면 괄호 안없애고 같이 내놓음

            name = re.sub(r'[,-]' , '', fs[i]).replace('\xa0','')#.replace(' ','')#원래 괄호 없애는거 있었는데 안없애기로. 띄어쓰기도 안없애기로
            if bool(re.search(r'^\(.*\)$',name)):
                name = re.sub('[\(\)]','',name)
            if name =='기타':
                pass
            else:
                _2cha[name] = {}
                _2cha[name]['d_h']= fs[i+1] #당기, 현금액
                _2cha[name]['d_y_r']= inc_rate(fs[i+5]) #당기, 전년대비 비율
                _2cha[name]['d_g_r']= inc_rate(fs[i+3]) #당기, 전기대비 비율
        n_gak = 0


        bool_2cha = False #다시 False로 맞춰줌. 숫자가 없을수있기에

        for i in _2cha.keys():
            d_h = _2cha[i]['d_h']
            d_y_r = _2cha[i]['d_y_r']
            d_g_r = _2cha[i]['d_g_r']

            if d_h not in ['0', '-']: #값이 있는 경우
                bool_2cha = True  #숫자가 하나라도 있으면 True

                n_gak += 1
                plma_ment = plma_func(d_y_r, '년')
                if plma_ment == '오류':
                    plma_ment = plma_func(d_g_r, '기')
                    if plma_ment == '오류':
                        raise Exception("2차 증감 문장에서 이상 발생")

                text_2cha += f"{i}{jongsung(i, '은는')} {plma_ment} {banolim(d_h,danwi,danwi)}원, "


                if not bool_tit_ind: #아직 안정해졌으면 정해줌
                    tit_ind = i
                    tit_d_h = d_h
                    bool_tit_ind =True


                if not bool_tit_plma:
                    tit_plma = plma_ment[:-1]
                    bool_tit_plma = True

        if bool_2cha:
            if n_gak >2:
                gak = '각각 '
            else:
                gak = ''
            text_2cha = text_2cha[:-2]+ f'을 {gak}기록했다.'

    #이마트가 12일 제출한 영업실적 공시에 따르면 이마트의 지난 12월
    start_text = "{}{} {}일 제출한{} 영업실적 공시에 따르면 ".format(
        crpNm,jongsung(crpNm,'이가') ,today, jepyo, crpNm, dang_gigan)

    if bool_1cha:
        article = start_text + text_1cha
        if bool_2cha:
            article +="<br><br>"+text_2cha
    else:
        article = start_text + text_2cha
    article = article.replace('+','')

    ###제목에 들어갈것들 위에서 만들어져 들어옴.####
    #이마트, 12월 매출 1.3조..전년비 17.5% 증가"


    title = "{}, {} {}{} {}원...{}".format(
        crpNm,
        dang_gigan,
        tit_jepyo,
        tit_ind,
        banolim(tit_d_h, danwi, '억'),
        tit_plma

    ).replace('+','')

    return {'title':title, 'article':article, 'table': ['실적내용', '정보제공내역', -2]}



end_time = time.time()
print((end_time-start_time))

if __name__ == "__main__":
    crpNm= '이마트'
    stockcode = '123'
    result = siljeok(f=f, fs=fs, crpNm=crpNm)
    print(result['title'])
    print(result['article'])
    # temp = juju_byun(f=f, crpNm=crpNm)
    # print(temp['title'])
    # print(temp['article'])