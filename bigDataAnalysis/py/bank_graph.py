from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.functions import col
import matplotlib.pyplot as plt
import numpy as np


def draw_bar_chart_legend(xlabel,x_axis_label,ylabel,yvalues1,yvalues2,legends,title):
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
    plt.title(title)
    plt.xlabel(x_axis_label)

    plt.show()

def draw_pie_chart(labels,sizes,title):

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    explode = np.zeros(len(sizes),dtype=np.int)  # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = tuple(explode)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title(title)
    plt.show()

def draw_hbars(labels,values,xlabel,title):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = labels
    y_pos = np.arange(len(people))

    performance = values
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    plt.show()

def draw_bars(objects,performance,xlabel,ylabel,title):

    y_pos = np.arange(len(objects))

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show()



def draw_scattered(xvalues,yvalues,xlabel,ylabel,title):
    plt.scatter(xvalues,yvalues,marker='+')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()






if __name__ == "__main__":

    sc = SparkContext(appName = "Bank Customer Analysis")
    sqlContext = SQLContext(sc)

    df = sqlContext.read.format("jdbc").options(
    url ="jdbc:mysql://localhost/maindb",
    driver="com.mysql.jdbc.Driver",
    dbtable="bank",
    user="root"
    #password=""
    ).load()

    #df.printSchema()
    #countsByAge = df.groupBy("age").count()
    #countsByAge.show()
    #countsByAge.write.format("json").save("file:///usr/local/mysql/mysql-connector-java-5.0.8/db.json")
    total_entries = df.count()
    print '\ntotal no of entries: ' + str(total_entries)



    #AGES
    min_age = df.groupBy().min('age').collect()[0][0]
    max_age = df.groupBy().max('age').collect()[0][0]

    min_age_level = (min_age/10) * 10
    max_age_level = ((max_age/10)+1)*10

    age_attributes = []
    age_values = []

    for i in range(min_age_level,max_age_level,10):
        age_attributes.append(str(i)+'-'+str(i+10))
        age_values.append(df.filter((col('age') > i) & (col('age') <= i+10)).count())

    #draw_bars(age_attributes,age_values,'Age division','No of people','AGE')

    #print 'min age: '+str(min_age) + ', max age: '+str(max_age)
    #print 'average age: ' + str(df.groupBy().avg('age').collect()[0][0])



    #MARTIAL SATUS
    mart_attributes = ["single","married","divorced"]
    mart_values = []
    mart_perc = []

    for i in range(len(mart_attributes)):
        mart_values.append(df.filter(df.marital == mart_attributes[i]).count())
        mart_perc.append((mart_values[i]*100.0)/total_entries)




    #KIND OF JOB
    job_attributes = ["services","management","entrepreneur","blue-collar","admin.","technician","retired","unknown"]
    job_values = []
    for i in range(len(job_attributes)):
        job_values.append(df.filter(df.job == job_attributes[i]).count())
        #print job_attributes[i]+' : ' + str(job_values[i])



    #EDUCATION
    edu_attributes = ["primary","secondary","tertiary","unknown"]
    edu_values = []
    edu_perc = []
    for i in range(len(edu_attributes)):
        edu_values.append(df.filter(df.education == edu_attributes[i]).count())
        edu_perc.append((edu_values[i]*100.0)/total_entries)




    #CONTACT MODE
    contact_attributes = ["cellular","telephone","unknown"]
    contact_values = []
    contact_perc = []
    for i in range(len(contact_attributes)):
        contact_values.append(df.filter(df.contact == contact_attributes[i]).count())
        contact_perc.append((contact_values[i]*100.0)/total_entries)

    #AGE VS BALANCE (SCATTER PLOT)
    age_df = df.select('age').collect()
    balance_df = df.select('balance').collect()
    age_df = np.asarray(age_df)
    balance_df = np.asarray(balance_df)

    #AGE - HOUSING LOAN and PERSONAL LOAN
    loan_age_attributes = []
    housing_loan_age_values = []
    personal_loan_age_values = []
    for i in range(min_age_level,max_age_level,10):
        loan_age_attributes.append(str(i)+'-'+str(i+10))
        housing_loan_age_values.append(df.filter((col('age') > i) & (col('age') <= i+10) & (col('housing') == 'yes')).count())
        personal_loan_age_values.append(df.filter((col('age') > i) & (col('age') <= i+10) & (col('loan') == 'yes')).count())

    #JOB - HOUSING LOAN AND PERSONAL LOAN
    #job_attributes
    housing_loan_job_values = []
    personal_loan_job_values = []
    for i in range(len(job_attributes)):
        housing_loan_job_values.append(df.filter((col('housing') == 'yes')&(col('job') == job_attributes[i])).count())
        personal_loan_job_values.append(df.filter((col('loan') == 'yes')&(col('job') == job_attributes[i])).count())

    #PLOTTING GRAPHS
    print '\nplotting graphs ............'
    draw_pie_chart(mart_attributes,mart_perc,'MARTIAL STATUS')
    draw_hbars(job_attributes,job_values,'No of People','KIND OF JOB')
    draw_pie_chart(edu_attributes,edu_perc,'EDUCATION')
    draw_bars(age_attributes,age_values,'Age division','No of people','AGE')
    draw_pie_chart(contact_attributes,contact_perc,'CONTACT MODE')
    draw_scattered(age_df,balance_df,'age','balance','AGE VS BALANCE')
    draw_bar_chart_legend(loan_age_attributes,'Age division','No of People',housing_loan_age_values,personal_loan_age_values,('housing','personal'),'AGE vs LOAN')
    draw_bar_chart_legend(job_attributes,'Age division','No of People',housing_loan_job_values,personal_loan_job_values,('housing','personal'),'JOB vs LOAN')
    
