
"""
    removes latex, maxima, and html from a string from a stack question text
"""
def rm_latex(s):
    l=len(s)
    i=0
    j=0
    start=0
    if l <= 0:
        return {'s':s, 'num':0}
    level=0
    cstyle=0
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
                print("error: improperly braced")
                out['s']=out['s']+s[start:i]
            out['count']=j
            return out
        print(s[i])
        special=False
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
                    print("level up")
                    break
            if level>0 and not special:
                for st in style['end']:
                    print(st)
                    if special:
                        break
                    if s[i:].startswith(st):
                        print("found end")
                        level=level-1
                        i=i+len(st)
                        if level == 0:
                            print("level 0")
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
                
                    
