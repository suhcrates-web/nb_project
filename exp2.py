#coding= utf8
import re
from toolBox import jongsung

a ='현대비앤지스틸(주), LG하우시스 (자동차소재·산업용필름설)사업부 인사수 검토 보도에 스대한 사조회공시 요구에 대한 조회공시 답변'

print(re.findall(r'(?<=\()[^\(\)]+설\s?(?=\))',a))

if bool(re.search(r'(?<=\()[^\(\)]+설\s?(?=\))',a)):
    print('fuck')
    reason = re.findall(r'(?<=\()[^\(\)]+설\s?(?=\))',a)[0]
else:
    for i in ['설','보도','관련']:
        if i in a:
            reason = i[:i.index(i)]
print(reason)





