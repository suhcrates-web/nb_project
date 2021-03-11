import re
a = "dd(ddd)"

print(bool(re.search(r'^\(.*\)$',a)))

if bool(re.search(r'^\(.*\)$',a)):
    a = re.sub('[\(\)]','',a)
    print(a)


