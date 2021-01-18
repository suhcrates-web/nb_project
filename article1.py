#모든 기사 유형은 여기에 넣어서 한꺼번에 관리하자. 유형 하나에 def 하나로
#기사유형 1 : 타법인 주식 및 출자증권 처분결정 #

from datetime import date, datetime
from banolim import banolim
import pandas, re, math
from toolBox import jongsung, word_to_date, siljeok_gigan, inc_rate
from kospi200_list import kospi200


#처리할 수있는 공시유형 목록. 빈칸 유지. 아래 append를 통해 채워짐.
dict_can = {} #{'bogoNm': 보고서 이름 , 'function' : 함수이름}
# f=[]
# with open('test.txt', 'r', encoding= 'utf-8') as file:
#     f = [x.rstrip() for x in file.readlines()]

#예시 : 20201208900383
if __name__ == "__main__":  #rcpNo_to_table 에서 만든 test.txt 파일 가져옴
    f = []
    with open('test.txt', 'r', encoding= 'utf-8') as file:
        f = [x.rstrip() for x in file.readlines()]



#'타법인 주식 및 출자증권 처분결정'
def otherCorp(f=None, crpNm=None, sou_html=None, **kwargs):
    if f[f.index('회사와 관계')+1] in ['자회사', '계열회사', '관계회사', '관계기업']:  #회사와의 관계가 자회사라면
        corpNm = crpNm
        relation = f[f.index('회사와 관계')+1]
        purpose = f[f.index('처분목적')+1]
        opCorpNm = f[f.index('회사명(국적)')+1].replace('주식회사','').replace('(주)','').replace('㈜','').strip()
        cheobun = f[f.index('처분주식수(주)')+1]
        jagi = f[f.index('자기자본대비(%)')+1]
        chebunPrice = f[f.index('처분금액(원)')+1]
        today = date.today().day
        juyosaup = f[f.index('주요사업')+1]
        jabongum = banolim(f[f.index('자본금(원)')+1])
        ch_hu_jibun = f[f.index('처분후 소유주식수 및 지분비율')+4]
        if ch_hu_jibun in ['-', '0']:
            title = "{}, {} {} 지분 {}원에 전량 처분".format(corpNm, relation, opCorpNm, banolim(chebunPrice, gijun='억'))

            article = '''
    {}{} {}를 위해 보유중인 {} {}의 지분 {}%({}주)를 약 {}원에 처분 결정했다고 {}일 공시했다.<br><br>{}의 주요 사업은 {}이며 자본금은 {}원이다.
        '''.format(corpNm, jongsung(corpNm,'은는'), purpose, relation, opCorpNm, jagi, banolim(cheobun, gijun='일'),
                   banolim(chebunPrice, gijun='억'), today , opCorpNm, juyosaup, jabongum  )
        else:
            title = "{}, {} {} 지분 {}원에 처분...잔여 지분 {}%".format(corpNm, relation, opCorpNm, banolim(chebunPrice,
                                                                                                 gijun='억'), ch_hu_jibun)

            article = '''
    {}{} {}를 위해 보유중인 {} {}의 지분 {}%({}주)를 약 {}원에 처분 결정했다고 {}일 공시했다. 처분 후 지분비율은 {}%가 된다.<br><br>{}의 주요 사업은 {}이며 자본금은 {}원이다.
        '''.format(corpNm, jongsung(corpNm,'은는'), purpose, relation, opCorpNm, jagi, banolim(cheobun, gijun='일'),
                   banolim(chebunPrice, gijun='억'), today, ch_hu_jibun, opCorpNm, juyosaup, jabongum)

        return {'title':title, 'article':article, 'table':'처분예정일자'}
    else:
        raise Exception('자회사, 계열사, 관계사가 아님')
dict_can['타법인주식및출자증권처분결정']=otherCorp #이게 각 def 위에 붙어서 해당 기사유형의 이름이 됨.


#현금ㆍ현물배당 결정
if __name__ == "__main__":
    crpNm = '보광산업'
