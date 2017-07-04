#apache spark libraries
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import col
from pyspark.sql import functions as F

#Graph plotting libraries
import matplotlib.pyplot as plt
import numpy as np

#GUI library
from Tkinter import *

#system library
import sys

#math library
import math

#date parsing library
from dateutil.parser import *


#GLOBAL VALUES
GLOBALS ={}
GLOBALS['SUGGESTIONS_LABEL'] = 0
GLOBALS['SUGGESTED_TABLES'] = 0
GRAPH_TYPES = ('Bar chart','Piechart','Histogram','Scatter plot','Bar chart multiple',
               'Bar chart horizontal','Bar chart versus','Line chart')
radio_buttons=[]
plot_details = {}

#UTILITY FUNCTIONS
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
    min_val = df.groupBy().min(colName).collect()[0][0]
    max_val = df.groupBy().max(colName).collect()[0][0]
    min_level = int(math.floor((min_val/10) * 10))
    max_level = int(math.ceil(((max_val/10)+1)*10))
    level_width = (max_level - min_level)/1.0
    level_width = int(math.ceil(level_width/int(plot_details['no of bins'])))
    return min_level,max_level,level_width

#LINE CHART PLOTTING FUNCTION
def draw_line_chart(x,y):
    plt.plot(x,y)
    plt.ylabel(plot_details['ylabel'])
    plt.xlabel(plot_details['xlabel'])
    plt.title(plot_details['title'])
    plt.show()

#BAR CHART MULTIPLE PLOTTING FUNCTION
def draw_bar_chart_legend(xlabel,ylabel,yvalues1,yvalues2,legends):
    N = len(xlabel)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.27       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    yvals = yvalues1
    rects1 = ax.bar(ind, yvals, width, color='r')
    zvals = yvalues2
    rects2 = ax.bar(ind+width, zvals, width, color='g')

    ax.set_ylabel(ylabel)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( xlabel,rotation = 'vertical' )
    ax.legend( (rects1[0], rects2[0]), legends )

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    plt.title(plot_details['title'])
    plt.xlabel(plot_details['xlabel'])
    plt.ylabel(plot_details['ylabel'])
    plt.show()

#HISTOGRAM PLOTIING FUNCTION
def draw_hist(xvalues,min_val,max_val):
    bins = np.linspace(min_val, max_val, int(plot_details['no of bins']))

    plt.hist(xvalues, bins=bins,alpha=0.5, histtype='bar', ec='black')
    plt.xlabel(plot_details['xlabel'])
    plt.ylabel(plot_details['ylabel'])
    plt.title(plot_details['title'])
    plt.show()


#PIE CHART PLOTIING FUNCTION
def draw_pie_chart(labels,sizes):

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    explode = np.zeros(len(sizes),dtype=np.int)  # only explode the highest values
    explode = tuple(explode)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title(plot_details['title'])
    plt.show()


#BAR CHART PLOTIING FUNCTION
def draw_bars(objects,performance):
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects,rotation='vertical')
    plt.xlabel(plot_details['xlabel'])
    plt.ylabel(plot_details['ylabel'])
    plt.title(plot_details['title'])
    plt.show()

#SCATTER PLOT PLOTTING FUNCTION
def draw_scattered(xvalues,yvalues):
    plt.scatter(xvalues,yvalues,marker='+')
    plt.xlabel(plot_details['xlabel'])
    plt.ylabel(plot_details['ylabel'])
    plt.title(plot_details['title'])
    plt.show()

