#!/usr/bin/python

import glob
#import xml.etree.ElementTree as ET
from lxml import etree as ET
from bs4 import BeautifulSoup
import csv
from bs4.formatter import HTMLFormatter
import os.path;

class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == 'm':
                continue
            yield k, v

filenames=glob.glob('*.xml')
fieldnames=["Nummer","de","en"]

for filename in filenames:
    if filename.endswith("_new.xml"):
        continue
    print(filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    texte=root.findall('.//*[@format="html"]/text')

    groups=[]
    texts=[]
    infile=open(filename,encoding='utf8')
    inhalt=infile.read()
    infile.close()

    categories=[i.text for i in root.findall('.//question[@type="category"]/category/text')]
    category=os.path.commonpath(categories)
    print(f"Neue Fragen stehen unter: {category}/überstzt")
    
    inhalt=inhalt.replace(category,category+"/übersetzt")
    inhalt=inhalt.replace('<quiz>',f"""<quiz>
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

            if orig not in inhalt:
                print(f"Potentieller Fehler bei Nummer: ###{number+1}###")
                # print(orig)
                # print("")
                continue
            else:
                number+=1
                inhalt=inhalt.replace(orig,"###"+str(number)+"###",1)
            text.text='<span class="multilang" lang="de">'+orig+'</span>'
            soup = BeautifulSoup(text.text,'html.parser')
            spans = soup.findAll("span",{"class":"multilang"})
            group=[]
            for span in spans:
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
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    number=0
    for group in groups:
        number+=1
        zeile={'de':texts[number-1]}
        zeile['Nummer']='###'+str(number)+'###'
        writer.writerow(zeile)
    csvfile.close()

    templatefile=open(filename+'.template','w',encoding='utf8')
    templatefile.write(inhalt)
    templatefile.close()