def a_hBaedang(f=None, crpNm=None, sou_html=None, **kwargs):
    corpNm = crpNm

    if (f[f.index('1주당 배당금(원)')+4] == '-'): #종류주식이 '-'인 경우. 보통주식이라는 말
        botong = f[f.index('1주당 배당금(원)')+2]

        baeKind = f[f.index('배당종류')+1]
        today = date.today().day
        baeTotal = f[f.index('배당금총액(원)')+1]
        gijunil =  pandas.to_datetime(f[f.index('배당기준일')+1], format= '%Y-%m-%d')


        if gijunil.month != date.today().month:
            gijun_wan = "{}월{}일".format(gijunil.month, gijunil.day)
        else:
            gijun_wan = "오는 {}일".format(gijunil.day)

        title = "{}, 주당 {}원 {} 결정".format(corpNm, banolim(botong,'원', '일'), baeKind)
        article = """
        {}{} 보통주 1주당 {}원의 {}을 결정했다고 {}일 공시했다. 배당금 총액은 {}원이다. 배당기준일은 {}이다.
        """.format(corpNm, jongsung(corpNm,'은는'), banolim(botong,'원', '일'), baeKind, today, banolim(baeTotal,'원','일'), \
                                         gijun_wan )
        return {'title':title, 'article':article, 'table': '배당기준일'}
    else:
        raise Exception("보통주가 아님")
dict_can['현금ㆍ현물배당결정']=a_hBaedang



#'주식배당 결정'
if __name__ == "__main__":
    crpNm = '나스미디어'
def a_jBaedang(f=None, crpNm=None, sou_html=None, **kwargs):
    corpNm = crpNm

    if (f[f.index('1주당 배당주식수 (주)')+4] == '-'): #종류주식이 '-'인 경우. 보통주식이라는 말
        botong = f[f.index('1주당 배당주식수 (주)')+2]

        today = date.today().day

        if f[f.index('배당주식총수 (주)')+4] == '-':
            baeTotal = f[f.index('배당주식총수 (주)')+2]
            gijunil =  pandas.to_datetime(f[f.index('배당기준일')+1], format= '%Y-%m-%d')
            if gijunil.month != date.today().month:
                gijun_wan = "{}월{}일".format(gijunil.month, gijunil.day)
            else:
                gijun_wan = "오는 {}일".format(gijunil.day)

            title = "{}, 주당 {}주 주식배당 결정".format(corpNm, banolim(botong,'원','일'))
            article ="""
            {}{} 1주당 보통주 {}주의 주식배당을 결정했다고 {}일 공시했다. 총 배당주식 수는 보통주 {}주다. 배당기준일은 {}이다.
            """.format(corpNm, jongsung(corpNm, '은는'), banolim(botong,'원','일'), today, banolim(baeTotal,'원','일'), \
                                                 gijun_wan )

            return {'title':title, 'article':article, 'table': '배당기준일'}
        else:
            raise Exception("배당주식총수 보통주 아님")
    else:
        raise Exception("1주당 배당주 보통주 아님")
dict_can['주식배당결정']=a_jBaedang


#'주요사항보고서(유상증자결정)'
if __name__ == "__main__":
    crpNm ='쎌마테라퓨틱스'
