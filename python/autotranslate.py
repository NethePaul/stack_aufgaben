#!/usr/bin/python

import glob
import csv
import os.path
import shutil
import sys
from libretranslatepy import LibreTranslateAPI


"""
    entfernt latex, maxima, und html von den Text von einer Stack Frage
    sodass es automatisch übersetzbar ist
"""
def rm_latex(s):
    l=len(s)
    i=0
    j=0
    start=0
    if l <= 0:
        return {'s':s, 'count':0}
    level=0
    cstyle=0
    brackets=''
    styles=[
        {'i':0,'start':["\\(","\\["],'end':["\\)","\\]"]},
        {'i':1,'start':["<style>","<script>"],'end':["</style>","</script>"]},
        {'i':2,'start':["<"],'end':[">"]},
        {'i':3,'start':["&"],'end':[";"]},
        {'i':4,'start':["{","[["],'end':["}","]]"]}
    ]
    out={'s':"",'count':0}
    while True:
        if i>=l:
            if level>0:
                return {'s':"",'count':0}
            out['count']=j
            return out
        special=False
        if level>0 and (s[i]=='"' or s[i]=="'"):
            if not brackets:
                brackets=s[i]
            elif s[i]==brackets:
                brackets=''
        if not brackets:
            for style in styles if level==0 else [styles[cstyle]]:
                for st in style['start']:
                    if special:
                        break
                    if s[i:].startswith(st):
                        if level == 0:
                            start=i
                            cstyle=style['i']
                        i=i+len(st)
                        level=level+1
                        special=True
                        break
                if level>0 and not special:
                    for st in style['end']:
                        if special:
                            break
                        if s[i:].startswith(st):
                            level=level-1
                            i=i+len(st)
                            if level == 0:
                                out['s']=out['s']+f" [X{j}] "
                                out[str(j)]=s[start:i]
                                j=j+1
                            special=True
                            break
        if not special and s[i]=='\\':
            if i<l-1:
                if not s[i+1].isalnum() or level!=0:
                    if level==0:
                        out['s']=out['s']+s[i]+s[i+1]
                    i=i+2
                else:
                    start=i
                    i=i+1
                    while i+1<l and s[i+1].isalnum():
                        i=i+1
                    i=i+1
                    out['s']=out['s']+f" [X{j}] "
                    out[str(j)]=s[start:i]
                    j=j+1
        elif not special and level==0:
            out['s']=out['s']+s[i]
            i=i+1
        elif not special:
            i=i+1          


def readd_latex(r):
    s=r['s']
    if r['count']==0:
        return s
    for i in range(r['count']):
        if s.count(f"[X{i}]")==0:
            return ""
        s=s.replace(f"[X{i}]",r[str(i)])
    return s


lt = LibreTranslateAPI("http://127.0.0.1:5000")
filenames=glob.glob('*.csv')
fieldnames=['Nummer',"de","en"]
for filename in filenames:
    zeilen=[]
    if os.path.isfile(filename+".progress"):
        csvfile=open(filename+".progress",'r',newline='',encoding='utf8')
        reader=csv.DictReader(csvfile)
        for zeile in reader:
            zeilen.append(zeile)
        csvfile.close()

    csvfile=open(filename,'r',newline='',encoding='utf8')
    reader=csv.DictReader(csvfile)
    i=len(zeilen)
    for zeile in reader:
        if i>0:
            i=i-1
            continue
        zeilen.append(zeile)
    csvfile.close()

    
    
    csvfile=open(filename+".progress",'w',newline='',encoding='utf8')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # print(lt.translate("LibreTranslate is awesome!", "en", "de")) 
    # print(lt.translate("Øving", "no", "de"))

    for zeile in zeilen:
        if not zeile['en']:
            o=rm_latex(zeile['de']);
            if o['s']:
                o['s']=lt.translate(o['s'], "de", "en")
            en=readd_latex(o)
            if not en:
                print(f"Fehler bei der Übersetzung von Nummer: {zeile['Nummer']}")
                en='Translation Error'
            else:
                sys.stdout.write(f" Nummer: {zeile['Nummer']}\r")
                sys.stdout.flush()
            zeile['en']=en
        writer.writerow(zeile)
    csvfile.close()

    shutil.copy(filename+".progress",filename)    
    
