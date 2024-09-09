#!/usr/bin/python


import glob
import csv

filenames=glob.glob('*.xml')

for filename in filenames:
    if filename.endswith("_new.xml"):
        continue
    print(filename) 
    templatefile=open(filename+'.template')
    inhalt=templatefile.read()
    templatefile.close()
    
    csvfile=open(filename+'.csv',encoding="UTF-8")
    line1=csvfile.readline()
    if line1.startswith('Nummer;de;en'):
        deli=';'
        csvfile.seek(0)
    elif line1.startswith('Nummer,de,en'):
        deli=','
        csvfile.seek(0)
    elif line1.startswith('sep='):
        deli=line1[4]
    
    
    #encoding="ISO-8859-1")
    reader = csv.DictReader(csvfile, delimiter=deli)
    languages=[lang for lang in reader.fieldnames if lang!='Nummer']
    for row in reader:
        new_str="".join([f'<span lang="{lang}" class="multilang">{row[lang]}</span>' for lang in languages if row[lang]])
        inhalt=inhalt.replace(row['Nummer'],new_str)
    csvfile.close()

    newfile=open(filename[:-4]+'_new.xml','w',encoding='utf8')
    newfile.write(inhalt)
    newfile.close()
