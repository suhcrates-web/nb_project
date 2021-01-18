from bs4 import BeautifulSoup
import re


if __name__ == "__main__":
    pyo = open('pyo.html', 'r', encoding='utf-8')
    pyo = pyo.read()
    pyo = BeautifulSoup(pyo, 'html.parser')


def table(html, gijun):
    gijun_0=None
    cmd =''
    if isinstance(gijun , list):   #리스트가 아닌 경우 그냥 아래쪽 기준으로 적용
        if len(gijun)==3:  #3번째에 특수명령신호
            cmd = gijun[2]
        gijun_0 = gijun[0]  #리스트가 들어올 경우 0번째는 위쪽 기준으로
        gijun = gijun[1]   #1번째는 아래쪽 기준으로 배정.

    #cmd :
        #-2  : 두번째 인자의 앞부분까지 끊어올리기.

    pyo = html
    pyo = pyo.findAll('tr')
    #아랫기준 단어를 포함한 요소의 인덱스를 찾아냄
    i=0
    a=False
    while a ==False:
        if bool(re.search(str(gijun),str(pyo[i]))) ==True:
            a=True

        else:
            i = i+1
    if cmd == -2:
        i = i-1

    # 윗기준 단어를 포함한 요소의 인덱스를 찾아냄
    if gijun_0 is not None:
        j=0
        a=False
        while a ==False:
            if bool(re.search(str(gijun_0),str(pyo[j]))) ==True:
                a=True
            else:
                j = j+1

    # j ~ i+1까지 출력
    tab = ''
    # j~i+1
    if gijun_0 is not None:
        temp = pyo[j:i+1]
    # ~i+1
    else:
        temp = pyo[:i+1]

    for a in temp:
        a= str(a)
        a = re.sub(r'\s+','  ',a)
        a = re.sub(r'<br.>','',a)
        tab = tab + a


    tab = '''
    <br><br>
    <h3><공시 원문 ></h3>
    <table border="1" bordercolordark="white" bordercolorlight="#666666" cellpadding="1" cellspacing="0" id="XFormD6_Form0_Table0" style="font-size:10pt;border:1px solid #7f7f7f;">
    <tbody>
    ''' + tab +'''
    </tbody>
    </table>
    '''
    return tab

# <table border="1" bordercolordark="white" bordercolorlight="#666666" cellpadding="1" cellspacing="0" id="XFormD6_Form0_Table0" style="margin:0px 0px 20px 0px;width:600px;font-size:10pt;border:1px solid #7f7f7f;">


if __name__ == "__main__":
    # print(pyo)
    print(table(pyo,['보고서<br/>', '이번보고서']))