import xml.etree.ElementTree as ET
import re


def TextMsgParser(raw_xml):
    XMLroot = ET.fromstring(raw_xml)
    userName = XMLroot.find('FromUserName').text
    content = XMLroot.find('Content').text

    # RE patterns for supported destinations
    XJKPattern = re.compile("Xin Jie Kou")
    AirportPattern = re.compile("(Nanjing )?(LuKou )?Airport")
    SouthPattern = re.compile("Nanjing South (Railway )?Station")
    MGGPattern = re.compile("(NUAA )?Ming Gu Gong (Campus)?")
    JNPattern = re.compile("(NUAA )?Jiang Ning (Campus)?")

    if XJKPattern.search(content):
        destination = "XJK"
    elif AirportPattern.search(content):
        destination = "Airport"
    elif SouthPattern.search(content):
        destination = "South"
    elif MGGPattern.search(content):
        destination = "MGG"
    elif JNPattern.search(content):
        destination = "JN"
    else:
        raise Exception("Destination not found or not supported.")

    return (userName, destination)


def GeoMsgParser(raw_xml):
    XMLroot = ET.fromstring(raw_xml)
    userName = XMLroot.find('FromUserName').text
    X = float(XMLroot.find('Location_X').text)
    Y = float(XMLroot.find('Location_Y').text)

    return (userName, X, Y)
