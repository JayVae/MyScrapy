# -*- coding: utf-8 -*-
import re
import urllib

import Method

for i in range(1,1000):
    request = urllib.request.Request('http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx')
    reponse = urllib.request.urlopen(request)
    # try:
    #     reponse = urllib.request.urlopen(request)
    # except urllib.error.HTTPError as e:
    #     print(e.code)
    #     print(e.reason)
    resu = reponse.read()
    resu = resu.decode('utf-8')
    VIEWSTATE = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*)" />', resu, re.I)
    EVENTVALIDATION = re.findall(
        r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*)" />', resu, re.I)
    print(i)

