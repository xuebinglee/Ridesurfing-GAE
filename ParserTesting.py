from Parser import TextMsgParser
from Parser import GeoMsgParser
import unittest


class ParserTests(unittest.TestCase):
    """basic tests for textMsgParser and geoMsgParser"""
    def setUp(self):
        # do something
        pass

    def test_BasicTextMsgTest(self):
        xml_data = '''
        <xml>
        <ToUserName>Ridesurfing</ToUserName>
        <FromUserName><![CDATA[Lee]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType>text</MsgType>
        <Content>I want to go to Xin Jie Kou</Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
        '''
        print TextMsgParser(xml_data)

    def test_BasicGeoMsgTest(self):
        xml_data = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[Yu]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[blah blah]]></Label>
        <MsgId>1234567890123456</MsgId>
        </xml>
        '''
        print GeoMsgParser(xml_data)

if __name__ == '__main__':
    unittest.main()
