import re
from datetime import datetime, date

#word : 단어 집어넣음
#context: 은는, 이가, 을를, 이다, 와과

def jongsung(word, context):
    ja = word[-1] #마지막 글자
    jong = ((ord(ja)-ord('가'))/28)%1
    if jong ==0 :  #나눠떨어짐. 받침 없는 경우
        result = {'은는':'는', '이가': '가', '을를':'를', '이다':'다', '와과':'와', '으로':'로', '했다고':'고' }
    else :
        result = {'은는':'은', '이가': '이', '을를':'을', '이다':'이다', '와과':'과', '으로':'으로' , '했다고':'이라고'}

    return result[context]


def word_to_date(date_word):
    if bool(re.search('월',date_word)):
        date_word = datetime.strptime(date_word, '%Y년%m월%d일')
    elif bool(re.search('-',date_word)):
        date_word = datetime.strptime(date_word, '%Y-%m-%d')
    else:
        date_word = datetime.strptime(date_word, '%Y.%m.%d')
    return date_word


####영업실적용. 실적보고서  분기, 월 구분해서  보고서의 대상 기간을 특정해주는 펑션##
def siljeok_gigan(dang, jeon):
    d = dang.replace(' ','')
    j = jeon.replace(' ','')
    def month(x, type='int'):
        for i in ['19','20','21','22']:
            try:
                x = x[d.index(i)+2:]
                try:
                    x = x[x.index(i)+2:]   #2020년 을 거르기 위해 두번 넣어줌
                except:
                    pass
            except:
                pass
        x = re.findall(r'\d+', x)[0]  #월 만 추려짐

        if type == 'int':
            x = int(x)
        elif type == 'str':
            x = str(x).strip()
        return x
    d_m = month(d)
    j_m = month(j)

    Q_force = False # '분기'로 처리할지 강제할지 여부 # False : 월 / True : 분기
    for i in ['분기', 'Q','q']:
        if bool(re.search(r'{}'.format(i), d)):
            gigan = '분기'  #이 키워드가 들어있으면 무조건 분기
            Q_force = True



    if Q_force == False: #force가 True를 받지 못했을 경우, 이제 d와 j 의 월 숫자 뽑아내서 비교해봐야함.
        #월 숫자는 19,20,21,22 숫자 다음에 나오는 숫자를 뽑는 식으로.(이 숫자는 월이나 일과 겹치지 않을듯)

        if abs(d_m - j_m) in [3,9]:
            Q_force =True
        elif abs(d_m - j_m) in [1,11]:
            Q_force = False
        else:
            raise Exception('기간 종류 분류에 에러 있음')

    if Q_force:
        gigan = '분기'
    elif not Q_force:
        gigan = '월'


    ##현재의 날짜로 보고서의 기간을 유추 ##
    now = date.today().month
    if gigan =='분기':
        if now in [1,2,3]:
            t = 4
        elif now in [4,5,6]:
            t =1
        elif now in [7,8,9]:
            t =2
        elif now in [10,11,12]:
            t =3
    elif gigan == '월':
        if now == 1:
            t = 12
        else:
            t = now - 1

    #dang에다가 '월'을 그대로 넣으면, '12분기' 가 나올 수 있음. 표기는 월단위로 돼있지만 9~12월, 이런식으로 할 수 있기때문. 현재를 기준으로 하는게 맞음.
    return {'dang':t, 'gigan':gigan} #dang: 당기  #gigan : 분기, 월
    #보고서 대상 기준을 찾기.


#####영업실적용. 증감액·율 구분####
def inc_rate(a):
    if bool(re.search(r'[\(\)]', a)):
        a = re.findall(r'(?<=\().+(?=\))', a)[0]
    a = a.replace('%','')
    return a

