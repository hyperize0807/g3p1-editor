import os, json
GAME=r"D:\DGGL\Games\G3P1103p_Win_260518"; PROJ=r"C:\Users\hyper\Projects\genesis3part1_editor"
raw=open(os.path.join(GAME,'dats','Abi.dat'),'rb').read()
def rd(p):
    d={}
    for ln in open(os.path.join(GAME,'G3Data',p),encoding='cp949'):
        ln=ln.rstrip('\r\n')
        if '\t' in ln:
            i,n=ln.split('\t',1)
            try:d[int(i)]=n
            except:pass
    return d
ABIL=rd('Abil.txt'); REC=39
mx={}; oob=[]; weird=[]
for id in sorted(ABIL):
    if id==0: continue
    o=(id-1)*REC+0x20
    if o<len(raw):
        v=raw[o]; mx[id]=v
        if v>15 or v==0: weird.append((id,v,ABIL[id]))
    else: oob.append(id)
from collections import Counter
print("extracted %d, OOB(>177)=%s"%(len(mx),oob))
print("value dist:",Counter(mx.values()).most_common())
print("weird(>15 or 0):",weird[:20])
# show the known ranges to confirm
print("\nid1-9:",[mx[i] for i in range(1,10)])
print("id10-22:",[mx[i] for i in range(10,23)])
print("id23-31:",[mx[i] for i in range(23,32)])
# save (only sane values 1..15)
clean={k:v for k,v in mx.items() if 1<=v<=15}
json.dump(clean,open(os.path.join(PROJ,'abil_max.json'),'w'))
with open(os.path.join(PROJ,'abil_max.txt'),'w',encoding='utf-8') as f:
    for id in sorted(clean): f.write("%3d  max=%d  %s\n"%(id,clean[id],ABIL[id]))
print("\nsaved abil_max.json (%d entries, sane only)"%len(clean))
