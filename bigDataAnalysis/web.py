#apache spark libraries
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import col
from pyspark.sql import functions as F

#Graph plotting libraries
import matplotlib.pyplot as plt
import numpy as np

#system library
import sys
import time
import os


#math library
import math

#date parsing library
from dateutil.parser import *

#libraries for ETL SERVICE...
import petl as etl
import pymysql.cursors
import xml2json
import optparse
import json
from dateutil.parser import parse
from pymongo import MongoClient

#ETL SERVICES


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
def load(tb,pkey,hst,usr,pwd,dtb,tname):
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



def getDict(filename):
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

def getLines(filename):
    fo = open(filename,'r')
    lines = []
    while True:
        line = fo.readline()
        line = line.replace('\n','')
        if line == '':
            fo.close()
            return lines
        lines.append(line)
    return lines

def extract(lines):
    tb = None
    if lines['FILE_TYPE']=='CSV':
        filename = PATH_WEB_SERVER+'\\upload\\'+lines['FILE_NAME']
        tb = etl.fromcsv(filename)

    elif lines['FILE_TYPE']=='XML':
        # filename = lines['FILE_NAME']
        filename = PATH_WEB_SERVER+'\\upload\\'+lines['FILE_NAME']
        fo = open(filename,'r')
        f = fo.read()
        fo.close()
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
        # filename = lines['FILE_NAME']
        filename = PATH_WEB_SERVER+'\\upload\\'+lines['FILE_NAME']
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
        port = int(lines['port'])
        dbName = lines['dbname']
        collName = lines['tname']

        coll = get_collections(host,port,dbName,collName)
        colNames = get_colNames(coll)
        table =  get_table(coll,colNames)
        tb = etl.head(table,len(table)-1)
    return tb



#ETL SERVICES




#GLOBAL VALUES
PATH_WEB_SERVER = 'C:\\xampp\\htdocs'
df = 0 #global dataframe
GLOBALS ={}
GRAPH_TYPES = ('Bar chart','Piechart','Histogram','Scatter plot','Bar chart multiple',
               'Bar chart horizontal','Bar chart versus','Line chart')
OPS = ["int","discrete","boolean","string","double","timestamp"]

plot_details = {}

#UTILITY FUNCTIONS

def getDBdetails(filename):
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

def getIndices(values,searchVal):
    values = np.array(values)
    matches = np.where(values == searchVal)[0]
    return list(matches)

def linearDate(date_str):
    date_str = str(date_str)
    try:
        date_obj = parse(date_str)
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        val = year+ (month/12.0) + (day/365)
        return val
    except:
        print 'error passing date :'+str(date_str)
        return 0

def divideIntVal(colName):
    plot_details['no of bins'] = 10
    min_val = df.groupBy().min(colName).collect()[0][0]
    max_val = df.groupBy().max(colName).collect()[0][0]
    min_level = int(math.floor((min_val/10) * 10))
    max_level = int(math.ceil(((max_val/10)+1)*10))
    level_width = (max_level - min_level)/1.0
    level_width = int(math.ceil(level_width/int(plot_details['no of bins'])))
    return min_level,max_level,level_width



