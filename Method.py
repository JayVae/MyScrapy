import urllib.request
import re

class method:
    def get_hiddenvalue(url):
        request = urllib.request.Request(url)
        reponse= urllib.request.urlopen(request)
        # try:
        #     reponse = urllib.request.urlopen(request)
        # except urllib.error.HTTPError as e:
        #     print(e.code)
        #     print(e.reason)
        resu = reponse.read()
        resu =resu.decode('utf-8')
        VIEWSTATE = re.findall(r'<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.*)" />', resu,re.I)
        EVENTVALIDATION = re.findall(r'<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="(.*)" />', resu,re.I)
        print(VIEWSTATE)
        print(EVENTVALIDATION)
        return VIEWSTATE[0], EVENTVALIDATION[0]