#HORIZONTAL BAR CHART PLOTTING FUNCTION
def draw_hbars(labels,values):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    y_pos = np.arange(len(labels))

    performance = values
    error = np.random.rand(len(labels))

    ax.barh(y_pos, performance, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(plot_details['xlabel'])
    ax.set_title(plot_details['title'])

#PLOTTING FUNCTION

def parseFields(top,entry_fields,graphName,choice,OPTIONS):
    fields = ('no of bins','xlabel','ylabel','title')
    for x in range(len(fields)):
        if entry_fields[x].get() != '':
            plot_details[fields[x]] = entry_fields[x].get()
        else:
            plot_details[fields[x]] = ''

    top.destroy()
    plotGraph(graphName,choice,OPTIONS)

#INTERMEDIATE DIALOG BOX
def createEntryDialog(graphName,choice,OPTIONS):
    text_fields = ("no of bins","xlabel","ylabel","title")
    top = Tk()
    frame = []
    for x in range(5):
        frame.append(Frame(top))
        frame[x].pack()

    entry_fields = []
    for x in range(len(text_fields)):
        Label(frame[x], text=text_fields[x]).pack( anchor = W)
        entry_fields.append(Entry(frame[x], bd =5,width = 20))
        entry_fields[x].pack(side = RIGHT)

    B = Button(frame[4], text ="submit", command =lambda: parseFields(top,entry_fields,graphName,choice,OPTIONS))
    B.pack()
    top.geometry('{}x{}'.format(400,400))
    top.mainloop()

def plotGraph(graphName,choice,OPTIONS):
    print 'choice: '+str(choice)

    text_fields = ("no of bins","xlabel","ylabel","title")
    field_val = []

    #OPTIONS = ["int","discrete","boolean","string","double","timestamp"]
    #GRAPH_TYPES = ('Bar chart','Piechart','Histogram','Scatter plot','Bar chart multiple','Bar chart horizontal')

    #bar chart
    if graphName == GRAPH_TYPES[0]:
        col_used = COL_NAMES[choice[0][0]][0]
        objects = []
        performance = []

        field_val = (0,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]

        #int data
        if choice[0][1] == OPTIONS[0] or choice[0][1] == OPTIONS[4]:

            min_level,max_level,level_width = divideIntVal(col_used)
            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used) > i) & (col(col_used) <= i+level_width)).count())

        #discrete or boolean data
        elif choice[0][1] == OPTIONS[1] or choice[0][1] == OPTIONS[2]:
            dis_obj = df.select(col_used).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]
            for attr in objects:
                performance.append( df.filter(df[col_used] == attr).count())

        draw_bars(objects,performance)

    #pie chart
    elif graphName == GRAPH_TYPES[1]:
        col_used = COL_NAMES[choice[0][0]][0]
        field_val = (0,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]

        performance = []
        sizes = []
        objects = []

        #int data
        if choice[0][1] == OPTIONS[0] or choice[0][1] == OPTIONS[4]:
            min_level,max_level,level_width = divideIntVal(col_used)

            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used) > i) & (col(col_used) <= i+level_width)).count())

        #discrete, boolean
        elif choice[0][1] == OPTIONS[1] or choice[0][1] == OPTIONS[2]:
            dis_obj = df.select(col_used).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]

            for attr in objects:
                    performance.append( df.filter(df[col_used] == attr).count())

        total = float(sum(performance))
        for x in range(len(performance)):
            sizes.append(performance[x]/total)

        draw_pie_chart(objects,sizes)


    #scatter plot
    elif graphName == GRAPH_TYPES[3]:
        col_used1 = COL_NAMES[choice[0][0]][0]
        col_used2 = COL_NAMES[choice[1][0]][0]
        field_val = (0,col_used1,col_used2,str(col_used1)+' vs '+str(col_used2))
        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]
        x_df = np.asarray(df.select(col_used1).collect())
        y_df = np.asarray(df.select(col_used2).collect())
        draw_scattered(x_df,y_df)


    #bar chart horizontal
    elif graphName == GRAPH_TYPES[5]:
        col_used = COL_NAMES[choice[0][0]][0]
        text_fields = ("no of bins","xlabel","ylabel","title")
        field_val = (0,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]

        objects = []
        performance = []

        field_val = (0,col_used,'frequency',col_used)
        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]

        #int data
        if choice[0][1] == OPTIONS[0] or choice[0][1] == OPTIONS[4]:
            min_level,max_level,level_width = divideIntVal(col_used)

            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used) > i) & (col(col_used) <= i+level_width)).count())

        #discrete or boolean data
        elif choice[0][1] == OPTIONS[1] or choice[0][1] == OPTIONS[2]:
            dis_obj = df.select(col_used).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]
            for attr in objects:
                performance.append( df.filter(df[col_used] == attr).count())

        draw_hbars(objects,performance)

    #histogram
    elif graphName == GRAPH_TYPES[2]:
        col_used =  COL_NAMES[choice[0][0]][0]
        #text_fields = ("no of bins","xlabel","ylabel","title")
        field_val = (0,col_used,'frequency','histogram of '+str(col_used))
        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]

        df_col =  df.select(col_used).collect()
        xvalues = [x[0] for x in df_col]
        min_level,max_level,level_width = divideIntVal(col_used)
        draw_hist(xvalues,min_level,max_level)

    #bar chart multiple
    elif graphName == GRAPH_TYPES[4]:

        ch_types = [x[1] for x in choice]

        #ch_req[0]:discrete,boolean,boolean
        #ch_req[1]:int,boolean,boolean
        ch_req = [[OPTIONS[1],OPTIONS[2],OPTIONS[2]],[OPTIONS[0],OPTIONS[2],OPTIONS[2]],[OPTIONS[4],OPTIONS[2],OPTIONS[2]]]

        xlabel = []
        ylabel = ''
        yvalues1 = []
        yvalues2 = []

        #discrete,boolean,boolean:bar chart multiple
        if len(list(set(ch_types) ^ set(ch_req[0])))==0:


            ind_dis = ch_types.index(OPTIONS[1])
            ind_bool1,ind_bool2 = getIndices(ch_types,OPTIONS[2])

            col_used1 = COL_NAMES[choice[ind_dis][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool1][0]][0]
            col_used3 = COL_NAMES[choice[ind_bool2][0]][0]

            x_dis = df.select(COL_NAMES[choice[ind_dis][0]][0]).distinct().collect()
            xlabel = [str(x[0]) for x in x_dis]


            for i in range(len(xlabel)):
                yvalues1.append(df.filter((col(col_used2) == 'yes')&(col(col_used1) == xlabel[i])).count())
                yvalues2.append(df.filter((col(col_used3) == 'yes')&(col(col_used1) == xlabel[i])).count())

            legends = [col_used2,col_used3]
            field_val = (0,col_used1,'frequency',str(col_used1)+' vs '+str(col_used2)+' and '+str(col_used3))

        #int,boolean,boolean:bar chart multiple
        elif len(list(set(ch_types) ^ set(ch_req[1])))==0 or len(list(set(ch_types) ^ set(ch_req[2])))==0:
            ind_int = []
            if len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPTIONS[0])
            elif len(list(set(ch_types) ^ set(ch_req[2])))==0:
                ind_int = ch_types.index(OPTIONS[4])

            ind_bool1,ind_bool2 = getIndices(ch_types,OPTIONS[2])

            col_used1 = COL_NAMES[choice[ind_int][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool1][0]][0]
            col_used3 = COL_NAMES[choice[ind_bool2][0]][0]

            min_level,max_level,level_width = divideIntVal(col_used1)

            for i in range(min_level,max_level,level_width):
                xlabel.append(str(i)+'-'+str(i+level_width))
                yvalues1.append(df.filter((col(col_used1) > i) & (col(col_used1) <= i+level_width) & (col(col_used2) == 'yes')).count())
                yvalues2.append(df.filter((col(col_used1) > i) & (col(col_used1) <= i+level_width) & (col(col_used3) == 'yes')).count())

            legends = [col_used2,col_used3]
            field_val = (0,col_used1,'frequency',str(col_used1)+' vs '+str(col_used2)+' and '+str(col_used3))

        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]
        draw_bar_chart_legend(xlabel,ylabel,yvalues1,yvalues2,legends)

    #bar chart versus
    elif graphName == GRAPH_TYPES[6]:

        ch_types = [x[1] for x in choice]
        ch_req = [[OPTIONS[0],OPTIONS[2]],[OPTIONS[1],OPTIONS[2]],[OPTIONS[4],OPTIONS[2]]]

        print ch_types

        objects = []
        performance = []

        #int data,double data
        if (len(list(set(ch_types) ^ set(ch_req[0])))==0) or (len(list(set(ch_types) ^ set(ch_req[2])))==0):
            print 'inside int'
            ind_int = []
            if len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPTIONS[0])
            elif len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPTIONS[4])

            ind_bool = ch_types.index(OPTIONS[2])

            col_used1 = COL_NAMES[choice[ind_int][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool][0]][0]

            min_level,max_level,level_width = divideIntVal(col_used1)

            for i in range(min_level,max_level,level_width):
                objects.append(str(i)+'-'+str(i+level_width))
                performance.append(df.filter((col(col_used1) > i) & (col(col_used1) <= i+level_width) & (col(col_used2) == 'yes')).count())
            field_val = (0,col_used1,col_used2,str(col_used1)+' vs '+str(col_used2))

        #discrete or boolean data
        elif len(list(set(ch_types) ^ set(ch_req[1])))==0:
            print 'inside dis'
            ind_dis = ch_types.index(OPTIONS[1])
            ind_bool = ch_types.index(OPTIONS[2])

            col_used1 = COL_NAMES[choice[ind_dis][0]][0]
            col_used2 = COL_NAMES[choice[ind_bool][0]][0]

            dis_obj = df.select(col_used1).distinct().collect()
            objects = [str(x[0]) for x in dis_obj]

            for i in range(len(objects)):
                performance.append(df.filter((col(col_used2) == 'yes')&(col(col_used1) == objects[i])).count())
            field_val = (0,col_used1,col_used2,str(col_used1)+' vs '+str(col_used2))
        print plot_details
        print text_fields
        print field_val

        for x in range(len(text_fields)):
            if plot_details[text_fields[x]] == '':
                plot_details[text_fields[x]] = field_val[x]

        draw_bars(objects,performance)

    #line chart
    elif graphName == GRAPH_TYPES[7]:
        ch_types = [x[1] for x in choice]
        ch_req = [[OPTIONS[0],OPTIONS[5]],[OPTIONS[4],OPTIONS[5]],[OPTIONS[2],OPTIONS[5]]]

        #int,date
        if len(list(set(ch_types) ^ set(ch_req[0])))==0 or len(list(set(ch_types) ^ set(ch_req[1])))==0:
            ind_int = None
            if len(list(set(ch_types) ^ set(ch_req[0])))==0:
                ind_int = ch_types.index(OPTIONS[0])
            else:
                ind_int = ch_types.index(OPTIONS[4])

            col_usedY = COL_NAMES[choice[ind_int][0]][0]
            df_col =  df.select(col_usedY).collect()
            yvalues = [x[0] for x in df_col]

            ind_date = ch_types.index(OPTIONS[5])
            col_usedX = COL_NAMES[choice[ind_date][0]][0]
            df_col =  df.select(col_usedX).collect()
            xvalues = [linearDate(x[0]) for x in df_col]
            xvalues,yvalues = zip(*sorted(zip(xvalues,yvalues)))

            field_val = (0,col_usedX,col_usedY,str(col_usedX)+' vs '+str(col_usedY))
            for x in range(len(text_fields)):
                if plot_details[text_fields[x]] == '':
                    plot_details[text_fields[x]] = field_val[x]

            draw_line_chart(xvalues,yvalues)

        #bool,date
        elif len(list(set(ch_types) ^ set(ch_req[2])))==0:

            ind_date = ch_types.index(OPTIONS[5])
            col_usedX = COL_NAMES[choice[ind_date][0]][0]
            df_col =  df.select(col_usedX).collect()
            xvalues = [linearDate(x[0]) for x in df_col]

            ind_bool = ch_types.index(OPTIONS[2])
            col_usedY = COL_NAMES[choice[ind_int][0]][0]

            yvalues = []
            for i in range(len(xvalues)):
                #df.filter((col(col_usedY) == 'yes')&(col(col_usedX) == df_col[i][])).count()
                yvalues.append(df.filter((col(col_usedY) == 'yes')&(col(col_usedX) == df_col[i][0])).count())


            xvalues,yvalues = zip(*sorted(zip(xvalues,yvalues)))

            field_val = (0,col_usedX,col_usedY,str(col_usedX)+' vs '+str(col_usedY))
            for x in range(len(text_fields)):
                if plot_details[text_fields[x]] == '':
                    plot_details[text_fields[x]] = field_val[x]

            draw_line_chart(xvalues,yvalues)






