
import glob
import csv


filenames=glob.glob('*.csv')
fieldnames=['Nummer',"de","en"]
for filename in filenames:
    if filename.count('excel')>0:
        continue
    print(filename)
    zeilen=[]
    csvfile=open(filename,'r',encoding="UTF-8",newline='')
    line1=csvfile.readline()
    if line1.startswith('Nummer;de;en'):
        deli=';'
        csvfile.seek(0)
    elif line1.startswith('Nummer,de,en'):
        deli=','
        csvfile.seek(0)
    elif line1.startswith('sep='):
        csvfile.close()
        continue
    else:
        print("Fehler beim Lesen der .csv Datei")
    reader=csv.DictReader(csvfile)

    for zeile in reader:
        zeilen.append(zeile)
    csvfile.close()

    
    
    csvfile=open(filename,'w',newline='',encoding='utf8')
    csvfile.write(f'sep={deli}\n')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for zeile in zeilen:
        writer.writerow(zeile)
    csvfile.close()

