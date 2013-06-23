# -*- coding: utf-8 -*-
import sae
import sae.const
import MySQLdb
from bottle import *
from Handler import Handler

ridesurfing = Bottle()


@ridesurfing.route('/insert')
def Insert():
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

    UserID = "this is another UserID"
    WechatID = "another haha"
    #LocationX = 3.14
    #LocationY = 3.14
    Destination = 'MGG'

    cur.execute("""
                INSERT INTO ConnectedUsers
                    (UserID, WechatID, Destination)
                VALUES
                    (%s, %s, %s)
                ON DUPLICATE KEY UPDATE

                    WechatID = VALUES(WechatID),
                    Destination = VALUES(Destination);
                """, (UserID, WechatID, Destination))
    db.commit()


@ridesurfing.route('/clear')
def ClearDB():
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
    cur.execute('DELETE FROM ConnectedUsers')
    db.commit()
    return 'Cleared'


@ridesurfing.route('/DB')
def PrintDB():
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
    cur.execute('SELECT * FROM ConnectedUsers')
    rows = cur.fetchall()
    for row in rows:
        for i in range(6):
            if row[i] is not None:
                print row[i]
            else:
                print 'NULL'
    return 'Sent to log'


@ridesurfing.route('/')
def MainPage():
    echostr = request.GET.get('echostr')
    return echostr


@ridesurfing.route('/', method='POST')
def MsgHandler():
    post_request = request.body.read()
    print post_request
    return Handler(post_request)

application = sae.create_wsgi_app(ridesurfing)
