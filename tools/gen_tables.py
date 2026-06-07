# -*- coding: utf-8 -*-
# tools/G3Data/*.txt -> tools/tables.json  (이름 테이블: 아이템/캐릭터/직업/소속/초상화/능력)
import os, json
PROJ = os.path.dirname(os.path.abspath(__file__))  # tools/

def rd(fn):
    d = {}
    for ln in open(os.path.join(PROJ, 'G3Data', fn), encoding='cp949'):
        ln = ln.rstrip('\r\n')
        if '\t' in ln:
            i, n = ln.split('\t', 1)
            try:
                d[int(i)] = n
            except ValueError:
                pass
    return d

tables = {f.split('.')[0]: rd(f) for f in
          ['Char.txt', 'Item.txt', 'Abil.txt', 'Job.txt', 'Group.txt',
           'AtType.txt', 'Face_Stat.txt', 'Face_Msg.txt']}
out = os.path.join(PROJ, 'tables.json')
open(out, 'w', encoding='utf-8').write(json.dumps(tables, ensure_ascii=False))
for k, v in tables.items():
    print("%-10s %d entries" % (k, len(v)))
print("->", out)
