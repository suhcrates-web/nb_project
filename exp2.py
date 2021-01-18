import re

a= '검토한 적 없지만 확정했다'

print(not bool(re.search('당사가|당사는',a)))