#!/usr/bin/python

import glob
#import xml.etree.ElementTree as ET
from lxml import etree as ET
from bs4 import BeautifulSoup
import csv
from bs4.formatter import HTMLFormatter
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
        {'i':1,'start':["<"],'end':[">"]},
        {'i':2,'start':["&"],'end':[";"]},
        {'i':3,'start':["{","[["],'end':["}","]]"]}
    ]
    out={'s':"",'count':0}
    while True:
        if i>=l:
            if level>0:
                print("Fehler bei Übersetzung")
                return {'s':"",'count':0}
            out['count']=j
            return out
        special=False
        if level>0 and (s[i]=='"' or s[i]=="'"):
            if len(brackets)==0:
                brackets=s[i]
            elif s[i]==brackets:
                brackets=''
        if len(brackets)==0:
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
        if s.count(f" [X{i}] ")==0:
            print("Fehler bei Übersetzung")
            return ""
        s=s.replace(f" [X{i}] ",r[str(i)])
    return s

class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == 'm':
                continue
            yield k, v

filenames=glob.glob('*.xml')
for filename in filenames:
    tree = ET.parse(filename)
    root = tree.getroot()
    texte=root.findall('.//*[@format="html"]/text')
    
    category=root.find('.//question[@type="category"]/category/text').text
    

    languages=set()
    languages.add('de')
    languages.add('en')
    groups=[]
    texts=[]
    infile=open(filename)
    inhalt=infile.read()
    infile.close()

    inhalt.replace(category,category+"/übersetzt")
    inhalt.replace('<quiz>',f"""<quiz>
<!-- question: 0  -->
  <question type="category">
    <category>
      <text>{category}</text>
    </category>
    <info format="moodle_auto_format">
      <text></text>
    </info>
    <idnumber></idnumber>
  </question>""",1)
    
    number=0
    for text in texte:
        if text.text:
            orig=text.text
            number+=1
            inhalt=inhalt.replace(orig,"###"+str(number)+"###")
            text.text='<span class="multilang" lang="de">'+orig+'</span>'
            soup = BeautifulSoup(text.text,'html.parser')
            spans = soup.findAll("span",{"class":"multilang"})
            group=[]
            for span in spans:
                languages.add(span['lang'])
                group.append(span)
                try:
                    nexttag_name=span.find_next_sibling().name
                except:
                    nexttag_name=""
            if group:
                groups.append(group)
                texts.append(orig)
                group=[]

    csvfile=open(filename+'.csv','w',newline='',encoding='utf8')
    fieldnames=['Nummer']+list(languages)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    # print(lt.translate("LibreTranslate is awesome!", "en", "de")) 
    # print(lt.translate("Øving", "no", "de")) 

    nummer=0
    for group in groups:
        number+=1
        zeile={'de':texts[number-1]}
        zeile['Nummer']='###'+str(number)+'###'
        o=rm_latex(zeile['de']);
        o['s']=lt.translate(o['s'], "de", "en")
        zeile['en']=readd_latex(o)
        writer.writerow(zeile)
    csvfile.close()

    templatefile=open(filename+'.template','w',encoding='utf8')
    templatefile.write(inhalt)
    templatefile.close()
