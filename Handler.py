# -*- coding: utf-8 -*-
import re
import xml.etree.ElementTree as ET
from ParserXML import TextMsgParser
from ParserXML import GeoMsgParser
from Responder import reply
from Responder import WechatIDMsgResponder
from Responder import TextMsgResponder
from Responder import GeoMsgResponder


def Handler(raw_xml):
    XMLroot = ET.fromstring(raw_xml)
    userID = XMLroot.find('FromUserName').text
    myID = XMLroot.find('ToUserName').text
    createTime = XMLroot.find('CreateTime').text
    msgType = XMLroot.find('MsgType').text

    if msgType == 'text':
        print 'text'
        content = XMLroot.find('Content').text
        namePattern = re.compile("[Ww]echat[Ii][Dd]")
        if namePattern.search(content):
            print 'wechatID'
            return WechatIDMsgResponder(userID, myID, createTime, content)
        else:
            print 'destination'
            destination = TextMsgParser(raw_xml)
            if destination is None:
                return reply(userID, myID, createTime, "Destination not found or not supported.")
            return TextMsgResponder(userID, myID, createTime, destination)
    elif msgType == 'location':
        print 'location'
        (X, Y) = GeoMsgParser(raw_xml)
        print 'location parsed X='+X+' Y='+Y
        return GeoMsgResponder(userID, myID, createTime, X, Y)
    elif msgType == 'event':
        event = XMLroot.find('Event').text
        if event == 'subscribe':
            userID = XMLroot.find('FromUserName').text
            myID = XMLroot.find('ToUserName').text
            createTime = XMLroot.find('CreateTime').text
            return reply(userID, myID, createTime, "Welcome! Please tell me your WechatID :)")
    else:

        return reply(userID, myID, createTime, "MESSAGE TYPE NOT RECOGNIZED.")
