import petl as etl
import sys
import pymysql.cursors
import xml2json
import optparse
import json
from dateutil.parser import parse
from pymongo import MongoClient
import os
import time

#mongo db functions
def get_collections(host,port,dbName,collName):
    client = MongoClient(host,port)
    db = client[dbName]
    return db[collName]

def get_colNames(coll):
    colNames = []
    di =  coll.find_one()
    del di[u'_id']
    for x in di:
        colNames.append(x)
    return tuple(colNames)


def get_table(coll,colNames):
    rows = []
    rows.append(colNames)
    for docs in coll.find({},{u'_id':0}):
        row = []
        for _,value in docs.iteritems():
            row.append(value)
        rows.append(list(row))
    return rows

#converting dictionary object to list
def d2l(tb):
    l = list()
    l.append(tb[1].keys())
    t = [x.values() for x in tb[1:]]
    l = l + t
    return l

#checking if a given string is date or not
def isdate(string):
    try:
        parse(string)
        return 1
    except ValueError:
        return 0

#checking if a given string is float or not
def isfloat(a):
    try:
        float(a)
        return 1
    except ValueError:
        return 0

#checking if a given string is int or not
def isint(a):
    try:
        int(a)
        return 1
    except ValueError:
        return 0

#Mapping the attributes with the datatypes
def dmap(attr,row):
    dtype = dict()
    for i in range(0,len(row)):
        if(isint(row[i])==1):
            dtype[attr[i]] = "INT(20)"
        elif(isfloat(row[i])==1):
            dtype[attr[i]] = "FLOAT(20)"
        else:
            dtype[attr[i]] = "VARCHAR(100)"
    return dtype
    """elif (isdate(row[i])==1):
            dtype[attr[i]] = "DATETIME" """

#Generates create table query. Arguments are attributes, datatype mapping dict and table object
def crtTable(attr,dtype,tb):
    q = "create table " + tb + "("
    for i in range(0,len(attr)-1):
        q = q + " " + attr[i] + " " + dtype[attr[i]] + ","
    q = q + " " + attr[len(attr)-1] + " " + dtype[attr[len(attr)-1]] + ");"
    return q




#returns insert query string. Arguments are the values to be inserted and attribute list.
def query_i(row,attr):
    q = "INSERT INTO " + tname + " ("
    for i in range(0,len(attr)-1):
        q = q + attr[i] + ", "
    q = q + attr[len(attr)-1] + ") values("
    for i in range(0,len(row)-1):
        q = q + " '" + str(row[i]) + "',"
    q = q + " '" + str(row[len(row)-1]) + "');"
    return q

#returns update query string. Arguments are the updates values, attribute list and "where" clause argument
def query_u(row,attr,pkey,search):
    q = "UPDATE " + tname + " SET "
    for i in range(0,len(attr)-1):
        q = q + attr[i] + "= '" + str(row[i]) + "',"
    q = q + attr[len(attr)-1] + "= '" + str(row[len(row)-1]) + "' where " + pkey +  "= '" + search + "';"
    return q



#loads the data into MySQL database. Arguments: Table Object
def load(tb,pkey,hst,usr,pwd,dtb,tname,rmFileName):
    db = pymysql.connect(host=hst,
                         user=usr,
                         password=pwd,
                         db=dtb,
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()

    if cur.execute("SHOW TABLES LIKE '" + tname + "';") == 0:
        cur.execute(crtTable(tb[0],dmap(tb[0],tb[1]),tname))
    print "No. of data to be processed: "+ str(len(tb))
    cur.execute('SET SQL_MODE=ANSI_QUOTES')
    etl.todb(tb,db,tname);
    db.commit()
    os.remove(rmFileName)


def getLines(filename):
    fo = open(filename,'r')
    fields = {}
    while True:
        line = fo.readline()
        line = line.replace('\n','')
        if line == '':
            fo.close()
            return fields
        a = line.split(':')
        fields[a[0]] = a[1]
    return fields

def extract(lines):
    tb = None
    if lines['FILE_TYPE']=='CSV':
        filename = lines['FILE_NAME']
        tb = etl.fromcsv(filename)

    elif lines['FILE_TYPE']=='XML':
        filename = lines['FILE_NAME']
        f = open(filename,'r').read()
        options = optparse.Values({"pretty": True})
        jsn = json.dumps(xml2json.xml2json(f,options))
        ob = json.loads(jsn.decode('string-escape').strip('"'))
        temp = dict()
        for key in ob.keys():
            for skey in ob[key].keys():
                temp = json.dumps(ob[key][skey])
        with open("temp.json","w") as tmp:
            tmp.write(temp)
        tb = etl.fromjson("temp.json")


    elif lines['FILE_TYPE']=='JSON':
        filename = lines['FILE_NAME']
        tb = etl.fromjson(filename)



    elif lines['FILE_TYPE']=='MYSQL':
        host = lines['hostname']
        user = lines['username']
        pwd = lines['password']
        dtb = lines['dbname']
        table = lines['tname']
        conn = pymysql.connect(host=host,
                               user=user,
                               password=pwd,
                               db=dtb,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        temp = etl.fromdb(conn, "SELECT * FROM " + table)
        tb = d2l(temp)

    elif lines['FILE_TYPE']=='MONGODB':
        host = lines['hostname']
        port = int(raw_input("Enter port:"))
        dbName = lines['dbname']
        collName = lines['tname']

        coll = get_collections(host,port,dbName,collName)
        colNames = get_colNames(coll)
        table =  get_table(coll,colNames)
        tb = etl.head(table,len(table)-1)
    return tb



INPUT_FILES = ("source_config.txt","target_config.txt")
print 'SERVICE STARTED...........'
while True:
    while True:
        f_exist = os.path.isfile(INPUT_FILES[1])
        if f_exist and time.time() - os.path.getmtime(INPUT_FILES[1]) < 3:
            details = getLines(INPUT_FILES[1])
            if details["DETAILS_FLAG"] == '1':
                break
        time.sleep(2.5)

    print 'READING INPUT FILE.......'
    lines = getLines(INPUT_FILES[0])
    tb = extract(lines)
    rmFileName = lines['FILE_NAME']
    print 'INPUT FILE LOADED.......'

    print 'LOADING INTO DATABASE.....'
    lines = getLines(INPUT_FILES[1])
    pkey = "id"
    load(tb,pkey,"localhost",lines['username'],lines['password'],lines['dbname'],lines['tname'],rmFileName)
    fo = open(INPUT_FILES[1],'w')
    fo.write('DETAILS_FLAG:0')
    fo.close()
    print 'FILE LOADED TO LOCAL DATABASE ......\n\n'
