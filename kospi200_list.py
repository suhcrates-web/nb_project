import requests
from datetime import date, timedelta
import time, re
from bs4 import BeautifulSoup
import os, glob, json


### 이거로 바뀜.######
#코스피200 의 이름과 넘버, 코스닥 150의 이름과 넘버를 뱉음. 목록은 한달마다 업데이트.
#결과값은 dict 이며 키값은'kospi_name' 'kospi_num' 'kosdaq_name' 'kosdaq_num'. 'all_name' 'all_num' 각각 리스트로 불려옴.
def kos_list():
    tomonth = date.today().strftime('%Y%m')
    today = date.today().strftime('%Y%m%d')
    w1_ago =  (date.today() - timedelta(days=7)).strftime('%Y%m%d')
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    result_dict = {}
    result_dict['all_name'] = []
    result_dict['all_num'] = []
    #이 펑션이 두번 반복됨. 파일 검색, 없으면 만들고 있으면 가져와 result_dict를 채움.

    glob_temp_nums = [] # maek_and_get 세번 반복하는 과정에서 중복 등록 방지 위함.
    def make_and_get(kowhat):

        if kowhat in ['byeondong_wanhwa']:
            filename = kowhat+str(today)+'.csv'
        else:
            filename = kowhat+str(tomonth)+'.csv'
        if not os.path.isfile(f'data_share/{kowhat}/'+ filename):
            with open(f'data_share/{kowhat}/'+ filename,'w') as f:
                if kowhat == 'kospi':
                    q_data = {
                        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
                        'tboxindIdx_finder_equidx0_0': '코스피 200',
                        'indIdx': '1',
                        'indIdx2': '028',
                        'codeNmindIdx_finder_equidx0_0': '코스피 200',
                        'param1indIdx_finder_equidx0_0': '',
                        'trdDd': str(today),
                        'money': '3',
                        'csvxls_isNo': 'false'
                    }
                elif kowhat== 'kosdaq':
                    q_data = {
                        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
                        'tboxindIdx_finder_equidx0_0': '코스피 200',
                        'indIdx': '1',
                        'indIdx2': '028',
                        'codeNmindIdx_finder_equidx0_0': '코스피 200',
                        'param1indIdx_finder_equidx0_0': '',
                        'trdDd': str(today),
                        'money': '3',
                        'csvxls_isNo': 'false'
                    }
                elif kowhat== 'byeondong_wanhwa': #변동성완화장치 발동종목 현황
                    q_data = {
                        'bld': 'dbms/MDC/STAT/issue/MDCSTAT22401',
                        'mktId': 'ALL',
                        'inqTpCd1': '01',
                        'viKindCd': 'ALL',
                        'tboxisuCd_finder_stkisu1_2': '전체',
                        'isuCd': 'ALL',
                        'isuCd2': 'ALL',
                        'codeNmisuCd_finder_stkisu1_2':'',
                        'param1isuCd_finder_stkisu1_2': 'ALL',
                        'strtDd': str(w1_ago),
                        'endDd': str(today),
                        'csvxls_isNo': 'true'
                    }
                result = requests.post(url, q_data)
                dicts = json.loads(result.content.decode(encoding='utf-8'))
                dicts = dicts['output']
                if kowhat in ['byeondong_wanhwa' ]: #변동성완화대상일 경우. 7일치를 비교하므로 중복이 많아
                    temp_nums = []
                    for i in dicts:
                        temp_num = i['ISU_NM']
                        if not temp_num in temp_nums:  #중복된거 걸러주는 장치
                            temp_nums.append(temp_num)
                            try:
                                f.writelines([i['ISU_NM'],',',i['ISU_CD'], '\n'])
                            except:
                                pass
                        else:
                            pass
                else:
                    for i in dicts:
                        try:
                            f.writelines([i['ISU_ABBRV'],',',i['ISU_SRT_CD'], '\n'])
                        except:
                            pass
                time.sleep(3)  # sleep은 해당 파일이 없어서 새로 만들때만 적용됨.
        try:
            with open(f'data_share/{kowhat}/'+ filename) as f:
                name_list= []
                num_list = []
                result = f.readlines()
                for i in result:
                    i = i.split(',')
                    temp_num = i[1]
                    if not temp_num in glob_temp_nums:
                        glob_temp_nums.append(temp_num)
                        name_list.append(i[0])
                        num_list.append(i[1].strip())
                        result_dict['all_name'].append(i[0])
                        result_dict['all_num'].append(i[1].strip())
                    else:
                        pass

        except:
            list = glob.glob(f'data_share/{kowhat}/*')
            latest = max(list, key= os.path.getctime)
            with open(latest) as f:
                name_list= []
                num_list = []
                result = f.readlines()
                for i in result:
                    i = i.split(',')
                    temp_num = i[1]
                    if not temp_num in glob_temp_nums:
                        glob_temp_nums.append(temp_num)
                        name_list.append(i[0])
                        num_list.append(i[1].strip())
                        result_dict['all_name'].append(i[0])
                        result_dict['all_num'].append(i[1].strip())
                    else:
                        pass

        result_dict[f'{kowhat}_name'] = name_list
        result_dict[f'{kowhat}_num'] = num_list
        return None

    make_and_get('kospi')
    make_and_get('kosdaq')
    make_and_get('byeondong_wanhwa')
    return result_dict

#
# def kospi200():
#     today = date.today().strftime('%Y%m%d')
#     filename = 'kos'+str(today)+'.csv'
#     if not os.path.isfile('data/kospi200/'+filename):
#         with open('data/kospi200/'+filename,'w') as f:
#             for i in [1,2,3,4]:
#                 url = 'https://finance.naver.com/sise/sise_market_sum.nhn?page='+str(i)
#                 data = requests.get(url)
#                 content = BeautifulSoup(data.text, 'html.parser')
#                 trs = content.find('caption', text='코스피').find_next_sibling('tbody').find_all('tr')
#                 for i in trs:
#                     try:
#                         href= i.find('a', {'class':'tltle'})['href']
#
#                         crpNumber = re.findall(r'(?<==)\d*$', href)[0]
#                         crpName =i.find('a', {'class':'tltle'}).text
#                         f.writelines([crpName, ',', crpNumber, '\n'])
#
#
#                     except :
#                         pass
#                 time.sleep(5)
#     try:
#         with open('data/kospi200/'+filename) as f:
#             name_list= []
#             num_list = []
#             result = f.readlines()
#             for i in result:
#                 i = i.split(',')
#                 name_list.append(i[0])
#                 num_list.append(i[1].strip())
#
#     except:
#         list = glob.glob('data/kospi200/*')
#         latest = max(list, key= os.path.getctime)
#         with open(latest) as f:
#             name_list= []
#             num_list = []
#             result = f.readlines()
#             for i in result:
#                 i = i.split(',')
#                 name_list.append(i[0])
#                 num_list.append(i[1].strip())
#     return ({'name_list':name_list, 'num_list':num_list})

# if __name__=="__main__":
    # print(kospi200()["name_list"])