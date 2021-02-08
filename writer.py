###메인 진행판. 여기서 각 모듈들을 불러와 조립함#####

import post
import article1, sys
from article1 import dict_can
from list_watch import list_watch
import table
from rcpNo_to_table import rcpNo_to_table
import time, json
from toolBox import real_do

if __name__ == '__main__':
    start = time.time()
    list_can = dict_can.keys()

    # print(watch_list)
    todo_list = []
    for j in [1,2,3,4,5,6,7,8]:
        watch_list = list_watch(j)
        for i in range(0, len(watch_list)):
            if watch_list.iloc[i]['report_nm'] in list_can:
                todo_list.append(watch_list.iloc[i]['rcept_no'])


def writer(rcept_no = None, stock_code = None):

    # 20201208900383, 20201207900557, 20201208900490
    #현물배당
    #20201211900186
    #주식배당 20201211900097
    #유상증자 20201210000537, 20201210000256, 0201210000266
    #단일계약 (비건설) 20201214900228(영어이름 어케할건지 과제), 20201214900210, 20201215901225, 20201210900098
    source =rcpNo_to_table(rcept_no)  # list와 html 딕셔너리를 가져옴. list는 공시의 표 부분을 리스트로 쪼갠것. html은 공시 전체 html 원문

    sou_list = source['list']
    sou_list_s =  source['l_without_space']
    sou_html = source['html']
    crpNm = source['crpNm']
    bogoNm= source['bogoNm']
    url = source['url']
    url0 = source['url0']

    dict_can = article1.dict_can  # 처리 가능한 보고서, 함수 짝 {'타법인 주식 및 출자증권 처분결정' : otherCorp}
    art_fun = dict_can[bogoNm] # 보고서 이름에 맞는 함수 가져옴

    ##list는 기사 원문을 만듦.
    temp_artc = art_fun(f = sou_list, fs =sou_list_s, crpNm = crpNm, sou_html =sou_html, stock_code = stock_code, bogoNm= bogoNm) #
    # 리스트를 넣으면 기사가 나옴. title과
    # article
    # 딕셔너리로.
    #기사작성 함수로부터 나온 3가지 리턴.
    #제목에 배정
    title = '(테스트)' + temp_artc['title']
    #기사에 배정
    article = temp_artc['article']
    #테이블 나누는 기준
    gijun = temp_artc['table']

    ##html은 테이블을 만듦
    global table
    table1 = table.table(sou_html, gijun)

    article = article + table1 #+"<br>※해당 기사는 뉴스1 경제·산업부가 자체 개발한 뉴스봇에 의해 작성됐습니다."
    #
    info = json.dumps({"rcept_no":rcept_no, "bogoNm":bogoNm, "url":url, "url0":url0}, ensure_ascii=False) #ensure_ascii
    # 이렇게 해야 한글
    # 안깨짐.
    # post.do(title=title, article=article,  op ='new_article')  #기사 올리기.
    post.do_temp(title=title, article=article,  op ='None', info=info)

    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
    port = port[0]
    if str(port) == '5231':
        global real_do
        if bogoNm in real_do:
            post.do_mbot(title=title, article=article,  op ='set_disc', rcept_no=rcept_no, ori_url=url0, corp_name= crpNm,
                     stock_code = stock_code)
    return {"title":title, "info":info}

if __name__ == '__main__':
    # print(todo_list)
    # print(todo_list)
    #
    writer(20210208900234)
    # print(real_do)
    #
    # for i in todo_list:
    #     try:
    #         writer(i)
    #         print(str(i) + ' success')

    #     except:
    #         print(str(i)+ " failed", sys.exc_info()[0])
    # # #
    #


    end = time.time()
    print(end - start - 5)