#MAIN PAGE UI
def submit_db(text_fields,entry_fields,top):
    global db_details
    db_details = {}
    for x in range(len(text_fields)):
        db_details[text_fields[x]] = entry_fields[x].get()
    top.destroy()
    return db_details


def createMainPage():
    text_fields = ("database name","table name","username","password")
    top = Tk()
    frame = []

    label = Label( top, text='INPUT DATABASE DETAILS',pady=20).pack()

    for x in range(5):
        frame.append(Frame(top))
        frame[x].pack()

    entry_fields = []
    for x in range(len(text_fields)):
        Label(frame[x], text=text_fields[x]).pack( anchor = W)
        entry_fields.append(Entry(frame[x], bd =5,width = 20))
        entry_fields[x].pack(side = RIGHT)


    B = Button(frame[4], text ="import", command =lambda: submit_db(text_fields,entry_fields,top))
    B.pack()
    top.geometry('{}x{}'.format(400,400))
    top.mainloop()



def nothing():
    pass


def getSuggestedGraphs(choices,OPTIONS):
    #GRAPH_TYPES = ('Bar chart','Piechart','Histogram','Scatter plot','Bar chart multiple',
    #'Bar chart horizontal','Bar chart versus')

    OPTIONS = ["int","discrete","boolean","string","double","timestamp"]
    if len(choices)==1:
        #int or double: pie chart,bar chart,histogram
        if choices[0][1]==OPTIONS[0] or choices[0][1]==OPTIONS[4]:
            return tuple([GRAPH_TYPES[0],GRAPH_TYPES[1],GRAPH_TYPES[2]])
        #discrete: pie chart,bar chart
        elif choices[0][1]==OPTIONS[1]:
            return tuple([GRAPH_TYPES[0],GRAPH_TYPES[1]])
        #boolean:
        elif choices[0][1]==OPTIONS[2]:
            return tuple([GRAPH_TYPES[0],GRAPH_TYPES[1]])

    elif len(choices)==2:
        ch_types = [x[1] for x in choices]

        ch_req = [[OPTIONS[0],OPTIONS[0]],[OPTIONS[0],OPTIONS[4]],
                  [OPTIONS[0],OPTIONS[2]],[OPTIONS[4],OPTIONS[2]],[OPTIONS[1],OPTIONS[2]],
                  [OPTIONS[0],OPTIONS[5]],[OPTIONS[2],OPTIONS[5]],[OPTIONS[4],OPTIONS[5]]]

        #int,int:scatter plots
        #double,int:scatter plots
        if len(list(set(ch_types) ^ set(ch_req[0])))==0 or len(list(set(ch_types) ^ set(ch_req[1])))==0:
            return tuple([GRAPH_TYPES[3]])
        #int,bool or dis,bool or double,bool: bar chart
        elif len(list(set(ch_types) ^ set(ch_req[2])))==0 or len(list(set(ch_types) ^ set(ch_req[3])))==0\
             or len(list(set(ch_types) ^ set(ch_req[4])))==0:
            return tuple([GRAPH_TYPES[6]])

        #int,date or bool,date: line chart
        elif len(list(set(ch_types) ^ set(ch_req[5])))==0 or len(list(set(ch_types) ^ set(ch_req[6])))==0\
             or len(list(set(ch_types) ^ set(ch_req[7])))==0:
            return tuple([GRAPH_TYPES[7]])


    elif len(choices)==3:

        ch_types = [x[1] for x in choices]

        #ch_req[0]:discrete,boolean,boolean
        #ch_req[1]:int,boolean,boolean
        #ch_req[2]:double,boolean,boolean
        ch_req = [[OPTIONS[1],OPTIONS[2],OPTIONS[2]],[OPTIONS[0],OPTIONS[2],OPTIONS[2]],[OPTIONS[4],OPTIONS[2],OPTIONS[2]]]

        #discrete,boolean,boolean:bar chart multiple
        if len(list(set(ch_types) ^ set(ch_req[0])))==0:
            return tuple([GRAPH_TYPES[4]])
        #int,boolean,boolean:bar chart multiple
        #double,boolean,boolean:bar chart multiple
        elif len(list(set(ch_types) ^ set(ch_req[1])))==0 or len(list(set(ch_types) ^ set(ch_req[2])))==0:
            return tuple([GRAPH_TYPES[4]])



