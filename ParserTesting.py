from Parser import TextMsgParser
from Parser import GeoMsgParser
import unittest


class ParserTests(unittest.TestCase):
    """basic tests for textMsgParser and geoMsgParser"""

    def test_BasicTextMsgTest(self):
        xml_data = '''
        <xml>
        <ToUserName>Ridesurfing</ToUserName>
        <FromUserName><![CDATA[Lee]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content>I want to go to Xin Jie Kou</Content>
        <MsgId>1234567890123456</MsgId>
        </xml>
        '''
        self.assertEquals(TextMsgParser(xml_data), ('Lee', 'XJK'))

    def test_BasicGeoMsgTest(self):
        xml_data = '''
        <xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[Hu]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[blah blah]]></Label>
        <MsgId>1234567890123456</MsgId>
        </xml>
        '''
        self.assertEquals(GeoMsgParser(xml_data), ('Hu', 23.134521, 113.358803))

if __name__ == '__main__':
    unittest.main()
