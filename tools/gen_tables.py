import os, json, struct
GAME=r"D:\DGGL\Games\G3P1103p_Win_260518"
PROJ=r"C:\Users\hyper\Projects\genesis3part1_editor"
def rd(p):
    d={}
    for ln in open(os.path.join(PROJ,'G3Data',p),encoding='cp949'):
        ln=ln.rstrip('\r\n')
        if '\t' in ln:
            i,n=ln.split('\t',1)
            try: d[int(i)]=n
            except: pass
    return d
tables={f.split('.')[0]:rd(f) for f in
  ['Char.txt','Item.txt','Abil.txt','Job.txt','Group.txt','AtType.txt','Face_Stat.txt','Face_Msg.txt']}
open(os.path.join(PROJ,'tables.json'),'w',encoding='utf-8').write(json.dumps(tables,ensure_ascii=False))
for k,v in tables.items(): print("%-10s %d entries"%(k,len(v)))

# verify block structure
MARK=bytes([0x30,0x3A,0x10,0x10]); REC=0x154
def load(p): return bytes(b^0xFF for b in open(p,'rb').read())
def records(buf):
    recs=[]; i=buf.find(MARK)
    while i!=-1 and i+REC<=len(buf): recs.append(buf[i:i+REC]); i=buf.find(MARK,i+1)
    return recs
def name(r):
    seg=r[6:6+24]; z=seg.find(b'\x00'); seg=seg[:z] if z!=-1 else seg
    return seg.decode('cp949','replace')
recs=records(load(os.path.join(GAME,'G30004.sav')))
def cid(r): return struct.unpack_from('<H',r,0x44)[0]
print("\nTotal records:",len(recs))
# Are blocks [0:106],[106:212],[212:318] same char sequence?
b0=[cid(r) for r in recs[0:106]]; b1=[cid(r) for r in recs[106:212]]; b2=[cid(r) for r in recs[212:318]]
print("block0==block1 charIDs:", b0==b1, "| block0==block2:", b0==b2)
print("first marker offset, last:", buf if False else (hex(load(os.path.join(GAME,'G30004.sav')).find(MARK))))
# what is between header(0) and first record, and after last record?
buf=load(os.path.join(GAME,'G30004.sav'))
print("file size", len(buf), "first rec @", hex(buf.find(MARK)), "last rec end @", hex(0x40C+318*REC))
