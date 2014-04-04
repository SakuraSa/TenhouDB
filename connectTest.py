import requests
import re

ref_regex = re.compile(r"(\d{10}gm-\w{4}-\d{4,5}-\w{8})")

def downloadLog(url):
    ref = ref_regex.findall(url)
    if not ref:
        raise Exception("Unexpected URL: %s" % url)
    reqUrl = r"http://tenhou.net/5/mjlog2json.cgi?" + ref[0]
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Pragma": "no-cache", 
        "Cache-Control": "no-cache", 
        "If-Modified-Since": "Thu, 01 Jun 1970 00:00:00 GMT", 
        "Host": "tenhou.net", 
        "Referer": reqUrl, 
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36", 
    }
    req = requests.get(reqUrl, headers = headers)

    for key in headers:
        print key, ":", headers[key]

    if req.status_code != 200:
        raise Exception("Can not connect with %s" % url)
    if req.text.strip() == "INVALID PATH":
        raise Exception("Return Unexpected text: %s" % req.text.strip())
    obj = req.json()
    if len(obj["name"]) != 4:
        raise Exception("Not 4 Player Game, skipped.")
    return obj, req.text

try:
    downloadLog(r"http://tenhou.net/5/?log=2014030816gm-0009-6140-c1785499&tw=0&js=1")
    print "ok!"
except Exception, e:
    print e