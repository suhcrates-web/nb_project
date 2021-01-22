import requests
from datetime import date, timedelta
import time, re
from bs4 import BeautifulSoup
import os, glob, json
today = date.today().strftime('%Y%m%d')
w1_ago =  (date.today() - timedelta(days=7)).strftime('%Y%m%d')
url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

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
print(dicts)