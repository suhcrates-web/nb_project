from list_watch import list_watch
import pandas
from article1 import dict_can
import re
#from rcpNo_to_table  # 이건 불러올 수 있는 형태로 다듬어놓자.

# new_list = list_watch().iloc[:16]
# old = list_watch().iloc[9:]
# new_list.to_csv('test1.csv')
# old.to_csv('old.csv')

list_can = dict_can.keys()

new_table = pandas.read_csv('test1.csv', header=0)
old_table = pandas.read_csv('old.csv', header=0)

rcpNo_checked = []
rcpNo_checked = old_table.loc[:,'rcept_no'].to_list() + rcpNo_checked #지금까지 체크된 것의 보고서 번호

new_list = new_table.loc[:,'rcept_no'].to_list() #새로 불러온 목록의 보고서 번호



to_be_processed = []  #new_list 중 처리돼야 할 것들
for new in new_list:
    if new not in rcpNo_checked:

        temp = str(new_table.loc[new_table['rcept_no']== new]['report_nm'])[1:].strip() #보고서 번호가 new인 행의 report_nm을
        # 뽑아 앞의 번호를 삭제하고 stript 시킴 -> 보고서 이름이 됨
        temp = re.sub(r'\n.*','',temp)

        if temp in list_can:  #새로운 보고서의 제목이 '처리할 수 있는 유형' 목록에 들어있으면 'to_be_processed' 리스트로 넣어짐.
            to_be_processed.append(new)


# to_be_processed : 새로 프로세스 해야할 보고서 넘버

###process##
#여기서 프로세스를 거칠듯


rcpNo_checked = to_be_processed + rcpNo_checked   # 프로세스를 거친 넘버는 '이미 체크된 넘버'에 넣음
# print(rcpNo_checked)
#rcpNo_to_table 패치 불러오기.


if __name__ == '__main__':
    print(list_can)
# print([str(new_table.loc[new_table['rcept_no']== x]['report_nm'])[1:].strip() for x in to_be_processed]) #내용확인