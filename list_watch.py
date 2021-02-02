#목록 받아보기.
import requests, xmltodict, json, pandas, datetime

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)
today = datetime.datetime.today().strftime(format='%Y%m%d')
yesterday = datetime.datetime.today()- datetime.timedelta(days=2)
yesterday = yesterday.strftime(format='%Y%m%d')
def list_watch(i):
    url = 'https://opendart.fss.or.kr/api/list.json'
    data = {  #없는건 ''로 남겨두지 말고 그냥 블라인드 해버리셈
        'crtfc_key' : '5d33a523ba2d678b84673a4a54f9b7efe5abf9c0',  #인증키
        # 'corp_code' : '',  #고유번호
        'bgn_de' : today, #시작일
        'end_de' : today, #종료일
        # 'last_reprt_at' : '',  #최종보고서 검색여부
        # 'pblntf_ty' : '', #공시유형
        # 'pblntf_detail_ty' : '', #공시상세유형
        # 'corp_cls' : 'K', #법인구분  Y(유가), K(코스닥), N(코넥스), E(기타)
        # 'sort' : '', #정렬
        # 'sort_mth': '', #정렬방법
        'page_no' : i, #페이지번호
        'page_count': '100', #페이지별 건수
    }
    content = requests.get(url, data).content
    content = json.loads(content)

    # content = content.decode('utf-8')
    # content = content['list'][0]
    try:
        pan = pandas.DataFrame(content['list'])   #pandas.read_json 하지 말고 그냥 DataFrame으로 읽으면 됨.
        return pan
    except:
        raise Exception(content['message'])

#timeline으로 감

if __name__ == "__main__":
    print(list_watch(1))


# pan.to_excel('list.xlsx', encoding='utf-8')

#월요일 오전 10시반쯤? 한번 이전 데이터들이 잘리는듯.
#페이지 카운트 100에 남은 데이터가 50이라고 할때, 페이지넘버가 2로 가면 1페이지 리스트가 다시 나열됨.