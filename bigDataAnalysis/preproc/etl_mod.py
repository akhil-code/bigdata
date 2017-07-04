import petl as etl
import sys
import pymysql.cursors
import xml2json
import optparse
import json
from dateutil.parser import parse
from pymongo import MongoClient
import sys

#import MySQLdb

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
    l.append(t)
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
    print a
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

#Extract the data from a file. Returns a two dimensional list or table object. Arguments: file path
def extract(file):
    tb = list()
    if file == "sql":
        host = raw_input("Enter Host:")
        user = raw_input("Enter Username:")
        pwd = raw_input("Enter pwd:")
        dtb = raw_input("Enter Database Name:")
        table = raw_input("Enter Table Name:")
        conn = pymysql.connect(host=host,
                               user=user,
                               password=pwd,
                               db=dtb,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        temp = etl.fromdb(conn, "SELECT * FROM " + table)
        tb = d2l(temp)
    elif file=="mongodb":
        host = raw_input("Enter Host:")
        port = int(raw_input("Enter port:"))
        dbName = raw_input("Enter Database Name:")
        collName = raw_input("Enter collection Name:")

        coll = get_collections(host,port,dbName,collName)
        colNames = get_colNames(coll)
        table =  get_table(coll,colNames)
        tb = etl.head(table,len(table)-1)

    elif ".csv" in file:
        tb = etl.fromcsv(file)
    elif ".xlsx" in file:
        tb = etl.fromxls(file)
    elif ".json" in file:
        tb = etl.fromjson(file)
    elif ".xml" in file:
        f = open(file,'r').read()
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
        #tb = etl.fromxml(file,'.//ROW',{'Service_Name':'Service_Name','Status':'Status','Service_Type':'Service_Type','Time':'Time'})
    elif ".txt" in file:
        tb = etl.fromtext(file)
        print tb
    return tb

#loads the data into MySQL database. Arguments: Table Object
def load(tb,pkey,hst,usr,pwd,dtb):
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
    print "Done loading."
    db.commit()

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

filename =
lines = getLines("")



file = sys.argv[1] #File name passed as an argument in command line

tb = extract(file) #store the list in a variable
load(tb,pkey,host,user,passwd,db) #load the data in the database.
