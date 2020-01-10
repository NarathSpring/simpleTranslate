# /usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import urllib.request
import random
import hashlib
import json


def salt(n):
    s = ""
    for i in range(n):
        s = str(random.randint(0, 9)) + s
    return s


def sign(option):
    st = option["appid"] + option["q"] + option["salt"] + option["secret"]
    m = hashlib.md5()
    m.update(st.encode("utf-8"))
    return m.hexdigest()


def is_Chinese(word):
    for ch in word:
        if "\u4e00" <= ch <= "\u9fff":
            return True
    return False


option = {}


def init(option):
    query = input("请输入想要翻译的单词：")
    option["q"] = query

    if is_Chinese(query):
        # 中译英
        option["from"] = "zh"
        option["to"] = "en"
    else:
        # 英译中
        option["from"] = "en"
        option["to"] = "zh"

    option["appid"] = "20200108000373922"
    option["salt"] = salt(10)
    option["secret"] = "VORJXge7vEjmh1S_cS_W"
    option["sign"] = sign(option)


init(option)

if is_Chinese(option["q"]):
    option["q"] = urllib.parse.quote(option["q"])

requestUrl = (
    "http://api.fanyi.baidu.com/api/trans/vip/translate?q="
    + option["q"]
    + "&from="
    + option["from"]
    + "&to="
    + option["to"]
    + "&appid="
    + option["appid"]
    + "&salt="
    + option["salt"]
    + "&sign="
    + option["sign"]
)

response = urllib.request.urlopen(requestUrl)
html = response.read().decode("utf-8")

j = json.loads(html)["trans_result"]

print(j[0]["dst"])