def a_yuJeung(f=None, crpNm=None, sou_html=None, **kwargs):
    corpNm = crpNm

    #총 규모 파악. 자금조달목적 내 '-' 제외한 모든 액수 더해야함#
    a = ['시설자금 (원)', '영업양수자금 (원)', '운영자금 (원)', '채무상환자금 (원)', '타법인 증권취득자금 (원)','기타자금 (원)']
    b = [] #a 항목들의 숫자
    c=0  # 0이 아닌 목록 번호
    d=[] # 0이 아닌 목록 번호의 list
    for i in a:
        temp =f[f.index(i)+1]
        b.append(temp)
        if temp not in ['-', '0']: #조달목적 중 해다 항목이 0이 아닌 경우
            d.append(c)    #그 목록 번호를 d에 저장
        c = c+1 #목록 번호는 1씩 계속 올라감

    totAmt = 0 #총 규모
    for i in d :
        totAmt = totAmt + float(b[i])


    #자금조달목적 (리스트 형식임)
    purposeList =[]
    for i in d:
        purposeList.append(a[i].replace('(원)','').strip())

    #목적, 리스트를 스트링으로
    purpose = ""
    for i in purposeList:
        purpose = purpose + ', ' +i
    purpose = purpose[2:] #줄줄 붙여놓은것.


    if f[f.index('신주의 종류와 수')+4] in ['-','0']:
        juPerAc = f[f.index('1주당 액면가액 (원)')+1]
        botong = f[f.index('신주의 종류와 수')+2]
        today = date.today().day

    way = f[f.index('증자방식')+1]

    if way == '제3자배정증자':
        samJa = sou_html
        samJa = samJa.findAll('table')

        j, jj = 0, 0
        for i in samJa:
            if bool(re.search(r'제3자배정 대상자</th>', str(i))):
                jj = j
            else:
                j = j+1


        '''
        #이렇게도 했음
        i=0
        temp = False
        while temp ==False:
            temp_sam = samJa[i].text
            if bool(re.search(r'제3자배정 대상자(?!별)', temp_sam)):
                temp =True
            else:
                i = i+1
        samJa= samJa[i]
        print(samJa.text)
        '''

        samJa = samJa[jj].findAll('td')
        samJa = [x.text.replace('\n','').replace('\xa0','') for x in samJa]
        i=0
        daesangList = []
        while i< len(samJa):
            daesangList.append(samJa[i].replace('(주)','').replace('㈜','').strip())
            i = i+6

        #대상자 리스트를 스트링으로
        daesang = ""
        for i in daesangList:
            daesang = daesang + ', ' +i
        daesang = daesang[2:] #줄줄 붙여놓은것.

    #corpNm, totAmt, purposeList, purpose, juPerAc, botong, today, way, daesangList, daesang

    if purposeList[0] !='기타자금':
        title= "{}, {}원 규모 유상증자 결정...{} 용도".format(corpNm, banolim(totAmt,'원','억'), purposeList[0])
        article = """
        {}{} 주당 액면가 {}원의 보통주 {}주를 유상증자 하기로 했다고 {}일 공시했다. 총 {}원 규모로, 자금 용도는 {} 등이다.   
        """.format(corpNm, jongsung(corpNm,'은는'), banolim(juPerAc, '원', '일'), banolim(botong,'원','일'), today,
                   banolim(totAmt,'원','일'),
                   purpose)
    else:
        if len(daesangList)>1:
            temp_name = daesangList[0] + ' 등'
        else:
            temp_name = daesangList[0]

        title= "{}, {}원 규모 유상증자 결정...{}에 배정".format(corpNm, banolim(totAmt,'원','억'), temp_name)
        article = """
            {}{} 주당 액면가 {}원의 보통주 {}주를 유상증자 하기로 했다고 {}일 공시했다. 총 {}원 규모다.   
            """.format(corpNm, jongsung(corpNm,'은는'), banolim(juPerAc, '원', '일'), banolim(botong,'원','일'), today, \
                                           banolim(totAmt,'원','일'),
                       purpose)


    if way == '제3자배정증자':
        three = """
        <br><br>증자방식은 제3자배정증자로, 배정 대상은 {}{}.
        """.format(daesang, jongsung(daesang, '이다'))

        article = article + three

    return {'title':title, 'article':article, 'table': ['신주의 종류와 수', '증자방식']}
dict_can['주요사항보고서(유상증자결정)']=a_yuJeung


