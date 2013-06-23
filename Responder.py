# -*- coding: utf-8 -*-
import sae
import sae.const
import MySQLdb
import re


def reply(userID, myID, createTime, content):
    return """
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
""" % (userID, myID, createTime, content)


def findACompany(userID, X, Y, destination):
    print str(X)+' '+str(Y)+' '+destination
    try:
        db = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                             user=sae.const.MYSQL_USER,
                             passwd=sae.const.MYSQL_PASS,
                             db=sae.const.MYSQL_DB,
                             port=int(sae.const.MYSQL_PORT)
                             )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    cur = db.cursor()
    print 'fetching all qualified users'
    cur.execute("""SELECT *
                   FROM ConnectedUsers
                   WHERE Destination=%s
                   AND UserID<>%s
                   AND LocationX IS NOT NULL
                   AND LocationY IS NOT NULL
                """, (destination, userID))
    rows = cur.fetchall()
    print 'all qualified users fetched'
    companies = ''
    for row in rows:
        currUserX = float(row[2])
        currUserY = float(row[3])
        if abs(X-currUserX) < 1 and abs(Y-currUserY) < 1:
            print 'Match found! '+row[1]+' X = '+str(currUserX)+' Y = '+str(currUserY)
            companies += ' '
            companies += row[1]
    return companies


def WechatIDMsgResponder(userID, myID, createTime, content):
    m = re.search(r'[Ww]echat[Ii][Dd] i?s? ?([a-zA-Z0-9_]+)\.?', content)
    wechatID = m.group(1)
    try:
        db = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                             user=sae.const.MYSQL_USER,
                             passwd=sae.const.MYSQL_PASS,
                             db=sae.const.MYSQL_DB,
                             port=int(sae.const.MYSQL_PORT)
                             )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    cur = db.cursor()
    cur.execute("""
                INSERT INTO ConnectedUsers
                    (UserID, WechatID)
                VALUES
                    (%s, %s)
                ON DUPLICATE KEY UPDATE

                    WechatID = VALUES(wechatID);
                """, (userID, wechatID))
    db.commit()
    return reply(userID, myID, createTime, 'G\'day '+wechatID+'! How may I help you?')


def TextMsgResponder(userID, myID, createTime, destination):
    try:
        db = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                             user=sae.const.MYSQL_USER,
                             passwd=sae.const.MYSQL_PASS,
                             db=sae.const.MYSQL_DB,
                             port=int(sae.const.MYSQL_PORT)
                             )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    cur = db.cursor()
    cur.execute("""
                INSERT INTO ConnectedUsers
                    (UserID, Destination)
                VALUES
                    (%s, %s)
                ON DUPLICATE KEY UPDATE

                    Destination = VALUES(Destination);
                """, (userID, destination))
    db.commit()
    print "destination inserted or updated"
    cur.execute("""SELECT *
                   FROM ConnectedUsers
                   WHERE UserID=%s""", (userID))
    row = cur.fetchone()
    # if no WebchatID
    if row[1] is None:
        print 'No WechatID.'
        return reply(userID, myID, createTime, "I still don't know your WechatID yet :)")
    elif row[2] is None or row[3] is None:
        print 'No geo info.'
        return reply(userID, myID, createTime, destination+"? Got it! Where are you now?")
    else:
        print 'find the user a company'
        companies = findACompany(userID, float(row[2]), float(row[3]), destination)
        print 'companies = ' + companies
        if companies == '':
            return reply(userID,
                         myID,
                         createTime,
                         "Sorry we cannot find you a company at the moment.\
                         Try again later?")
        else:
            return reply(userID,
                         myID,
                         createTime,
                         'Hooray! We found the following users for you! Happy chatting!\n'+companies)


def GeoMsgResponder(userID, myID, createTime, X, Y):
    print 'Trying to open DB'
    try:
        db = MySQLdb.connect(host=sae.const.MYSQL_HOST,
                             user=sae.const.MYSQL_USER,
                             passwd=sae.const.MYSQL_PASS,
                             db=sae.const.MYSQL_DB,
                             port=int(sae.const.MYSQL_PORT)
                             )
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
    print 'DB opened. Trying to assign cur.'
    cur = db.cursor()
    print 'Trying to insert or update location'
    cur.execute("""
                INSERT INTO ConnectedUsers
                    (UserID, LocationX, LocationY)
                VALUES
                    (%s, %s, %s)
                ON DUPLICATE KEY UPDATE

                    LocationX = VALUES(LocationX),
                    LocationY = VALUES(LocationY);
                """, (userID, X, Y))
    db.commit()
    print 'location inserted or updated'
    cur.execute("""SELECT *
                   FROM ConnectedUsers
                   WHERE UserID=%s""", (userID))
    row = cur.fetchone()
    # if no WebchatID
    if row[1] is None:
        print 'No WechatID.'
        return reply(userID, myID, createTime, "Now I know where you are. Could you please tell me your WechatID as well? :)")
    elif row[4] is None:
        print 'No destination.'
        return reply(userID, myID, createTime, "Okay, where do you wanna go?")
    else:
        print 'find the user a company'
        companies = findACompany(userID, float(X), float(Y), row[4])
        if companies == '':
            return reply(userID,
                         myID,
                         createTime,
                         "Sorry we cannot find you a company at the moment.\
                         Try again later?")
        else:
            return reply(userID,
                         myID,
                         createTime,
                         'Hooray! We found the following users for you! Happy chatting!\n'+companies)
