import telegram

def bot(type='p', message = 'None'):

    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')#노트북 5232, 데스크탑 5231
    port = port[0]
    if str(port) == '5232':
        cmd = 'p'
    elif str(port) == '5231':
        cmd = 'o'

    if type =='c':
        type = cmd #일괄조정 가능
    botter = telegram.Bot('1334671210:AAG9Cfvt8PYb0meZxgH7KKWzNHcVtqTKzts')
    def bot_open(message):
        botter.send_message('@news1_test_bot_channel', message)
    def bot_private(message):
        botter.send_message('@news1_private_test',message)
    if type=='o':

        bot_open(message)
    if type=='p':
        bot_private(message)
    if type=='op':
        bot_open(message)
        bot_private(message)



