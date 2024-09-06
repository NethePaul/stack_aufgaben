#!/usr/bin/python


import glob

filenames=glob.glob('*.xml.template')

for filename in filenames:
    print(filename)
    with open(filename) as f:
        s=f.read()
    with open(filename,'w') as f:
        s=s.replace('<text>###','<text><![CDATA[###')
        s=s.replace('###</text>','###]]></text>')
        f.write(s)
