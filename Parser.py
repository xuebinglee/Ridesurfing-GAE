import re


def TextMsgParser(raw_xml):
    # userName
    m = re.search(r'<FromUserName><!\[CDATA\[(\w*)\]\]></FromUserName>', raw_xml)
    userName = m.group(1)
    # content
    m = re.search(r'<Content>([a-zA-Z0-9_ ]*)</Content>', raw_xml)
    content = m.group(1)

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
    # userName
    m = re.search(r'<FromUserName><!\[CDATA\[(\w*)\]\]></FromUserName>', raw_xml)
    userName = m.group(1)
    # X
    m = re.search(r'<Location_X>((\d)+\.?(\d)*)</Location_X>', raw_xml)
    X = float(m.group(1))
    # Y
    m = re.search(r'<Location_Y>((\d)+\.?(\d)*)</Location_Y>', raw_xml)
    Y = float(m.group(1))

    return (userName, X, Y)
