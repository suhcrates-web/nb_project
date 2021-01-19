import re


def dadum_sentences(answer_0):
    #나눠지지 않은 통문장이 들어옴
    ##2021.09.09 을 2021년9월9일 로 변환
    date_in_text = re.findall(r'\d{4}\.\s?\d{2}\.\s?\d{2}\.?' , answer_0)
    subs = []
    for i in date_in_text:
        Y =re.findall(r'\d+(?=\.)',i)[0]
        i = i[i.index(Y)+len(Y):]
        m = re.findall(r'\d+(?=\.)',i)[0]
        i = i[i.index(m)+len(m):]
        d = re.findall(r'\d+',i)[0]
        sub = f'{str(int(Y))}년{str(int(m))}월{str(int(d))}일'
        subs.append(sub)
    answer= re.sub(r'\d{4}\.\s?\d{2}\.\s?\d{2}\.?', '{}', answer_0)
    answer = answer.format(*subs)

    ## . 을 기준으로 문장들을 나눠 리스트화. **다만  3.39% 처럼  . 뒤에 숫자가 있는 경우는 건너뜀.
    def split_sentence(a):
        sentences = []
        end = False
        while end == False:
            sentence = ''
            j = 0
            for i in a:
                if i not in ['.']:
                    sentence += i
                    j +=1
                elif bool(re.search(r'\.\d',a[j:j+2])) :
                    sentence += i
                    j +=1
                else:
                    sentences.append(sentence)
                    j += 1
                    a = a[j:]
                    break

            if len(a) ==j :
                end = True
        return sentences

    answers = split_sentence(answer)

    return answers


#####조회공시에 대한 답변###. '당사는 ~~~검토중에 있으나 확정된 사항이 없다" 문장 만들어줌
#fr(raw 버전)의 '답변내용' 부분을 넣어주면 'sentence'를 뱉음. 반드시 '검토' '확정' '없' '당사는' 이 포함돼야하며, 그 문장만 뱉어냄.

def make_sentence(answers):

    n=0
    for i in answers:
        sure = ['검토','없', '확정']
        sure_bool = True
        for j in sure:
            if not re.search(j, i):
                sure_bool = False  #한개라도 일치하는 게 없으면 False.
                break
        if not bool(re.search('당사가|당사는',i)): #당사가, 당사는 둘다 없으면 역시 False
            sure_bool = False
        if sure_bool ==True: #sure과 모두 일치하면
            break  #멈추고 n을 내놓음

        n+=1         #아니면 n을 하나 더한 뒤 루프를 계속 진행

    if n == len(answers):
        raise Exception("맞는 문장이 없음")

    sentence= answers[n]
    try:
        sentence= sentence[sentence.index('당사는'):]
    except:
        sentence= sentence[sentence.index('당사가'):]

    sentence = sentence[:sentence.index('없')+1]+'다'

    return sentence