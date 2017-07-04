from dateutil.parser import *
from dateutil.tz import *

dates = ('7-10-1996','1996-10-7','1996-7-10','7-1996-10','10-7-1996','7 october 1996',
         'october 7,1996','7.10.1996','10.7.1996','7/10/1996','10/7/1996','1996/7/10','7/10/1996')

#a = parse()
#a.day,a.month,a.year

for x in dates:
    try:
        print 'parsed '+x+ ' into: ' +str(parse(x))
    except:
        print '\t\t\t\t\t\t\terror parsing '+str(x)