def plotGraph(graphName,choice,FILE_PATH):

    text_fields = ("no of bins","xlabel","ylabel","title")
    field_val = []

    filename = FILE_PATH + '\\config\\plotData.txt';
    fo = open(filename,'w');
    fo.write('RESPONSE_FLAG:1\n')
    fo.write('graphName:'+graphName+'\n')

    #bar chart
    if graphName == GRAPH_TYPES[0]:
        col_used = COL_NAMES[choice[0][0]][0]
        objects = []
        performance = []

        field_val = (10,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]

        #int data
        if choice[0][1] == OPS[0] or choice[0][1] == OPS[4]:
            min_level,max_level,level_width = divideIntVal(col_used)
            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used) > i) & (col(col_used) <= i+level_width)).count())

        #discrete or boolean data
        elif choice[0][1] == OPS[1] or choice[0][1] == OPS[2]:
            dis_obj = df.select(col_used).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]
            for attr in objects:
                performance.append( df.filter(df[col_used] == attr).count())

        fo.write('labels:'+str(objects))
        fo.write('\n')
        fo.write('values:'+str(performance))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))
        fo.write('\n')
        fo.write('ytitle:'+str(field_val[2]))
        fo.write('\n')
        fo.write('title:'+str(field_val[3]))

    #pie chart
    elif graphName == GRAPH_TYPES[1]:
        col_used = COL_NAMES[choice[0][0]][0]
        field_val = (10,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]

        performance = []
        sizes = []
        objects = []

        #int data
        if choice[0][1] == OPS[0] or choice[0][1] == OPS[4]:
            min_level,max_level,level_width = divideIntVal(col_used)

            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used) > i) & (col(col_used) <= i+level_width)).count())

        #discrete, boolean
        elif choice[0][1] == OPS[1] or choice[0][1] == OPS[2]:
            dis_obj = df.select(col_used).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]

            for attr in objects:
                performance.append( df.filter(df[col_used] == attr).count())

        fo.write('labels:'+str(objects))
        fo.write('\n')
        fo.write('values:'+str(performance))
        fo.write('\n')
        fo.write('title:'+str(field_val[3]))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))


    #scatter plot
    elif graphName == GRAPH_TYPES[3]:
        col_used1 = COL_NAMES[choice[0][0]][0]
        col_used2 = COL_NAMES[choice[1][0]][0]
        field_val = (10,col_used1,col_used2,str(col_used1)+' vs '+str(col_used2))
        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]
        x_df = np.asarray(df.select(col_used1).collect())
        y_df = np.asarray(df.select(col_used2).collect())
        y_df,x_df = zip(*sorted(zip(y_df,x_df)))


        fo.write('values:[')
        for i in range(len(y_df)):
            fo.write('[')
            if i == len(y_df)-1:
                fo.write(str(y_df[i][0]))
                fo.write(',')
                fo.write(str(x_df[i][0]))
                fo.write(']')
            else:
                fo.write(str(y_df[i][0]))
                fo.write(',')
                fo.write(str(x_df[i][0]))
                fo.write('],')
        fo.write(']')


        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))
        fo.write('\n')
        fo.write('ytitle:'+str(field_val[2]))
        fo.write('\n')
        fo.write('title:'+str(field_val[3]))


    #bar chart horizontal
    elif graphName == GRAPH_TYPES[5]:
        col_used = COL_NAMES[choice[0][0]][0]
        text_fields = ("no of bins","xlabel","ylabel","title")
        field_val = (10,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]

        objects = []
        performance = []

        field_val = (10,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]

        #int data
        if choice[0][1] == OPS[0] or choice[0][1] == OPS[4]:
            min_level,max_level,level_width = divideIntVal(col_used)

            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used) > i) & (col(col_used) <= i+level_width)).count())

        #discrete or boolean data
        elif choice[0][1] == OPS[1] or choice[0][1] == OPS[2]:
            dis_obj = df.select(col_used).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]
            for attr in objects:
                performance.append( df.filter(df[col_used] == attr).count())

        fo.write('labels:'+str(objects))
        fo.write('\n')
        fo.write('values:'+str(performance))
        fo.write('\n')
        fo.write('title:'+str(field_val[1]))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[3]))
        fo.write('\n')
        fo.write('ytitle:'+str(field_val[2]))

    #histogram
    elif graphName == GRAPH_TYPES[2]:
        col_used =  COL_NAMES[choice[0][0]][0]
        #text_fields = ("no of bins","xlabel","ylabel","title")
        field_val = (10,col_used,'frequency','histogram of '+str(col_used))
        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]

        df_col =  df.select(col_used).collect()
        xvalues = [x[0] for x in df_col]
        min_level,max_level,level_width = divideIntVal(col_used)

        fo.write('xvalues:'+str(xvalues))
        fo.write('\n')
        fo.write('minlevel:'+str(min_level))
        fo.write('\n')
        fo.write('maxlevel:'+str(max_level))
        fo.write('\n')
        fo.write('title:'+str(field_val[3]))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))




    #bar chart multiple
    elif graphName == GRAPH_TYPES[4]:

        ch_types = [x[1] for x in choice]

        #ch_req[0]:discrete,boolean,boolean
        #ch_req[1]:int,boolean,boolean
        ch_req = [[OPS[1],OPS[2],OPS[2]],[OPS[0],OPS[2],OPS[2]],[OPS[4],OPS[2],OPS[2]]]

        xlabel = []
        ylabel = ''
        yvalues1 = []
        yvalues2 = []

        #discrete,boolean,boolean:bar chart multiple
        if len(list(set(ch_types) ^ set(ch_req[0])))==0:


            ind_dis = ch_types.index(OPS[1])
            ind_bool1,ind_bool2 = getIndices(ch_types,OPS[2])

            col_used1 = COL_NAMES[choice[ind_dis][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool1][0]][0]
            col_used3 = COL_NAMES[choice[ind_bool2][0]][0]

            x_dis = df.select(COL_NAMES[choice[ind_dis][0]][0]).distinct().collect()
            xlabel = [str(x[0]) for x in x_dis]


            for i in range(len(xlabel)):
                yvalues1.append(df.filter((col(col_used2) == 'yes')&(col(col_used1) == xlabel[i])).count())
                yvalues2.append(df.filter((col(col_used3) == 'yes')&(col(col_used1) == xlabel[i])).count())

            legends = [col_used2,col_used3]
            field_val = (10,col_used1,'frequency',str(col_used1)+' vs '+str(col_used2)+' and '+str(col_used3))

        #int,boolean,boolean:bar chart multiple
        elif len(list(set(ch_types) ^ set(ch_req[1])))==0 or len(list(set(ch_types) ^ set(ch_req[2])))==0:
            ind_int = []
            print ch_types
            print ch_req[1]
            print ch_req[2]
            if len(list(set(ch_types) ^ set(ch_req[1])))==0:
                ind_int = ch_types.index(OPS[0])
            elif len(list(set(ch_types) ^ set(ch_req[2])))==0:
                ind_int = ch_types.index(OPS[4])
            print 'ind_int'+str(ind_int)
            ind_bool1,ind_bool2 = getIndices(ch_types,OPS[2])

            col_used1 = COL_NAMES[choice[ind_int][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool1][0]][0]
            col_used3 = COL_NAMES[choice[ind_bool2][0]][0]

            min_level,max_level,level_width = divideIntVal(col_used1)

            for i in range(min_level,max_level,level_width):
                xlabel.append(str(i)+'-'+str(i+level_width))
                yvalues1.append(df.filter((col(col_used1) > i) & (col(col_used1) <= i+level_width) & (col(col_used2) == 'yes')).count())
                yvalues2.append(df.filter((col(col_used1) > i) & (col(col_used1) <= i+level_width) & (col(col_used3) == 'yes')).count())

            legends = [col_used2,col_used3]
            field_val = (10,col_used1,'frequency',str(col_used1)+' vs '+str(col_used2)+' and '+str(col_used3))

        for x in range(len(text_fields)):
            plot_details[text_fields[x]] = field_val[x]

        fo.write('xlabel:'+str(xlabel))
        fo.write('\n')
        fo.write('ylabel:'+str(ylabel))
        fo.write('\n')
        fo.write('yvalues1:'+str(yvalues1))
        fo.write('\n')
        fo.write('yvalues2:'+str(yvalues2))
        fo.write('\n')
        fo.write('legends:'+str(legends))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))
        fo.write('\n')
        fo.write('ytitle:'+str(field_val[2]))


    #bar chart versus
    elif graphName == GRAPH_TYPES[6]:

        ch_types = [x[1] for x in choice]
        ch_req = [[OPS[0],OPS[2]],[OPS[1],OPS[2]],[OPS[4],OPS[2]]]


        objects = []
        performance = []

        #int data,double data
        if (len(list(set(ch_types) ^ set(ch_req[0])))==0) or (len(list(set(ch_types) ^ set(ch_req[2])))==0):
            ind_int = []
            if len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPS[0])
            elif len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPS[4])

            ind_bool = ch_types.index(OPS[2])

            col_used1 = COL_NAMES[choice[ind_int][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool][0]][0]

            min_level,max_level,level_width = divideIntVal(col_used1)

            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used1) > i) & (col(col_used1) <= i+level_width) & (col(col_used2) == 'yes')).count())
            field_val = (10,col_used1,col_used2,str(col_used1)+' vs '+str(col_used2))

        #discrete or boolean data
        elif len(list(set(ch_types) ^ set(ch_req[1])))==0:
            ind_dis = ch_types.index(OPS[1])
            ind_bool = ch_types.index(OPS[2])

            col_used1 = COL_NAMES[choice[ind_dis][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool][0]][0]

            dis_obj = df.select(col_used1).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]

            for i in range(len(objects)):
                performance.append(df.filter((col(col_used2) == 'yes')&(col(col_used1) == objects[i])).count())
            field_val = (10,col_used1,col_used2,str(col_used1)+' vs '+str(col_used2))

        fo.write('labels:'+str(list(objects)))
        fo.write('\n')
        fo.write('values:'+str(list(performance)))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))
        fo.write('\n')
        fo.write('ytitle:'+str(field_val[2]))
        fo.write('\n')
        fo.write('title:'+str(field_val[3]))



    #line chart
    elif graphName == GRAPH_TYPES[7]:
        xvalues = []
        yvalues = []
        ch_types = [x[1] for x in choice]
        ch_req = [[OPS[0],OPS[5]],[OPS[4],OPS[5]],[OPS[2],OPS[5]]]

        #int,date
        if len(list(set(ch_types) ^ set(ch_req[0])))==0 or len(list(set(ch_types) ^ set(ch_req[1])))==0:
            ind_int = None
            if len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPS[0])
            else:
                ind_int = ch_types.index(OPS[4])

            col_usedY = COL_NAMES[choice[ind_int][0]][0]
            df_col =  df.select(col_usedY).collect()
            yvalues = [x[0] for x in df_col]

            ind_date = ch_types.index(OPS[5])
            col_usedX = COL_NAMES[choice[ind_date][0]][0]
            df_col =  df.select(col_usedX).collect()
            xvalues = [linearDate(x[0]) for x in df_col]
            xvalues,yvalues = zip(*sorted(zip(xvalues,yvalues)))

            field_val = (10,col_usedX,col_usedY,str(col_usedX)+' vs '+str(col_usedY))
            for x in range(len(text_fields)):
                plot_details[text_fields[x]] = field_val[x]

        #bool,date
        elif len(list(set(ch_types) ^ set(ch_req[2])))==0:

            ind_date = ch_types.index(OPS[5])
            col_usedX = COL_NAMES[choice[ind_date][0]][0]
            df_col =  df.select(col_usedX).collect()
            xvalues = [linearDate(x[0]) for x in df_col]

            ind_bool = ch_types.index(OPS[2])
            col_usedY = COL_NAMES[choice[ind_int][0]][0]

            yvalues = []
            for i in range(len(xvalues)):
                #df.filter((col(col_usedY) == 'yes')&(col(col_usedX) == df_col[i][])).count()
                yvalues.append(df.filter((col(col_usedY) == 'yes')&(col(col_usedX) == df_col[i][0])).count())


            #xvalues,yvalues = zip(*sorted(zip(xvalues,yvalues)))

            field_val = (10,col_usedX,col_usedY,str(col_usedX)+' vs '+str(col_usedY))
            for x in range(len(text_fields)):
                plot_details[text_fields[x]] = field_val[x]

        fo.write('xvalues:'+str(list(xvalues)))
        fo.write('\n')
        fo.write('yvalues:'+str(list(yvalues)))
        fo.write('\n')
        fo.write('xtitle:'+str(field_val[1]))
        fo.write('\n')
        fo.write('ytitle:'+str(field_val[2]))
        fo.write('\n')
        fo.write('title:'+str(field_val[3]))

    fo.close()
    filename = FILE_PATH+"\\config\\selection.txt"
    fo = open(filename,'w')
    fo.write('REQUEST_FLAG:0')
    fo.close()


