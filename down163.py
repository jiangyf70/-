import os
import re
import json
import requests
from Crypto.Cipher import AES
from hm3u8dl_cli import m3u8download

MSGSPATH = "./msgs/"  # 信息存储文件，注意末尾的'/'不能少
MSGFILES = []



# 加载信息文件
for each in os.listdir(MSGSPATH):
    MSGFILES.append(each)

for each in MSGFILES:
    videoName = each.rsplit('.', 1)[0] + '.mp4'
    msg = json.loads(open(MSGSPATH + each, 'r').read())
    m3u8url = msg['url']
    key = msg['key']
    m3u8download(m3u8url, title=videoName, key=key)