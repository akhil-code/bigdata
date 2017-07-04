bar chart: Ages(int -single)
barchart: Job (discrete-single)
piechart: Martial status (discrete-single)
piechart:Education(discrete-single)
pie chart:contact mode(discrete-single)

scatter plots: age vs balance(int vs int-double)
bar chart multiple: age - housing loan and personal loan(int vs discrete,discrete-triple)
bar chart multiple:job - housing loan and personal loan(discrete vs discrete,discrete-triple)
asdfas
single:
int: pie chart,bar chart,histogram
discrete:pie chart,bar chart

double:
int,int: scatter plots
int,boolean:bar chart
discrete,boolean:bar chart


triple:
int,boolean,boolean:bar chart multiple
discrete,boolean,boolean:bar chart multiple

date:
int vs date: line chart(continuos time line)
double vs date: line chart(continuos time line)

int vs date: bar chart(monthly)

bool vs date: line chart(convert bool to int)(continuos timeline)
bool vs date: bar chart(monthly)



*int vs discrete
*bar chart horizontal
*dates data type

ALTER TABLE `the_table` ADD `new_field` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST; 