#CREATING COLUMNS UI
def writeColumns(COL_NAMES,FIRST_ROW,FILE_PATH):
    filename = FILE_PATH+"\\config\\cols.txt"
    fo = open(filename,'w')
    type_var = []
    #drop down OPS
    #creating UI elments
    for x in range(len(COL_NAMES)):
        type_var.append("")

        #choosing default option
        default_option = COL_NAMES[x][1]
        temp = str(FIRST_ROW[0][x]).lower()

        if default_option == 'string' and (temp=='yes' or temp=='no' or temp=='true' or temp=='false'):
            default_option = OPS[2]
        elif default_option == 'string' and len(df.select(COL_NAMES[x][0]).distinct().collect()) < 30:
            default_option = OPS[1]
        elif default_option == 'string':
            try:
                parse(temp)
                default_option = OPS[5]
            except:
                pass

        type_var[x] = default_option
        fo.write(COL_NAMES[x][0]+':'+default_option+'\n')
    fo.close()

    filename = FILE_PATH+"\\config\\dbDetails.txt"
    fo = open(filename,'w')
    fo.write('COL_FLAG:1')
    fo.close()

def getChoices(details,FILE_PATH):
    filename = FILE_PATH+"\\config\\selection.txt"
    graphName = None;
    choices = []

    #process starts
    graphName = details['GraphName']
    try:
        GRAPH_TYPES.index(graphName)
    except:
        graphName = graphName.replace('_',' ')
    del details['GraphName']
    del details['REQUEST_FLAG']
    del details['RESPONSE_FLAG']
    COL = [x[0] for x in COL_NAMES]
    for key in details:
        choices.append((COL.index(key),details[key]))
    print 'graph name:'+str(graphName)
    print 'graph_choices: '+str(choices)
    plotGraph(graphName,choices,FILE_PATH)
    choices = []
    #process ends