def fetchGraphs(col_var,type_var,COL_NAMES,OPTIONS,root,sugg_frame):
    global GLOBALS,radio_buttons
    choices = []
    for x in range(len(col_var)):
        if col_var[x].get() == 1:
            choices.append((x,type_var[x].get()))
    if GLOBALS['SUGGESTIONS_LABEL'] == 0:
        #displaying suggestions
        Label(root, text='Suggested Graphs',pady = 10).pack( anchor = CENTER)
        GLOBALS['SUGGESTIONS_LABEL'] = 1

    for x in radio_buttons:
        x.destroy()
    del radio_buttons[:]
    suggestions = getSuggestedGraphs(choices,OPTIONS)
    sugg_choice = IntVar()
    try:
        for x in range(len(suggestions)):
            radio_buttons.append(Radiobutton(sugg_frame, text=suggestions[x], variable=sugg_choice, value=x,command=nothing))
            radio_buttons[x].pack(anchor=W)
    except:
        pass
    sugg_frame.pack()
    GLOBALS['SUGGESTED_TABLES'] = 0
    radio_buttons.append(Button(root, text ="Plot", command =lambda:createEntryDialog(suggestions[sugg_choice.get()],choices,OPTIONS) ))

    radio_buttons[-1].pack()


#CREATING COLUMNS UI
def createColumnsPage(COL_NAMES,FIRST_ROW):
    #selector buttons
    buttons = []
    #root window
    root = Tk()
    #root.resizable(width=False, height=False)
    #root.geometry('{}x{}'.format(600,600))

    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    #selector column variables
    col_var = []
    for x in range(len(COL_NAMES)):
        col_var.append(IntVar())

    #Heading
    label = Label(root)
    Label(root, text='TABLE COLUMNS',pady=30).pack( anchor = CENTER)
    label = Label(root)
    Label(root, text='\t\tCOLUMNS\t\tDATA TYPE',pady=10).pack( anchor = CENTER)

    #drop down options
    OPTIONS = ["int","discrete","boolean","string","double","timestamp"]
    type_var = []
    #frames used for organising rows
    sel_frame = []

    #creating UI elments
    for x in range(len(COL_NAMES)):
        sel_frame.append(Frame(root));
        sel_frame[x].pack(anchor = CENTER)
        buttons.append(Checkbutton(sel_frame[x], text = COL_NAMES[x][0], variable = col_var[x],\
                                   onvalue = 1,offvalue = 0,width=30))
        type_var.append(StringVar(sel_frame[x]))

        #choosing default option
        default_option = COL_NAMES[x][1]
        temp = str(FIRST_ROW[0][x]).lower()

        if default_option == 'string' and (temp=='yes' or temp=='no' or temp=='true' or temp=='false'):
            default_option = OPTIONS[2]
        elif default_option == 'string' and len(df.select(COL_NAMES[x][0]).distinct().collect()) < 30:
            default_option = OPTIONS[1]
        elif default_option == 'string':
            try:
                parse(temp)
                default_option = OPTIONS[5]
            except:
                pass

        type_var[x].set(default_option) # default value

        w = apply(OptionMenu, (sel_frame[x], type_var[x]) + tuple(OPTIONS))
        buttons[x].pack(side=LEFT)
        w.pack(side=LEFT)
    sugg_frame = Frame(root)


    #fetch graph button
    Button(root, text ="fetch graphs", command =lambda: fetchGraphs(col_var,type_var,COL_NAMES,OPTIONS,root,sugg_frame)).pack(anchor = CENTER)
    root.mainloop()



if __name__ == "__main__":

    sc = SparkContext(appName = "My App")
    sqlContext = SQLContext(sc)
    #global data frame
    df = 0

    #creating main page UI
    print 'GENERATING IMPORT WINDOW....'
    db_details = {}


    createMainPage()
    #importing data from MySQL database
    try:
        df = sqlContext.read.format("jdbc").options(
        url ="jdbc:mysql://localhost/"+db_details['database name'],
        driver="com.mysql.jdbc.Driver",
        dbtable = db_details['table name'],
        user = db_details['username'],
        password = db_details['password']
        ).load()
        print 'IMPORT SUCCESSFUL....'
    except:
        print 'ERROR IMPORTING....'
        sys.exit()


    print 'GENERATING COLUMNS....'
    COL_NAMES = df.dtypes
    FIRST_ROW =  df.take(1)
    createColumnsPage(COL_NAMES,FIRST_ROW)