##################################
######조회공시요구 답변 용#########
#통문단을 받아 '.'을 기준으로 나눠줌. 다만  '2020.01.03' 은 '2020년1월3일'로 바꿔주고, 3.49% 처럼 . 뒤에 숫자가 있으면 건너뜀
def dadum_tong_mun(tong_mun_0): #통문장들을 다듬음
    #나눠지지 않은 통문장이 들어옴
    ##2021.09.09 을 2021년9월9일 로 변환
    date_in_text = re.findall(r'\d{4}\.\s?\d{2}\.\s?\d{2}\.?' , tong_mun_0)
    subs = []
    for i in date_in_text:
        Y =re.findall(r'\d+(?=\.)',i)[0]
        i = i[i.index(Y)+len(Y):]
        m = re.findall(r'\d+(?=\.)',i)[0]
        i = i[i.index(m)+len(m):]
        d = re.findall(r'\d+',i)[0]
        sub = f'{str(int(Y))}년{str(int(m))}월{str(int(d))}일'
        subs.append(sub)
    tong_mun= re.sub(r'\d{4}\.\s?\d{2}\.\s?\d{2}\.?', '{}', tong_mun_0)
    tong_mun = tong_mun.format(*subs)

    ## . 을 기준으로 문장들을 나눠 리스트화. **다만  3.39% 처럼  . 뒤에 숫자가 있는 경우는 건너뜀.
    def split_mun(a):
        list_sens = [] #list of sentences
        end = False
        while end == False:
            sentence = ''
            j = 0
            for i in a:
                if i not in ['.', '-']:
                    sentence += i
                    j +=1
                elif bool(re.search(r'[.-]\d',a[j:j+2])) :
                    sentence += i
                    j +=1
                else:
                    list_sens.append(sentence)
                    j += 1
                    a = a[j:]
                    break

            if len(a) ==j :
                end = True
        return list_sens

    list_sentences = split_mun(tong_mun)

    return list_sentences


###문장* 안에 보도 해명 내용이 있는지 체크 후 result를 뱉음. ##
def bodo_hm(list_sentences):
    p = 0
    hm = ''
    try:
        for i in list_sentences:
            if bool(re.search(r"""\".+[^\"].+\"""", i)):  # " " 안에 들어있는 문장이 있을 경우
                tit = re.findall(r"""\".+[^\"].+\"""", i)[0]  # tit : 기사제목
                if bool(re.search(r'기사|보도|언론',list_sentences[p])) :
                    try:
                        hm= i[i.index('당사는'):]   # hm : 해명문.  당사는, 당사의 로 시작.
                    except:
                        hm= i[i.index('당사의'):]   # 당사~
                    break #하나 만들면 멈춤
            p +=1

        relation = True # 관계 없다
        if hm != '':
            if '없' in hm:
                hm = hm[:hm.index('없')+1] +'다'
                relation = False

            else:
                for j in ['입니다','습니다','였습니다','합니다','했습니다']:
                    if j in hm:
                        hm = hm[:hm.index(j)] + jongsung(hm, '이다')
                        break
        print(hm)

        text_bodo_hm = f"""최근의 {tit} 보도와 관련해서는 "{hm}"{jongsung(hm,'했다고')} 밝혔다"""
        return {'result':text_bodo_hm, 'relation':relation}
    except:
        return {'result':False}

###'당사는(당사가, 현재) ~~ 확정 ~~~없다'
def dangsa(list_sentences):
    n=0
    result = False
    try:
        for i in list_sentences:
            n +=1
            if not bool(re.search(r'\(미확정\)|\(\s?풍문\s?또는\s?보도\s?\)|\(재공시\)',i)): #여기 걸리면 무조건 걸러냄
                if bool(re.search(r'확정.*없|결정.*없',i)): #그 중 '확정 ~ 없' 을 담은 문장
                    for j in ['당사는', '당사가', '현재']:  #의 앞에 이것들이 있는지 찾아봄.

                        if j in i:
                            sent = i[i.index(j):i.index('없')+1] +'다'
                            result = sent
                            break

        return {'result':result}  #문장을 내보냄
    except :
        return {'result':False} #위에 수집된게 없으면 False를 내보냄