#단일판매ㆍ공급계약체결
def danil(f=None, crpNm=None, sou_html=None, **kwargs):
    fs = []
    for i in f:
        i = i.replace(' ','')
        fs.append(i)
    today = date.today().day
    if '판매ㆍ공급계약 내용' in f:
        if f[f.index('판매ㆍ공급계약 내용')+1] != '건설수주':
            tot = f[f.index('계약금액 총액(원)')+1]

            machulRate =  f[fs.index('매출액대비(%)')+1]

            if True in [float(machulRate) > 10]:
                if True in [float(tot) > 5000000000, float(machulRate) >= 100]:

                    corpNm = crpNm
                    opCorpNm_sentence = ''
                    opCorpNm = f[f.index('계약상대방')+1].replace('주식회사','').replace('(주)','').replace('㈜','').strip()
                    if opCorpNm == '-':
                        opCorpNm_sentence = ''
                    else:
                        business=None
                        if not bool(re.search(r'[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]', opCorpNm)):
                            nation = f[f.index('판매ㆍ공급지역')+1]
                            business=  f[f.index('-주요사업')+1]
                            b_con = True
                            if business == '-':
                                business = '업체'
                                b_con = False
                            if not bool(re.search(r'업체$', business)):
                                if b_con ==False:
                                    business = business + ' 업체'
                                else:
                                    business = business + ' 관련 업체'
                            opCorpNm = "{} {}({})".format(nation, business, opCorpNm)

                        if business == None:
                            temp_jongsung = jongsung(opCorpNm, '와과')
                        else:
                            temp_jongsung = jongsung(business, '와과')
                        opCorpNm_sentence = '{}{} '.format(opCorpNm, temp_jongsung)


                    naeYong =  f[f.index('판매ㆍ공급계약 내용')+1].strip()
                    if not bool(re.search(r'계약$',naeYong)):
                        naeYong = naeYong + ' 계약'

                    today = date.today().day

                    gye_gigan = ""
                    try:
                        gs_0 = pandas.to_datetime(f[f.index('시작일')+1], format= '%Y-%m-%d')
                        gs_1 = pandas.to_datetime(f[f.index('종료일')+1], format= '%Y-%m-%d')
                        if (gs_0 != '-') & (gs_1 != '-'):
                            gyeStart = "{}년 {}월{}일".format(gs_0.year, gs_0.month, gs_0.day)
                            gyeEnd = "{}년 {}월{}일".format(gs_1.year, gs_1.month, gs_1.day)
                            gye_gigan = " 계약기간은 {}부터 {}까지다.".format(gyeStart, gyeEnd)
                    except:
                        pass


                    title='{}, {}원 규모 공급계약 체결...매출액 대비 {}%'.format(corpNm, banolim(tot,'원','억'), math.floor(float(machulRate)))
                    article = """
                    {}{} {}{}원 규모의 {}을 체결했다고 {}일 공시했다. 계약금액은 최근 매출액 대비 {}% 수준이다.{}
                    """.format(corpNm, jongsung(corpNm, '은는'), opCorpNm_sentence, banolim(tot,'원','만'), naeYong,
                               today,machulRate, gye_gigan)

                    if f[f.index('공시유보 관련내용')+2] not in ['-', '0']:
                        gh_0 =pandas.to_datetime(f[f.index('유보기한')+1], format= '%Y-%m-%d')
                        gihan = "{}년 {}월{}일".format(gh_0.year, gh_0.month, gh_0.day)
                        sayu = f[f.index('유보사유')+1]

                        yubo_article = """
                        {}{} {}까지 공시 유보된다.
                        """.format(sayu, jongsung(sayu, '으로'), gihan)
                        article = article + yubo_article

                return {'title':title, 'article':article, 'table': '종료일'}
            raise Exception("총액 적거나 매출비율 적어서")
        raise Exception("양식 달라서") #이건 없어도 될듯

    elif '판매ㆍ공급계약 구분' in f:
        if f[f.index('판매ㆍ공급계약 구분')+1] == '공사수주':
            opCorpNm = f[f.index('계약상대')+1].replace('주식회사','').replace('(주)','').replace('㈜','').strip()
            naeYong =  f[f.index('- 체결계약명')+1].strip()
            naeYong = re.sub(r'계약$', '', naeYong)
            tot = f[f.index('계약금액(원)')+1]
            machulRate =  f[fs.index('매출액대비(%)')+1]

            gye_gigan = ""
            try:
                gs_0 = pandas.to_datetime(f[f.index('시작일')+1], format= '%Y-%m-%d')
                gs_1 = pandas.to_datetime(f[f.index('종료일')+1], format= '%Y-%m-%d')
                if (gs_0 != '-') & (gs_1 != '-'):
                    gyeStart = "{}년 {}월{}일".format(gs_0.year, gs_0.month, gs_0.day)
                    gyeEnd = "{}년 {}월{}일".format(gs_1.year, gs_1.month, gs_1.day)
                    gye_gigan = " 계약기간은 {}부터 {}까지다.".format(gyeStart, gyeEnd)
            except:
                pass


            nation = f[f.index('판매ㆍ공급지역')+1]

            a, b,c, d, title_content = '', '', '', '', ''
            for i in ['아파트', '시설', '구조물', '국도', '주택']:
                if bool(re.search(i, naeYong)):
                    a = re.findall(r'\w*{}'.format(i), naeYong)[0] + ' '
                    d = '건설'

            for i in ['정비']:
                if bool(re.search(i, naeYong)):
                    a = re.findall(r'\w \w*{}'.format(i), naeYong)[0] + ' '

            if bool(re.search('신축', naeYong)):
                b = '신축 '

            if bool(re.search(r'.+시', nation)):
                c = re.findall(r'\w+시', nation)[0]+ ' '
                c = re.sub(r'광역', '', c)
            elif bool(re.search(r'.+군', nation)):
                c = re.findall(r'\w+군', nation)[0]+ ' '
            if bool(re.search(r'서울', c)):
                c=''

            title_content = c+a+b +d

            title = "{}, {}원 규모 {}공사 수주".format(crpNm, banolim(tot, '원', '억'), title_content)
            article = """
            {}{} {}{} '{}' 수주계약을 체결했다고 {}일 공시했다. 계약금액은 {}원 규모이며, 이는 최근 매출액 대비 {}%다.{} 공급지역은 {}{}.
            """.format(crpNm, jongsung(crpNm, '은는'), opCorpNm, jongsung(opCorpNm, '와과'), naeYong, today, banolim(tot,
                                                                                                                 '원',
                                                                                                                 '만'), machulRate, gye_gigan, nation, jongsung(nation,'이다'))
            return {'title':title, 'article':article, 'table': '종료일'}

        else:

            tot = f[f.index('계약금액(원)')+1]
            machulRate =  f[fs.index('매출액대비(%)')+1]
            if True in [float(machulRate) > 10]:
                if True in [float(tot) > 5000000000, float(machulRate) >= 100]:
                    opCorpNm = f[f.index('계약상대')+1].replace('주식회사','').replace('(주)','').replace('㈜','').strip()
                    opCorpNm_sentence = ''
                    if opCorpNm == '-':
                        opCorpNm_sentence = ''

                    else:
                        business=None
                        if not bool(re.search(r'[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]', opCorpNm)):
                            if bool(re.search(r'samsung',opCorpNm.lower())):
                                opCorpNm_sentence = '삼성({})과 '.format(opCorpNm)
                                title_jaebeol = '삼성에 '
                            elif bool(re.search(r'LG',opCorpNm)):
                                opCorpNm_sentence = 'LG({})와 '.format(opCorpNm)
                                title_jaebeol = 'LG에 '
                            elif bool(re.search(r'hyundai',opCorpNm.lower())):
                                opCorpNm_sentence = '현대({})와 '.format(opCorpNm)
                                title_jaebeol = '현대에 '
                            else:
                                nation = f[f.index('판매ㆍ공급지역')+1]
                                try:
                                    business=  f[f.index('-주요사업')+1]
                                except:
                                    business = '-'
                                b_con = True
                                if business == '-':
                                    business = '업체'
                                    b_con = False
                                if not bool(re.search(r'업체$', business)):
                                    if b_con ==False:
                                        business = business + ' 업체'
                                    else:
                                        business = business + ' 관련 업체'
                                opCorpNm = "{} {}({})".format(nation, business, opCorpNm)

                                if business == None:
                                    temp_jongsung = jongsung(opCorpNm, '와과')
                                else:
                                    temp_jongsung = jongsung(business, '와과')
                                opCorpNm_sentence = '{}{} '.format(opCorpNm, temp_jongsung)


                    naeYong =  f[f.index('- 체결계약명')+1].strip()
                    if not bool(re.search(r'[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]', naeYong)):
                        naeYong = ''
                    else:
                        naeYong = re.sub(r'계약$', '', naeYong) + ' '


                    gye_gigan = ""
                    try:
                        gs_0 = pandas.to_datetime(f[f.index('시작일')+1], format= '%Y-%m-%d')
                        gs_1 = pandas.to_datetime(f[f.index('종료일')+1], format= '%Y-%m-%d')
                        if (gs_0 != '-') & (gs_1 != '-'):
                            gyeStart = "{}년 {}월{}일".format(gs_0.year, gs_0.month, gs_0.day)
                            gyeEnd = "{}년 {}월{}일".format(gs_1.year, gs_1.month, gs_1.day)
                            gye_gigan = " 계약기간은 {}부터 {}까지다.".format(gyeStart, gyeEnd)
                    except:
                        pass

                    jogun = ''
                    if '주요 계약조건' in f:
                        jo = f[f.index('주요 계약조건')+1]
                        if jo not in ['-', '']:
                            jogun = " 주요 계약조건은 '{}'{}.".format(jo, jongsung(jo, '이다'))

                    title = "{}, {}{}원 공급계약...매출액 대비 {}%".format(crpNm, title_jaebeol, banolim(tot,'원','억'), machulRate)
                    article = """
                    {}{} {}{}원 규모의 {}공급계약을 체결했다고 {}일 공시했다. 이는 최근 매출 대비 {}에 해당하는 규모다.{}
                    """.format(crpNm, jongsung(crpNm, '은는'), opCorpNm_sentence, banolim(tot, '원', '만'), naeYong, today,
                               machulRate, gye_gigan)

                    article = article + jogun
                    return {'title':title, 'article':article, 'table': '종료일'}
                else:
                    raise Exception("50억 미만이거나 100% 미만")
            else:
                raise Exception("매출액대비 10% 미만")
