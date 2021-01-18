#반올림

import math
# a = 37389534
a='-259627'
b = '원'


# danwi : 원본의 단위  /  gijun : 출력 의 단위
def banolim(num, danwi='원', gijun ='일', buho='buho'):  #buho  'abs' 절대값으로, 'buho' 부호 포함
    num = float(num)

    if num >=0:
        plma = ''
    else:
        plma = '-'
    num = abs(num)
    org_num = num  #뒤에서  결과 없을 경우 기준을 '일'로 조정해 다시 돌리기 위해 org_num으로 원본을 저장.

    if danwi == '원':
        danwi = '일'
    dan = {
        '일':1,
        '백':100,
        '천':1000,
        '만':10000,
        '십만':100000,
        '백만':1000000,
        '천만':10000000,
        '억':100000000,
        '일억':100000000,
        '십억':1000000000,
        '백억':10000000000,
        '천억':100000000000,
        '조':1000000000000,
    }

    gi = {
        '일':'일',
        '십':'일',
        '백':'일',
        '천':'일',
        '만':'만',
        '십만':'만',
        '백만':'만',
        '천만':'만',
        '억':'억',
        '십억':'억',
        '천억':'억'
    }
    gijun = gi[gijun]

    num = num * dan[danwi]

    num_12, num_8, num_4 = 0, 0, 0

    if num % 1 == 0:
        num = int(num)

        # if danwi in ['원', '주']:

        if gijun == '만':
            num_4 = round(num/10000)
            num = 0
        else:
            num_4 = math.floor(num/10000)
            num = num - num_4*10000

        if num_4 != 0:
            if gijun == '억':
                num_8 = round(num_4/10000)
                num_4, num = 0, 0
            else:
                num_8 = math.floor(num_4/10000)
                num_4 = num_4 - num_8 *10000

            if num_8 != 0:
                if gijun == '조':
                    num_12 = round(num_8/10000)
                    num_8, num4, num = 0, 0, 0
                else:
                    num_12 = math.floor(num_8/10000)
                    num_8 = num_8 - num_12 * 10000
    temp = [num_12, num_8, num_4, num]
    temp_1 = ['조', '억', '만', '']
    result = ''
    for i in range(0,4):
        if temp[i] != 0 :
            result = result + str(temp[i]) + temp_1[i]

    if result == '':  #빈값이 나오면 자동으로 기준을 '일'로 수정하도록.
        result = banolim(num= org_num, danwi = danwi, gijun='일')

    if buho == 'abs':
        return result
    if buho == 'buho':
        return plma+result

if __name__ == "__main__" :
    print(banolim(a,b, '일'))
