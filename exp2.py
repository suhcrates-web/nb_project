import requests
from datetime import date
import time, re
from bs4 import BeautifulSoup
import os, glob, json


def kos_list():
    tomonth = date.today().strftime('%Y%m')
    today = date.today().strftime('%Y%m%d')
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    result_dict = {}
    result_dict['all_name'] = []
    result_dict['all_num'] = []
    #이 펑션이 두번 반복됨. 파일 검색, 없으면 만들고 있으면 가져와 result_dict를 채움.
    def make_and_get(kowhat):
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
                result = requests.post(url, q_data)
                dicts = json.loads(result.content.decode(encoding='utf-8'))
                dicts = dicts['output']
                for i in dicts:
                    try:
                        f.writelines([i['ISU_ABBRV'],',',i['ISU_SRT_CD'], '\n'])
                    except:
                        pass
                time.sleep(3)
        try:
            with open(f'data_share/{kowhat}/'+ filename) as f:
                name_list= []
                num_list = []
                result = f.readlines()
                for i in result:
                    i = i.split(',')
                    name_list.append(i[0])
                    num_list.append(i[1].strip())
                    result_dict['all_name'].append(i[0])
                    result_dict['all_num'].append(i[1].strip())

        except:
            list = glob.glob(f'data_share/{kowhat}/*')
            latest = max(list, key= os.path.getctime)
            with open(latest) as f:
                name_list= []
                num_list = []
                result = f.readlines()
                for i in result:
                    i = i.split(',')
                    name_list.append(i[0])
                    num_list.append(i[1].strip())
                    result_dict['all_name'].append(i[0])
                    result_dict['all_num'].append(i[1].strip())

        result_dict[f'{kowhat}_name'] = name_list
        result_dict[f'{kowhat}_num'] = num_list
        return None

    make_and_get('kospi')
    make_and_get('kosdaq')
    return result_dict

print(kos_list())