dict_can['단일판매ㆍ공급계약체결']=danil


#최대주주등소유주식변동신고서
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
    if len(jusic.keys()) ==1:
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

    if (stock_code in kospi200()['num_list']) or \
            (abs(float(jeon_jibun) - float(hu_jibun))>1) :
        force = True


    if force:
        return {'title':title, 'article':article, 'table':['보고일자','증감']}
    else:
        raise Exception("필터에서 걸러짐.")
dict_can['최대주주등소유주식변동신고서'] = juju_byun


#임원ㆍ주요주주 특정증권등 소유상황보고서
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
dict_can['임원ㆍ주요주주특정증권등소유상황보고서'] = juju_state


#최대주주변경
def juju_change(f=None, fs=None, crpNm=None, sou_html=None, **kwargs):

    crpNm = crpNm
    today = date.today().day
    before_change =  f[f.index("변경전")+2].replace('(주)','').replace('㈜','')
    if bool(re.search(r'공단$', before_change)):
        before_change = re.sub(r'공단$','',before_change)
    after_change =  f[f.index("변경후")+2].replace('(주)','').replace('㈜','')
    if bool(re.search(r'공단$',after_change)):
        after_change = re.sub(r'공단$','',after_change)

    #전후 주식, 비율 값들
    before_ju = f[f.index("변경전")+4]
    before_bi = f[f.index("변경전")+6]

    after_ju = f[f.index("변경후")+4]
    after_bi = f[f.index("변경후")+6]

    ### 주요기관 ###
    VIP = False
    before_VIP = False
    after_VIP = False
    VIP = ['국민연금']
    v = 0
    if before_change in VIP:
        before_VIP = True
        VIP = True
        VIP_name = before_change
        v+=1
    elif after_change in VIP:
        after_VIP = True
        VIP_name = after_change
        VIP = True
        v+=1
    if v ==2:
        before_VIP=False
        after_VIP=False


    #주식 단위
    danwi =  re.findall(r'(?<=\().*(?=\))',f[f.index("변경전")+3] )[0]

    #변경사유
    reason = f[f.index("변경사유")+1]

    #변경일자
    change_day =  word_to_date(f[f.index("변경일자")+1])

    title = ''

    if VIP:
        title += '['+ VIP_name  +']'

    temp = f[fs.index("변경전최대주주")-1]
    title += '{} 최대주주 {} → {}'.format(crpNm, temp, after_change)

    article = """
    {crpNm}{jong_corp} 최대주주가 {before_change}에서 {after_change}으로 변경됐다고 {today}일 공시했다.<br><br>
    변경 사유는 {reason}{reason_jong}. {after_change}은 {after_ju}주({after_bi}%)를 보유해 {crpNm}의 최대주주가 됐다. {before_change}의 지분은 
    {before_ju}주({before_bi}%)다.
    """.format(
        crpNm = crpNm,
        jong_corp = jongsung(crpNm,'은는'),
        before_change = before_change,
        today = today,
        reason = reason,
        reason_jong = jongsung(reason,'이다'),
        after_change = after_change,
        after_ju = banolim(after_ju, danwi, '일') ,
        after_bi = after_bi,
        before_ju =  banolim(before_ju, danwi, '일') ,
        before_bi = before_bi
    )

    return {'title':title, 'article':article, 'table': ['변경내용', '변경일자']}
