
import glob
import csv


filenames=glob.glob('*.csv')
fieldnames=['Nummer',"de","en"]
for filename in filenames:
    if filename.count('excel')>0:
        continue
    print(filename)
    zeilen=[]
    csvfile=open(filename,'r',newline='',encoding='utf8')
    reader=csv.DictReader(csvfile)
    for zeile in reader:
        zeilen.append(zeile)
    csvfile.close()

    
    
    csvfile=open(filename,'w',newline='',encoding='utf8')
    csvfile.write('sep=,\n')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for zeile in zeilen:
        writer.writerow(zeile)
    csvfile.close()

