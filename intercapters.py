import re
import json
import threading
import mitmproxy
import base64
from Crypto.Cipher import AES


URL = ""  # m3u8文件地址/视频地址
VIDEONAME = ""  # 视频名称
FILE = ""  # m3u8文件
MSGSPATH = "./msgs/"  # 信息存储文件，注意末尾的'/'不能少
KEYSPATH = "./keys/"  # key存储文件，注意末尾的'/'不能少


def keyDownloader(url: object, text, key, name):
    """存放加密视频信息
    """
    global MSGSPATH, KEYSPATH
    ke =  key.decode('utf-8')

    msg = {
        'url': url,
        'key': ke
    }
    msgFile = MSGSPATH + name.rsplit('.', 1)[0] + '.txt'

    with open(msgFile, 'w', encoding='utf-8') as f:
        json.dump(msg, f)

    print(name, "已记录")





class NameIntercapter:
    """拦截视频名
    """

    def __init__(self) -> None:
        super()

    def response(self, flow: mitmproxy.http.HTTPFlow):
        global VIDEONAME
        global URL
        if re.match(r'^https://vod.study.163.com/eds/api/v1/vod/video\?videoId=(\d*?)&signature=(.*?)&clientType=1$', flow.request.url):
            VIDEONAME = json.loads(flow.response.text)['result']['name']
            videos = json.loads(flow.response.text)['result']['videos']

            # 遍历视频列表，查找 "quality" 为 3 的视频
            for video in videos:
                if video['quality'] == 3:
                    video_url = video['videoUrl']
                    break

            URL = video_url



class KeyIntercapter:
    """拦截解密key
    """

    def __init__(self) -> None:
        super()

    def response(self, flow: mitmproxy.http.HTTPFlow):
        global FILE, VIDEONAME, URL
        if re.match(r'^https://vod.study.163.com/eds/api/v1/vod/hls/key\?id=(\d*?)&token=(.*?)$', flow.request.url):
            if len(flow.response.content) == 16:

                encodeer = base64.b64encode(flow.response.content)

                #encodeer = flow.response.content
                threading.Thread(target=keyDownloader, args=(
                    URL, FILE, encodeer, VIDEONAME)).start()


# 加载拦截器
addons = [
    NameIntercapter(),
    KeyIntercapter()
]