dict_can['최대주주변경'] = juju_change



#### 영업실적 ######

#연결재무제표기준영업(잠정)실적(공정공시)
def yg_siljeok(f=None, fs=None, crpNm=None, sou_html=None, cmd=None, **kwargs):
    return siljeok(f=f, fs=fs, crpNm=crpNm, sou_html=sou_html, cmd='yeon')
dict_can['연결재무제표기준영업(잠정)실적(공정공시)'] = yg_siljeok

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
    if yeon_gyeol: #연결인지 확인
        jepyo= ' 연결재무제표'
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
        for i in fs:
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

    key_1cha = ['매출액', '영업이익', '당기순이익']
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


    bool_1cha = True
    for i in key_1cha:
        if _1cha[i]['d_h'] in ['0', '-']:
            bool_1cha = False
        else:
            bool_1cha = True
            break
        #하나라도 0, -  아닌게 있으면 True가 되면서 for loop을 멈추고 나옴.

    ##text 작성구간##


    ###1차 (매출액, 영업이익, 당기순이익) 작성구간
    text_1cha = ''
    #이마트가 14일 공시한 바에 따르면 지난 {12}{월} 동안
    # 매출액은 1조3230억원으로 전년대비 17.5% 증가,

    #전' '대비 {   }, / '흑자전환', '~~프로 증가'
    #전년비 증가율 있을 경우 하고, 없으면 전기대비로 함. // '흑자전환' 멘트 있을 경우 넣고, 숫자면 숫자로 채워줌.
    def plma_func(data, yg_word):
        if data not in ['0', '-','']:
            # if data == d_y_r:
            #     yg_word = '년' #전'년'대비
            # elif data == d_g_r:
            #     yg_word = '기'
            if bool(re.search('전환', data)):
                plma_ment = '전{}대비 {}, '.format(yg_word, data)
            else:
                plma = '증가' if float(data) >0 else '감소'
                plma_ment = '전{}대비 {}% {}, '.format(yg_word, data, plma)
            return plma_ment
        return '오류'

    bool_tit_ind = False  #제목에 넣을 값 뽑기
    bool_tit_plma = False # 제목에 들어갈 증감 뽑기

    if bool_1cha:
        for i in key_1cha:
            d_h = _1cha[i]['d_h']
            d_y_r = _1cha[i]['d_y_r']
            d_g_r = _1cha[i]['d_g_r']
            if d_h not in ['0', '-']: #값이 있는 경우

                if yeon_gyeol:  #연결재무제표일 경우 키값에 이게 포함됨.
                    if i =='지배기업소유주지분순이익':
                        i = '지배기업 소유주지분 순이익'
                text_1cha += '{}{} {}원으로 '.format(i, jongsung(i, '은는'), banolim(d_h, danwi,danwi))

                if not bool_tit_ind: #아직 안정해졌으면 정해줌
                    tit_ind = i
                    tit_d_h = d_h
                    bool_tit_ind =True

                plma_ment = plma_func(d_y_r, '년')

                if plma_ment == '오류':
                    plma_ment = plma_func(d_g_r, '기')
                    if plma_ment == '오류':
                        raise Exception("1차 증감 문장에서 이상 발생")

                text_1cha += plma_ment
                if not bool_tit_plma:
                    tit_plma = plma_ment[:-2]
                    bool_tit_plma = True

        text_1cha = text_1cha[:-2] +'했다.'


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
            name = re.sub(r'[\(\),-]' , '', fs[i]).replace('\xa0','').replace(' ','')
            if name =='기타':
                pass
            else:
                _2cha[name] = {}
                _2cha[name]['d_h']= fs[i+1] #당기, 현금액
                _2cha[name]['d_y_r']= inc_rate(fs[i+5]) #당기, 전년대비 비율
                _2cha[name]['d_g_r']= inc_rate(fs[i+3]) #당기, 전기대비 비율

        for i in _2cha.keys():
            d_h = _2cha[i]['d_h']
            d_y_r = _2cha[i]['d_y_r']
            d_g_r = _2cha[i]['d_g_r']

            if d_h not in ['0', '-']: #값이 있는 경우
                text_2cha += '{}{} {}원으로 '.format(i, jongsung(i, '은는'), banolim(d_h, danwi,danwi))
                if not bool_tit_ind: #아직 안정해졌으면 정해줌
                    tit_ind = i
                    tit_d_h = d_h
                    bool_tit_ind =True


                plma_ment = plma_func(d_y_r, '년')
                if plma_ment == '오류':
                    plma_ment = plma_func(d_g_r, '기')
                    if plma_ment == '오류':
                        raise Exception("2차 증감 문장에서 이상 발생")

                text_2cha += plma_ment
                if not bool_tit_plma:
                    tit_plma = plma_ment[:-2]
                    bool_tit_plma = True

        text_2cha = text_2cha[:-2] +'했다.'


    #이마트가 12일 제출한 영업실적 공시에 따르면 이마트의 지난 12월
    start_text = "{}{} {}일 제출한{} 영업실적 공시에 따르면 {}의 지난 {}{} ".format(
        crpNm,jongsung(crpNm,'이가') ,today, jepyo, crpNm, str(dang), gigan)

    if bool_1cha:
        article = start_text + text_1cha
        if bool_2cha:
            article +="<br><br>"+text_2cha
    else:
        article = start_text + text_2cha
    article = article.replace('-','').replace('+','')

    ###제목에 들어갈것들 위에서 만들어져 들어옴.####
    #이마트, 12월 매출 1.3조..전년비 17.5% 증가"
    title = "{}, {}{} {} {}원...{}".format(
        crpNm,
        str(dang),
        gigan,
        tit_ind,
        banolim(tit_d_h, danwi, '억'),
        tit_plma

    ).replace('-','').replace('+','')

    return {'title':title, 'article':article, 'table': ['실적내용', '정보제공내역', -2]}
dict_can['영업(잠정)실적(공정공시)'] = siljeok




if __name__ == "__main__":
    # print(f)
    # otherCorp(f, 'dd')
    # temp = a_yuJeung(f, crpNm)
    # print(temp['title'])
    # print(temp['article'])
    print([*dict_can])
#dict_keys(['타법인주식및출자증권처분결정', '현금ㆍ현물배당결정', '주식배당결정', '주요사항보고서(유상증자결정)'])

# def fuck():
#     print(list_can)  # 다른 파일에서 fuck()을 불러내도  article1 파일 안의 list_can 이 프린트됨.



