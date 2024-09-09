#!/usr/bin/python

import glob
import csv
import os.path
import shutil
import sys
import json
from urllib import request, parse



class LibreTranslateAPI:
    DEFAULT_URL = "http://127.0.0.1:5000"

    def __init__(self, url=None, api_key=None):
        """Create a LibreTranslate API connection.

        Args:
            url (str): The url of the LibreTranslate endpoint.
            api_key (str): The API key.
        """
        self.url = LibreTranslateAPI.DEFAULT_URL if url is None else url
        self.api_key = api_key

        # Add trailing slash
        assert len(self.url) > 0
        if self.url[-1] != "/":
            self.url += "/"

    def translate(self, q, source="en", target="es"):
        """Translate string

        Args:
            q (str): The text to translate
            source (str): The source language code (ISO 639)
            target (str): The target language code (ISO 639)

        Returns:
            str: The translated text
        """
        url = self.url + "translate"
        params = {"q": q, "source": source, "target": target, "format":"html"}
        if self.api_key is not None:
            params["api_key"] = self.api_key
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req)
        response_str = response.read().decode()
        return json.loads(response_str)["translatedText"]

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
        {'i':1,'start':["<style","<script","[[jsxgraph"],'end':["</style>","</script>","/>","[[/jsxgraph]]"]},
        {'i':2,'start':["\\begin"],'end':["\\end"]},
        {'i':3,'start':["<"],'end':[">"]},
        # {'i':4,'start':["&"],'end':[";"]},
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
        if level>0 and cstyle!=0 and cstyle!=2 and (s[i]=='"' or s[i]=="'"):
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
                                out['s']=out['s']+f'<x id="{j}"></x>'
                                out[str(j)]=s[start:i]
                                j=j+1
                            special=True
                            break
        if not special and s[i]=='\\':
            if i<l-1:
                if not s[i+1].isalnum() or level!=0:
                    if level==0:
                        out[str(j)]=s[i]+s[i+1]
                        out['s']=out['s']+f'<x id="{j}"></x>'
                        j=j+1
                    i=i+2
                else:
                    start=i
                    i=i+1
                    while i+1<l and s[i+1].isalnum():
                        i=i+1
                    i=i+1
                    out['s']=out['s']+f'<x id="{j}"></x>'
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
        c = s.count(f'<x id="{i}"></x>')
        if c!=1:
            return ""
        s=s.replace(f'<x id="{i}"></x>',r[str(i)])
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

    
    csvfile=open(filename,encoding="UTF-8")
    line1=csvfile.readline()
    if line1.startswith('Nummer;de;en'):
        deli=';'
        csvfile.seek(0)
    elif line1.startswith('Nummer,de,en'):
        deli=','
        csvfile.seek(0)
    elif line1.startswith('sep='):
        deli=line1[4]
    else:
        deli=' '
        print("Delimiter konnte nicht bestimmt werden")
    
    
    #encoding="ISO-8859-1")
    reader = csv.DictReader(csvfile, delimiter=deli)
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
    print(f"Gesamtzahl {len(zeilen)}")
    for zeile in zeilen:
        if not zeile['en']:
            en=""
            sys.stdout.write(f" Nummer: {zeile['Nummer']}\r")
            sys.stdout.flush()
            o=rm_latex(zeile['de']);
        
            dbg=o
            de=o['s']
            if o['s']:
                o['s']=lt.translate(o['s'], "de", "en")
            en=readd_latex(o)
            if not en:
                o['s']='Translation Error\n'+de
                en=readd_latex(o)
                print(f"Fehler bei der Übersetzung von Nummer: {zeile['Nummer']}")
                
            zeile['en']=en
        writer.writerow(zeile)
    csvfile.close()

    shutil.copy(filename+".progress",filename)    
    