if __name__ == "__main__":

    #creating spark context
    sc = SparkContext(appName = "My App")
    sqlContext = SQLContext(sc)
    INPUT_FILES = (PATH_WEB_SERVER+"\\upload\\source_config.txt",PATH_WEB_SERVER+"\\upload\\target_config.txt")


    print 'SERVER STARTED.........'
    while True:
        #getting choices and plotting
        filename = PATH_WEB_SERVER+"\\config\\selection.txt"
        sel_file_exist = os.path.isfile(filename)
        if sel_file_exist and time.time() - os.path.getmtime(filename) < 3:
            details = getDBdetails(filename)
            if details["REQUEST_FLAG"] == '1':
                getChoices(details,PATH_WEB_SERVER)


        #waiting for the database details
        FILE_NAME = "\\config\\dbDetails.txt"
        db_details = None
        if time.time() - os.path.getmtime(PATH_WEB_SERVER+FILE_NAME) < 3:
            lines = getLines(PATH_WEB_SERVER+FILE_NAME)
            if ('DETAILS_FLAG:1' in lines):
                db_details = getDBdetails(PATH_WEB_SERVER+FILE_NAME)
                print 'spark: '+str(db_details)
                #importing data from MySQL database
                try:
                    df = sqlContext.read.format("jdbc").options(
                    url ="jdbc:mysql://localhost/"+db_details['dbname'],
                    driver="com.mysql.jdbc.Driver",
                    dbtable = db_details['tname'],
                    user = db_details['username'],
                    password = db_details['password']
                    ).load()
                    print 'IMPORT SUCCESSFUL....'
                except:
                    print 'ERROR IMPORTING....'
                    print 'PLEASE TRY AGAIN\n'
                    filename = PATH_WEB_SERVER+"\\config\\dbDetails.txt"
                    fo = open(INPUT_FILES[1],'w')
                    fo.write('DETAILS_FLAG:0')
                    fo.close()
                    filename = PATH_WEB_SERVER+"\\config\\dbDetails.txt"
                    fo = open(filename,'w')
                    fo.write('ERROR_FLAG:2')
                    fo.close()
                    time.sleep(2.5)
                    continue


                print 'GENERATING COLUMNS....'
                COL_NAMES = df.dtypes
                FIRST_ROW =  df.take(1)
                writeColumns(COL_NAMES,FIRST_ROW,PATH_WEB_SERVER)


        #ETL SERVICE
        f_exist = os.path.isfile(INPUT_FILES[1])
        if f_exist and time.time() - os.path.getmtime(INPUT_FILES[1]) < 3:
            lines = getLines(INPUT_FILES[1])
            if('DETAILS_FLAG:1' in lines):
                details = getDict(INPUT_FILES[1])
                print 'READING INPUT FILE.......'
                try:
                    lines = getDict(INPUT_FILES[0])
                    tb = extract(lines)
                    print 'INPUT FILE LOADED.......'
                except:
                    print 'error in source details'

                    fo = open(INPUT_FILES[1],'w')
                    fo.write('DETAILS_FLAG:0')
                    fo.close()

                    filename = PATH_WEB_SERVER+"\\config\\dbDetails.txt"
                    fo = open(filename,'w')
                    fo.write('ERROR_FLAG:1')
                    fo.close()
                    time.sleep(2.5)
                    continue



                print 'LOADING INTO TARGET DATABASE.....'
                lines = getDict(INPUT_FILES[1])
                pkey = "id"
                try:
                    load(tb,pkey,lines['hostname'],lines['username'],lines['password'],lines['dbname'],lines['tname'])
                except:
                    print 'error in target details\n'
                    fo = open(INPUT_FILES[1],'w')
                    fo.write('DETAILS_FLAG:0')
                    fo.close()
                    filename = PATH_WEB_SERVER+"\\config\\dbDetails.txt"
                    fo = open(filename,'w')
                    fo.write('ERROR_FLAG:2')
                    fo.close()
                    time.sleep(2.5)
                    continue

                try:
                    lines = getDict(INPUT_FILES[0])
                    rmFileName = PATH_WEB_SERVER+'\\upload\\'+lines['FILE_NAME']
                    print rmFileName
                    os.remove(rmFileName)
                    print 'file removed successfully'
                except:
                    print 'error deleting the uploaded file or there is no file uploaded'

                fo = open(INPUT_FILES[1],'w')
                fo.write('DETAILS_FLAG:0')
                fo.close()
                print 'FILE LOADED TO LOCAL DATABASE ......\n\n'
        time.sleep(2.5)
