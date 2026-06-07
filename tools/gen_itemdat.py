# -*- coding: utf-8 -*-
# dats/Item.dat -> tools/item_info.json  (아이템 한글명/영문명/설명 추출)
# Item.dat: XOR 0xFF 난독화(텍스트), 204바이트 고정 레코드, record(id)=(id-1)*204 (id 1=단검..).
#   +0x02 한글 이름(CP949), +0x20 영문 이름(ASCII), +0x69 부근 한글 설명(CP949,null종료).
import json, os, struct

GAME = r"D:\DGGL\Games\G3P1103p_Win_260518"      # 게임 설치 경로
PROJ = os.path.dirname(os.path.abspath(__file__))  # tools/
REC = 204

def load(p):  # XOR 0xFF 디코드
    return bytes(b ^ 0xFF for b in open(p, "rb").read())

NAME_OFF, ENG_OFF, DESC_OFF = 0x02, 0x20, 0x6A   # 레코드 내 고정 필드 오프셋

def cstr(d, o, mx=96):
    e = o
    while e < o + mx and e < len(d) and d[e] != 0:
        e += 1
    try:
        return d[o:e].decode("cp949").strip()
    except Exception:
        return ""

def main():
    d = load(os.path.join(GAME, "dats", "Item.dat"))
    n = len(d) // REC
    info = {}
    for r in range(n):
        b = r * REC
        item_id = r + 1                      # record index 0 = item id 1
        name = cstr(d, b + NAME_OFF)
        eng = cstr(d, b + ENG_OFF)
        desc = cstr(d, b + DESC_OFF)         # 설명: 고정 오프셋 +0x6A (null 종료 CP949)
        # 설명이 이름과 동일/포함뿐이면(짧은 잡음) 비워둠
        entry = {"name": name, "eng": eng}
        if desc and desc != name:
            entry["desc"] = desc
        info[item_id] = entry
    # id 0 = 없음
    info[0] = {"name": "없음", "eng": ""}
    out = os.path.join(PROJ, "item_info.json")
    json.dump(info, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    have = sum(1 for v in info.values() if v.get("desc"))
    print("records=%d, item_info entries=%d, with desc=%d -> %s" % (n, len(info), have, out))
    # 검증 샘플
    for sid in (1, 25, 126, 127, 106):
        v = info.get(sid, {})
        print("  id%-3d %-14s | %s" % (sid, v.get("name", ""), v.get("desc", "(설명없음)")))

if __name__ == "__main__":
    main()
