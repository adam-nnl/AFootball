import sys
import fileinput
import csv

filename = raw_input("What file to convert?: ")
copy  = open("tanh_convert-" + filename, "wb")
writer = csv.writer(copy, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
with open(filename, "rU") as f:
    reader = csv.reader(f, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
    head=reader.next()
    writer.writerow(head)
    for row in reader:
        if len(row)>3:
            writer.writerow(row)
        elif row[0]=="1":
            writer.writerow(["1","-1"])
        elif row[0]=="0":
            writer.writerow(["-1","1"])
f.close()
copy.close()        

