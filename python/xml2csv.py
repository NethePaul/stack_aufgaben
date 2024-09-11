#!/usr/bin/python

import glob
#import xml.etree.ElementTree as ET
from lxml import etree as ET
from bs4 import BeautifulSoup
import csv
from bs4.formatter import HTMLFormatter


class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            if k == 'm':
                continue
            yield k, v

filenames=glob.glob('*.xml')
fieldnames=["Nummer","de","en"]

for filename in filenames:
    tree = ET.parse(filename)
    root = tree.getroot()
    texte=root.findall('.//*[@format="html"]/text')

    groups=[]
    texts=[]
    infile=open(filename,newline='',encoding='utf8')
    inhalt=infile.read()
    infile.close()

    category=root.find('.//question[@type="category"]/category/text').text
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
