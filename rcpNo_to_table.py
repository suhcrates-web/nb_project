# 보고서 넘버 넣으면  공시를 리스트화한 것과  원문 그대로의 html을 뱉어냄 #

#재무제표 크롤링 성공 ㅋㅋ
import requests, xmltodict, json, pandas, re, time, csv
from bs4 import BeautifulSoup


if __name__ == "__main__":
    #20201210000537 #유상증자
    #20201208000293 # 유상증자(정정)

    rcpNo = '20210311800330'

def rcpNo_to_table(rcpNo):
    #rcpNo를 통해 dcmNo를 추론. 그래야 공시 html 가져올 수 있음.
    url0 = 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo='+str(rcpNo)  #dcfNo는 여기서 추론할 수 있긴 함.
    # <a href="#download" onclick="openPdfDownload('20201207800563', '7624179'); return false;" > 여기 숨어있음.
    content = requests.get(url0)#.content.decode('utf-8')
    content = BeautifulSoup(content.text, 'html.parser')
    # print(url0)


    #html인지 찾기
    viewDoc = re.findall(r'viewDoc\(.*\)',str(content))[0]
    if_html = bool(re.search(r'HTML', viewDoc))
    if_xsd =  bool(re.search(r'dart3.xsd', viewDoc))

    crpNm = content.find('a',{'href': '#companyview'})['title'] # 기업이름. 임시로 여기에 둠
    bogoNm = content.find('option', {'value':'rcpNo={}'.format(rcpNo)})['title'] #보고서 이름

    content = content.find('a',{'href':'#download'})['onclick']
    dcmNo = re.findall(r'\'(\d{7})\'', content)[0].replace("'",'')  # dcm넘버 찾기

    time.sleep(5) # 5초 쉼
    #rcpNo와 dcmNo를 통해 공시 html을 가져옴
    if if_html:
        url = 'http://dart.fss.or.kr/report/viewer.do?rcpNo='+ str(rcpNo) +'&dcmNo=' + str(dcmNo)  \
              +'&eleId=0&offset=0&length=0&dtd=HTML' #보고서 형식 공시는 dtd=HTML 쿼리가 있으면 깨짐.
    elif if_xsd:
        url = 'http://dart.fss.or.kr/reportKeyword/viewer.do?rcpNo='+str(
            rcpNo)+'&dcmNo='+ str(dcmNo) +'&eleId=1&offset=667&length=3000&dtd=dart3.xsd&keyword=#keyword'
    else:
        url = 'http://dart.fss.or.kr/report/viewer.do?rcpNo='+ str(rcpNo) +'&dcmNo=' + str(dcmNo) \
              +'&eleId=0&offset=0&length=0'
    # print(url)
    content = requests.get(url)#.content.decode('utf-8')
    content = BeautifulSoup(content.text, 'html.parser')

    cont_orig =content  #테이블의 재료가 될 html 원문

    contents = content.findAll('td') #
    l = []
    ls = []  #여백을 제거한 버전
    lr = [] #전처리 거치지 않은 완전 raw한 버전.
    for con in contents:
        ##### l, ls ,lr 채우는 구간
        # con = con.text.replace(' ','').replace(',','')
        con = con.text.strip()
        # lr.append(con.replace('\r','\\r').replace('\n','\\n')) #이부분은 테스트 위한 것.
        if not if_html:  #html로 파싱한 문서가 아닌 경우(보고서 형식) \xa0 가 중간에 껴있음. 이걸 제거하기 위한 것.
            con = con.replace(u'\xa0 ', '').replace(u'\xa0', '')
        # lr.append(con.replace('\r','\\r').replace('\n','\\n')) #이부분은 테스트 위한 것.  # lr은 폐기함.
        con = re.sub(r'(?<=\d),(?=\d)', '',con)  # ?<= look behind  , ?=  look ahead
        con = re.sub(r'^\d\. ','',con).replace('\n','').replace('\r','').replace('\xa0','')
        con = re.sub(r'\s+',' ',con) ## 여러칸의 공백은 모두 한 칸으로 줄이기.
        con = con.strip()#.replace(',','')
        l.append(con)

        con = re.sub(r'\s+','',con)
        # con = con.replace(' ','')
        ls.append(con)  # 식별을 쉽게 하기 위해 여백을 제거한 버전


    return {'html':cont_orig, 'list':l, 'l_without_space':ls,  'crpNm': crpNm, 'bogoNm':bogoNm,
    'url':url, 'url0':url0}
    #html은 table로, list는 article로 가서 가공됨. list 는 writer의 source로 연결됨

if __name__ == "__main__":
    result = rcpNo_to_table(rcpNo)
    print(result['url0'])
    print(result['url'])
    print(result['list'])
    print(result['l_without_space'])
    # print(result['bogoNm'])
    f=open('test.txt', 'w', encoding='utf-8')
    f.writelines('%s\n' %x for x in result['list'])
    f.close()

    csv.register_dialect('pipes', delimiter = '|')

    f= open('pyo.html', 'w', encoding='utf-8')
    f.write(str(result['html']))
    f.close()
