import re
from datetime import datetime, date

#word : 단어 집어넣음
#context: 은는, 이가, 을를, 이다, 와과

def jongsung(word, context):
    ja = word[-1] #마지막 글자
    jong = ((ord(ja)-ord('가'))/28)%1
    if jong ==0 :  #나눠떨어짐. 받침 없는 경우
        result = {'은는':'는', '이가': '가', '을를':'를', '이다':'다', '와과':'와', '으로':'로' }
    else :
        result = {'은는':'은', '이가': '이', '을를':'을', '이다':'이다', '와과':'과', '으로':'으로' }

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



#####조회공시에 대한 답변###. '당사는 ~~~검토중에 있으나 확정된 사항이 없다" 문장 만들어줌
#fr(raw 버전)의 '답변내용' 부분을 넣어주면 'sentence'를 뱉음. 반드시 '검토' '확정' '없' '당사는' 이 포함돼야하며, 그 문장만 뱉어냄.
def make_sentence(answer_0):

    date_in_text = re.findall(r'\d{4}\.\s?\d{2}\.\s?\d{2}\.?' , answer_0)
    subs = []
    for i in date_in_text:
        Y =re.findall(r'\d+(?=\.)',i)[0]
        i = i[i.index(Y)+len(Y):]
        m = re.findall(r'\d+(?=\.)',i)[0]
        i = i[i.index(m)+len(m):]
        d = re.findall(r'\d+',i)[0]
        sub = f'{str(int(Y))}년{str(int(m))}월{str(int(d))}일'
        subs.append(sub)
    answer= re.sub(r'\d{4}\.\s?\d{2}\.\s?\d{2}\.?', '{}', answer_0)
    answer = answer.format(*subs)
    answers_0 = re.split('\. |\n', answer)
    answers = []
    for i in answers_0:
        i = re.sub(r'\s+', r' ', i)
        if i in ['' , ' ']:
            pass
        else:
            answers.append(i.strip())


    n=0
    for i in answers:
        sure = ['검토','없', '확정']
        sure_bool = True
        for j in sure:
            if not re.search(j, i):
                sure_bool = False  #한개라도 일치하는 게 없으면 False.
                break
        if not bool(re.search('당사가|당사는',i)): #당사가, 당사는 둘다 없으면 역시 False
            sure_bool = False
        if sure_bool ==True: #sure과 모두 일치하면
            break  #멈추고 n을 내놓음

        n+=1         #아니면 n을 하나 더한 뒤 루프를 계속 진행

    if n == len(answers):
        raise Exception("맞는 문장이 없음")

    sentence= answers[n]
    try:
        sentence= sentence[sentence.index('당사는'):]
    except:
        sentence= sentence[sentence.index('당사가'):]

    sentence = sentence[:sentence.index('없')+1]+'다'

    return sentence


# print(jongsung('병신','은는'))