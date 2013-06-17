import re
from Parser import TextMsgParser
from Parser import GeoMsgParser


def Handler(raw_xml):
    m = re.search(r"<MsgType><!\[CDATA\[(\w+)\]\]></MsgType>", raw_xml)
    msgType = m.group(1)
    if msgType == 'text':
        print 'text'
        TextMsgParser(raw_xml)
        # TextMsgResponder
    elif msgType == 'location':
        print 'location'
        GeoMsgParser(raw_xml)
        # GeoMsgResponder
    else:
        # NEED TO COME BACK LATER!!!
        raise Exception("MESSAGE TYPE NOT RECOGNIZED.")
