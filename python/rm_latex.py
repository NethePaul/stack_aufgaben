
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
