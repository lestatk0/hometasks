import re
import collections

file = open('./access_log', 'r')
ip_addr = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', file.read())
for i in collections.Counter(ip_addr).most_common(10):
    print('IP %s, counter %d' % (i[0], i[1]))