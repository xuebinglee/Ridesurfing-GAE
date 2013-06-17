from Handler import Handler
import unittest


class HandlerTests(unittest.TestCase):
    """basic tests for Handler"""

    def test_BasicHandlerTest(self):
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
        Handler(xml_data)

if __name__ == '__main__':
    unittest.main()
