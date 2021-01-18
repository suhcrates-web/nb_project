###집배신에 올리기 ####
import requests
from datetime import datetime

# url = 'http://alpha.news1.kr/view/report/article/article_reg_popup.php?id=4140779&tp=edit&code=03' # 팝업링크 예시

#수정 완료 누르면 'article_save_ok(91)' 이 작동됨
#article_save_ok(state)는 91을 11로 바꾸고 myform을 제출함


#op : new_article ; 새로 만들기 ,  edit_article ; 기존 기사 수정

def do_temp(op=None, title = '제목없음', article = '내용없음', info = '내용없음'):
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
        port = port[1]  # http://172.30.1.53:5232/bot_v3/

    today = datetime.today().strftime("%Y-%m-%d")
    url= port + str(today) +'/'
    data = {
        'title':title,
        'article':article,
        'info': info
    }
    requests.post(
        url,
        data = data,)


def do(op='edit_article', title = '제목없음', article = '내용없음'):
    #세션열기
    session_requests = requests.session()
    #로그인정보
    payload = {
        'cmd' : 'member',
        'op' : 'alpha_login',
        'uid' : 'suhcrates' ,
        'pwd' : 'sbtmdnjs1'
    }
    #로그인, 기사 보내는 ajax url.
    login_url ='http://alpha.news1.kr/ajax/ajax.php'

    if op=='new_article':
        data = {
            'cmd' : 'article',
            'op' : 'new_article',
            'autosave': '',
            'articles_num' : '',
            'article_status' : '9',
            'article_org_status': '0',
            'regist_status': '' ,
            'result_category_selected' : '83',
            'result_byline_selected':'1128',
            'result_keyword_selected': '',
            'result_keyword_str': '',
            'result_article_relation_value':'9' ,
            'article_foreign_photo_id_arr':'',
            'article_photo_id_arr':'',
            'article_movie_id_arr':'',
            'result_hotissue_selected':'',
            'user_job_title' : '5',
            'article_title' : title,
            'subSubjectChk' : '1',
            'subSubject[]' : '(테스트)',
            'article_byline_area' : '(세종=뉴스1)',
            'article_byline_selected' : '1128',
            'contentArea' : article,
            'article_editor_email' : 'suhcrates@news1.kr',
            'article_embargo_hour' : '',
            'article_embargo_min' : '',
            'department_id':'5',
            'source_id' : '10',
            'article_category_id' : '83',
            'article_category_selected' : '83',
            'article_kindof' : '1',
            'article_cotent_type[]' : '7',
            'keyword':'',
            'www_only' : '0',
            'exclude_images' : '0',
            'article_bundle_id' : '24',
            'article_bundle_selected' : '24',
            'is_edit_title':'1',
            'bundle_edited_title':'',
            'breaking' : '2',
            'article_relation_value' :'1',
            'id': '4139089',
            'code' : '1000',
            'mode' : '',
            'user_id' :'1128',
            'msg': 'OK',
            'status' : '1',

        }
    elif op=='edit_article':
        data = {
            'cmd' : 'article',
            'op' : 'edit_article',
            'autosave': '', #이거 넣으면 작동 안함. 그냥 공란으로 비워두길.
            'articles_num' : '4140779',
            'article_status' : '91',  #1  #수정완료 버튼을 누르면 91에서 11로 바꾸도록 함
            # 근데 11을 넣으면 '예약요청'이 되고 91을 넣으면 '수정완료'가 됨
            'article_org_status': '91', # 수정버튼 누르면 91 -> 11 하도록 함. 근데 막상 열어서 보면 1임
            'regist_status': '11' , #공란
            'result_category_selected' : '83',
            'result_byline_selected':'1128',
            'result_keyword_selected': '',
            'result_keyword_str': '',
            'result_article_relation_value':'' ,
            'article_foreign_photo_id_arr':'',
            'article_photo_id_arr':'',
            'article_movie_id_arr':'',
            'result_hotissue_selected':'',
            'user_job_title' : '5',
            'article_title' : title,
            'subSubjectChk' : '1',
            'subSubject[]' : '(테스트)',
            'article_byline_area' : '(세종=뉴스1)',
            'article_byline_selected' : '1128',
            'contentArea' : article,
            'article_editor_email' : 'suhcrates@news1.kr',
            'article_embargo_hour' : '',
            'article_embargo_min' : '',
            'department_id':'5',
            'source_id' : '10',
            'article_category_id' : '83',  #카테고리 설정. 5번은 '청와대' . 산업일반 83
            'article_category_selected' : '83',
            'article_kindof' : '1',
            'article_cotent_type[]' : '7',#article_cotent_type[] / content가 아니라 cotent임 / 7번이 발생
            'keyword':'',
            'www_only' : '0',
            'exclude_images' : '0',
            'article_bundle_id' : '24',
            'article_bundle_selected' : '24',
            'is_edit_title':'1',
            'bundle_edited_title':'',
            'breaking' : '2',
            'article_relation_value' :'1',
            'id': '4140779',
            'code' : '03',
            'tp' : 'edit',
            'mode' : '',
            'user_id' :'1128',
            'msg': 'OK',
            'status' : '1',
        }

    # data0['contentArea'] = content_n1
    session_requests.post(
        login_url,
        data = payload,
    )
    session_requests.post(
        login_url,
        data = data,)


if __name__ == "__main__":
    do()


