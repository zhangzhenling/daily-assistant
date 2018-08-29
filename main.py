# -*- coding:utf-8 -*-

from flask import Flask,request
from time import time
import xml.etree.ElementTree as et
import muban

import hashlib

app = Flask(__name__)
app.debug = True

@app.route('/',methods=['GET','POST'])
def wechat():

    if request.method == 'GET':
        token = 'xiaoqingxin'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')

        list = [token, timestamp, nonce]
        list.sort()

        s = list[0] + list[1] + list[2]

        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()

        if hascode == signature:
            return echostr
        else:
            return ""

    if request.method == 'POST':

        str_xml = request.stream.read()
        xml = et.fromstring(str_xml)
        msgType = xml.find("MsgType").text
        xml_muban = muban.reply_muban(msgType)
        if msgType == "text":
            content = xml.find("Content").text
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            return xml_muban % (fromUser, toUser, int(time()), content)
        elif msgType == "image":
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            mediaid = xml.find("MediaId").text
            print(xml_muban % (fromUser, toUser, int(time()), mediaid))
            return xml_muban % (fromUser, toUser, int(time()), mediaid)
        else:
            itemDic = [{'Title':'Title','Description':'Description',
                    'PicUrl':'https://ss0.baidu.com/73x1bjeh1BF3odCf/it/u=3705265267,3767781981&fm=85&s=DE0A5C2A7D264E1B62FD99CB0300C0B1',
                    'Url':'www.baidu.com'},{'Title':'Title1','Description':'Description1',
                    'PicUrl':'https://ss0.baidu.com/73x1bjeh1BF3odCf/it/u=3705265267,3767781981&fm=85&s=DE0A5C2A7D264E1B62FD99CB0300C0B1',
                    'Url':'www.baidu.com'}]
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            mediaid = xml.find("MediaId").text
            return muban.image_text_new_muban(itemDic) % (fromUser, toUser, int(time()))




if __name__ == '__main__':
    app.run(port="80")