#!/usr/bin/python


import glob
import csv
import re


filenames=glob.glob('*.xml')
ptn=r"""\[\[(?:validation|input|feedback):[a-zA-Z0-9_]*\]\]"""


def wrap(str,lang):
    return f'<span lang="{lang}" class="multilang">{str}</span>'

for filename in filenames:
    if filename.endswith("_new.xml"):
        continue
    print(filename) 
    templatefile=open(filename+'.template',newline='',encoding='utf8')
    inhalt=templatefile.read()
    templatefile.close()
    
    csvfile=open(filename+'.csv',newline='',encoding='utf8')
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

    error=False
    for row in reader:
        found_de=re.findall(ptn,row['de'])
        found_en=re.findall(ptn,row['en'])
        split_de=[wrap(i,"de") for i in re.split(ptn,row['de'])]
        split_en=[wrap(i,"en") for i in re.split(ptn,row['en'])]
        if found_de!=found_en or len(split_de)!=len(split_en):
            print(f"Fehler bei Nummer {row['Nummer']} : die [[validation:?]], [[input:?]], oder [[feedback:?]] passen nicht in beiden Übersetzungen zusammen")
            print("Abbruch!")
            error=True
            break
        print(len(found_de))
        found_de.append('')
        z=zip(found_de,split_de,split_en)        
        
        
        new_str="".join(f"{sd}{se}{f}" for f,sd,se in z)
        inhalt=inhalt.replace(row['Nummer'],new_str)
    if error:
        continue
    csvfile.close()

    newfile=open(filename[:-4]+'_new.xml','w',newline='',encoding='utf8')
    newfile.write(inhalt)
    newfile.close()
