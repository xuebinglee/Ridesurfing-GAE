# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re


def TextMsgParser(raw_xml):
    XMLroot = ET.fromstring(raw_xml)
    content = XMLroot.find('Content').text.encode('utf-8')

    # RE patterns for supported destinations
    XJKPattern = re.compile("Xin Jie Kou")
    AirportPattern = re.compile("(Nanjing )?(LuKou )?Airport")
    SouthPattern = re.compile("Nanjing South (Railway )?Station")
    MGGPattern = re.compile("(NUAA )?Ming Gu Gong (Campus)?")
    JNPattern = re.compile("(NUAA )?Jiang Ning (Campus)?")

    if XJKPattern.search(content):
        destination = "Xin Jie Kou"
    elif AirportPattern.search(content):
        destination = "Nanjing Airport"
    elif SouthPattern.search(content):
        destination = "Nanjing South Railway Station"
    elif MGGPattern.search(content):
        destination = "Ming Gu Gong Campus"
    elif JNPattern.search(content):
        destination = "Jiang Ning Campus"
    else:
        destination = None

    return destination


def GeoMsgParser(raw_xml):
    XMLroot = ET.fromstring(raw_xml)
    X = XMLroot.find('Location_X').text
    Y = XMLroot.find('Location_Y').text

    return (X, Y)
