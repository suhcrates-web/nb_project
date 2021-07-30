from writer import writer
from list_watch import list_watch
from article1 import dict_can
from datetime import datetime
import csv, time, re
import traceback
from telebot import bot, bot_public
from toolBox import real_do



today = datetime.today().strftime(format='%Y%m%d')
now= datetime.today().strftime(format='%H:%M')

#tot_list_0 : split 하기 전 그대로
#tot_list :한 것 중 보고서번호를 포함한 전체 리스트
#list_processed : tot_list의 보고서번호만
def process(cycle):
    list_processed=[]  #한 것 중 보고서번호만 추린것
    with open('data/list_done/'+today+'.csv', 'a+', encoding='utf-8') as f:
        f.seek(0)
        tot_list_0 = f.readlines()
        #빈 경우 만들어야.
        tot_list = []
        for i in tot_list_0:
            temp_list = i.split(',')
            tot_list.append(temp_list)
            list_processed.append(temp_list[0])
    if tot_list_0 ==[]:
        first_line=True
    else:
        first_line=False

    print(list_processed)

    list_can = list(dict_can.keys())
    watch_all_list = []
    watch_all_dict = {}

    if cycle == 1:
        arr = [1,2,3,4,5,6,7,8]
    elif cycle>1:
        arr = [1]
    for j in arr:
        watch_list = list_watch(j) ##판다스 표 그대로 들어옴
        for i in range(0, len(watch_list)):
            corp_name = watch_list.iloc[i]['corp_name']
            stock_code = watch_list.iloc[i]['stock_code']
            report_nm = watch_list.iloc[i]['report_nm'].replace(' ','')   #api에서 온 보고서이름 그대로임.
            report_nm_raw = report_nm

            # report_nm_raw 는 원래 제목 그대로
            # report_nm 은 특수경우 괄호내용을 떼고 일반화한것.
            rm = watch_list.iloc[i]['rm']

            cmd = ''

            #괄호 떼고 일반화. 여기서 report_nm과 report_nm_raw가 달라짐.
            #해당 키워드 있을때만  괄호 떼기
            general_list = ['사업보고서'] #조회공시요구 는 아직
            for k in general_list:
                if bool(re.search(k, report_nm)):
                    cmd = re.findall(r'(?<=\()[^\(\)]+(?=\))', report_nm)
                    report_nm = re.sub(r'\([^\(\)]+\)', '', report_nm)  # 괄호 안에 있는걸 지워버림
                else:
                    cmd = ''

            if report_nm in list_can:  # 처리가능 보고서 목록과 비교.
                rcept_no = watch_list.iloc[i]['rcept_no']
                watch_all_dict[rcept_no] = {}
                watch_all_dict[rcept_no]['report_nm'] = report_nm  #일반화된 보고서 이름
                watch_all_dict[rcept_no]['report_nm_raw'] = report_nm_raw  #보고서이름 원문
                watch_all_dict[rcept_no]['corp_name'] = corp_name #커맨드
                watch_all_dict[rcept_no]['stock_code'] = stock_code #커맨드
                watch_all_dict[rcept_no]['cmd'] = cmd #커맨드
                #watch_all_dict[rcept_no]['rm'] = rm # 비고. 유코채넥


    watch_all_list = list(watch_all_dict.keys())[:10]
    print(watch_all_list)

    todo_list = []

    #watch_all_list : 지금 떠있는 보고서 전부.
    #todo_list : 그 중 processed 에 없는 걸 추린 리스트.
    for i in watch_all_list:
        if i not in list_processed:
            todo_list.append(i)
    print(todo_list)


    #todo_list를 처리.
    if todo_list != []:
        list_done = [] #처리된 항목
        title_list = [] #기사제목 리스트임.
        title_real_list = [] #집배신에 보내는 리스트
        for i in todo_list:

            try:
                stock_code = watch_all_dict[i]['stock_code']
                wrote = writer(rcept_no = i, stock_code = stock_code )  # 기사작성, post 둘다 함. {title, info} 를 내놓음
                title = wrote['title']
                info = wrote['info'] #recept_no , bogoNm, url  포함.
                message = 'success' #기록에 남길 메세지
                title_list.append(title) #텔레그램 보낼 리스트 (이제 안보냄. 진짜는 title_real_list)

                if watch_all_dict[i]['report_nm'] in real_do:
                    title_real_list.append(title)


            except Exception as e :
                message = 'fail m:'+str(e)


            list_done_0 = [] #처리된 항목의 하위 리스트. 이 안에 개별 보고서 번호, fail/success, 보고서 name_raw
            list_done_0.append(i)  #1번 : 보고서 번호
            list_done_0.append(message) #2번 : fail/success
            list_done_0.append(watch_all_dict[i]['report_nm_raw'])  #3번 : 보고서 이름
            list_done_0.append(watch_all_dict[i]['corp_name']) # 4번 회사 이름
            list_done.append(list_done_0)

        if len(title_list) == 1:
            bot_public('c', title_list[0] + "\n올렸습니다!\n" + "http://testbot.ddns.net:5231/bot_v3")
        elif len(title_list) >1:
            bot_public('c', title_real_list[0] + "\n 외 " + str(len(title_list) - 1) + "건 "
                                                                               "올렸습니다!\n" + "http://testbot.ddns.net:5231/bot_v3")

        if len(title_real_list) == 0:
            print("집배신 보낸 거 없음")
        elif len(title_real_list) ==1:
            bot('c' ,title_real_list[0] +"\n올렸습니다!\n"+"http://testbot.ddns.net:5231/bot_v3")
        else:
            bot('c',title_real_list[0] +"\n 외 "+ str(len(title_list)-1)+"건 "
                                                                      "올렸습니다!\n"+"http://testbot.ddns.net:5231/bot_v3")


        #r+는 앞에서부터 덮어씌움.
        with open('data/list_done/'+today+'.csv', 'a+', encoding='utf-8', newline='') as f:
            if first_line == False: #첫줄이 아닌 경우
                if not bool(re.search(r'\n$', tot_list[-1][-1])):
                    linebreak= False
                else:
                    linebreak = True
                for i in list_done:
                    if linebreak == False:
                        f.writelines(['\n',i[0],',',i[1],',',i[2],',',i[3],'\n'])
                        linebreak=True
                    else:
                        f.writelines([i[0],',',i[1],',',i[2],',',i[3],'\n'])
                    print(str(i[0]) + ' '*(15-len(str(i[0]))) + i[1] + ' '*(8-len(i[1])) + i[2]+ ' '*(24-len(i[2]))+' '+ i[3])
            else: #첫줄인 경우
                for i in list_done:
                    f.writelines([i[0],',',i[1],',',i[2],',',i[3],'\n'])
                    print(str(i[0]) + ' '*(15-len(str(i[0]))) + i[1] + ' '*(8-len(i[1])) + i[2] + ' '*(24-len(i[2]))+' '+ i[3])
    return ''

def timeline():
    now = datetime.today().strftime(format='%H:%M')
    if True:#now < '09:10':
        bot_public('o', "뉴스봇 가동 시작 \n 아침9시~저녁7시반 가동 \n 문의사항 kakao: suhcrates1\n 개발자 : 서영빈 연합인포맥스 기자")


    op = True
    cycle=1
    while op == True:
        process(cycle)
        now= datetime.today().strftime(format='%H:%M')
        if now<'19:00':
            print(str(now)+' '+  str(cycle) + " Cycle done")
            cycle += 1
            time.sleep(120)
        else:
            bot('c' , str(now)+ " 뉴스봇 퇴근 zz")
            return 'end'

if __name__ == '__main__':
    timeline()
