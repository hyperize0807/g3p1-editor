# -*- coding: utf-8 -*-
"""나무위키 저장 HTML에서 직업 문서 텍스트 추출(구조 파악용)."""
import re, sys, html
sys.stdout.reconfigure(encoding='utf-8')
from html.parser import HTMLParser

SRC = r"C:\Users\hyper\Projects\genesis3part1_editor\samples\job\창세기전 3_직업 - 나무위키.html"
OUT = r"C:\Users\hyper\Projects\genesis3part1_editor\samples\job\extracted.txt"

BLOCK = {'div','p','li','ul','ol','h1','h2','h3','h4','h5','h6','br','tr','table','section'}
SKIP = {'script','style','noscript','svg','head'}

class TextX(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in SKIP: self.skip+=1
        if tag in BLOCK: self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in SKIP and self.skip>0: self.skip-=1
        if tag in BLOCK: self.parts.append('\n')
    def handle_data(self,data):
        if self.skip==0:
            t=data.strip()
            if t: self.parts.append(t+' ')

doc=open(SRC,encoding='utf-8',errors='replace').read()
p=TextX(); p.feed(doc)
text=''.join(p.parts)
text=re.sub(r'[ \t]+',' ',text)
text=re.sub(r'\n\s*\n+','\n',text)
open(OUT,'w',encoding='utf-8').write(text)
print("lines:",text.count('\n'),"chars:",len(text))
# 핵심 마커 위치 탐색
for kw in ['투르','팬드래건','게이시르','한 제국','기타 계열','무슬림','앙그라법전','시반 블레이드','성기사단']:
    idx=text.find(kw)
    print(f"  '{kw}': {'found@'+str(idx) if idx>=0 else 'NOT FOUND'}")
