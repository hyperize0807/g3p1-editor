# -*- coding: utf-8 -*-
# 에디터 빌더: tools/tables.json + tools/abil_max.json 을 index.html(dist/)에 내장하여 생성.
import json, os
PROJ = os.path.dirname(os.path.abspath(__file__))            # tools/
ROOT = os.path.dirname(PROJ)                                  # 저장소 루트
DIST = os.path.join(ROOT, 'dist'); os.makedirs(DIST, exist_ok=True)
tables = open(os.path.join(PROJ, 'tables.json'), encoding='utf-8').read()
abil_max = open(os.path.join(PROJ, 'abil_max.json'), encoding='utf-8').read()

HTML = r'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>창세기전3 파트1 세이브 에디터 (MVP)</title>
<style>
  :root{--bg:#1a1c22;--panel:#23262e;--panel2:#2b2f3a;--line:#3a3f4b;--fg:#e6e8ee;--mut:#9aa0ad;--acc:#6ea8fe;--ok:#5ed18b;--warn:#e6b65c}
  *{box-sizing:border-box}
  body{margin:0;font:14px/1.5 "Segoe UI",Malgun Gothic,sans-serif;background:var(--bg);color:var(--fg)}
  header{padding:10px 16px;background:var(--panel);border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:center;flex-wrap:wrap}
  header h1{font-size:15px;margin:0;font-weight:600}
  .badge{font-size:11px;color:#0b0d12;background:var(--warn);border-radius:4px;padding:1px 6px;font-weight:700}
  button{background:var(--panel2);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:6px 12px;cursor:pointer}
  button:hover{border-color:var(--acc)}
  button.primary{background:var(--acc);color:#0b0d12;border-color:var(--acc);font-weight:600}
  button:disabled{opacity:.4;cursor:not-allowed}
  #drop{margin:8px 16px;padding:30px;border:2px dashed var(--line);border-radius:10px;text-align:center;color:var(--mut)}
  #drop.hl{border-color:var(--acc);color:var(--fg)}
  #globalbar{background:var(--panel);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}
  #globalbar .gtitle{color:var(--acc);font-weight:600;font-size:13px}
  #globalbar .gfld{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--mut)}
  #globalbar .gfld input{width:120px}
  #globalbar .gtitle{color:var(--ok)}
  .gold-more{margin-left:auto}
  .gold-more>summary{cursor:pointer;color:var(--warn);font-size:12px;list-style:none}
  .gold-more>summary::-webkit-details-marker{display:none}
  .gold-more>summary:before{content:'▸ '}
  .gold-more[open]>summary:before{content:'▾ '}
  .gold-more[open]{background:#241818;border:1px solid #6b3a3a;border-radius:6px;padding:8px 10px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;width:100%;margin-top:8px}
  .gold-more .gwarn{color:#e6b6b6;font-size:12px;flex-basis:100%}
  main{display:none;grid-template-columns:320px 1fr;height:calc(100vh - 53px - 49px)}
  #list{border-right:1px solid var(--line);overflow:auto;background:var(--panel)}
  #search{width:100%;padding:8px 10px;border:0;border-bottom:1px solid var(--line);background:var(--panel2);color:var(--fg);position:sticky;top:0}
  .row{padding:6px 12px;border-bottom:1px solid #2c303a;cursor:pointer;display:flex;justify-content:space-between;gap:8px}
  .row:hover{background:var(--panel2)}
  .row.sel{background:#33405e}
  .row .nm{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .row .meta{color:var(--mut);font-size:11px;flex:none}
  #edit{overflow:auto;padding:16px 22px}
  .grp{margin-bottom:20px}
  .grp h3{font-size:13px;color:var(--acc);border-bottom:1px solid var(--line);padding-bottom:5px;margin:0 0 10px;display:flex;gap:8px;align-items:center}
  .tag{font-size:10px;padding:1px 5px;border-radius:3px}
  .tag.ok{background:#1e3d2c;color:var(--ok)}
  .tag.guess{background:#3d361e;color:var(--warn)}
  .fld{display:grid;grid-template-columns:150px 1fr;gap:10px;align-items:center;margin-bottom:7px}
  .fld label{color:var(--mut)}
  .fld .off{color:#666;font-size:11px}
  input[type=number],input[type=text],select{background:var(--panel2);color:var(--fg);border:1px solid var(--line);border-radius:5px;padding:5px 7px;width:100%}
  input[readonly]{color:var(--mut)}
  .combo-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
  .combo-grid .fld{grid-template-columns:34px 1fr;margin:0}
  table.raw{border-collapse:collapse;font-family:Consolas,monospace;font-size:12px;width:100%}
  table.raw td{border:1px solid #333;padding:2px 4px;text-align:center}
  table.raw td.o{color:var(--mut);background:#202329}
  table.raw input{padding:2px;text-align:center;border:0;background:transparent;color:var(--fg);width:46px}
  details summary{cursor:pointer;color:var(--acc);margin:6px 0}
  .hex{font-family:Consolas,monospace;font-size:11px;color:var(--mut);white-space:pre;overflow:auto;background:#181a1f;padding:8px;border-radius:6px}
  .hint{color:var(--mut);font-size:12px}
  .applyall{display:flex;gap:6px;align-items:center;color:var(--mut);font-size:12px}
  #modal{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:50;align-items:flex-start;justify-content:center}
  #modal .box{background:var(--panel);border:1px solid var(--line);border-radius:10px;margin-top:40px;width:760px;max-width:94vw;max-height:86vh;overflow:auto;padding:18px 22px}
  #modal h2{margin:0 0 4px;font-size:16px}
  .zone-safe{border:1px solid #2f6b45;border-radius:8px;padding:6px 12px 12px;margin:10px 0;background:#16241c}
  .zone-h{color:var(--ok);font-weight:600;font-size:13px;margin:8px 0}
  .zone-danger{border:1px solid #6b3a3a;border-radius:8px;margin:14px 0;background:#241818}
  .zone-danger>summary{cursor:pointer;color:var(--warn);font-weight:600;padding:10px 12px;list-style:none}
  .zone-danger>summary::-webkit-details-marker{display:none}
  .zone-danger>summary:before{content:'▸ ';}
  .zone-danger[open]>summary:before{content:'▾ ';}
  .zone-danger>*:not(summary){margin-left:12px;margin-right:12px}
  .danger-warn{background:#2e1d1d;border:1px solid #6b3a3a;border-radius:6px;padding:10px;color:#e6b6b6;font-size:12px;line-height:1.7;margin:4px 12px 10px}
  .invtbl{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:12px 0;background:var(--panel2)}
  .invtbl.cur{border-color:var(--ok)}
  .invtbl .ih{display:flex;justify-content:space-between;align-items:center;color:var(--acc);font-size:13px;margin-bottom:8px}
  .invrow{display:grid;grid-template-columns:1fr 90px 32px;gap:8px;margin-bottom:5px}
  .invrow .del{background:#3a2326;border-color:#5a3338}
  .smallbtn{font-size:12px;padding:3px 8px}
</style>
</head>
<body>
<header>
  <h1>창세기전3 파트1 세이브 에디터</h1><span class="badge">MVP</span>
  <input type="file" id="file" accept=".sav" style="display:none">
  <button id="open">📂 .sav 열기</button>
  <button id="invbtn" disabled>🎒 보관함 편집</button>
  <button id="save" class="primary" disabled>💾 저장(다운로드)</button>
  <span id="fname" class="hint"></span>
  <span class="applyall" style="margin-left:auto"><input type="checkbox" id="applyall" checked> 모든 에피소드 블록에 적용(권장)</span>
</header>
<div id="drop">여기에 <b>.sav</b> 파일을 끌어다 놓거나 "열기"를 누르세요.<br><span class="hint">파일은 브라우저 안에서만 처리되며 어디에도 업로드되지 않습니다.</span></div>
<div id="globalbar" style="display:none"></div>
<div id="modal"><div class="box">
  <h2>🎒 보관함 편집</h2>
  <p class="hint">세이브에서 자동 탐지한 아이템 보관함 목록입니다. 아이템 구성을 보고 본인의 에피소드(시반슈미터/크림슨크루세이더/아포칼립스) 보관함을 찾으세요. 같은 내용의 사본은 함께 수정되어 게임에 반영됩니다. 수량/아이템을 바꾸고 닫은 뒤 "저장"을 누르세요. (게임 내부 고정 목록이 함께 보일 수 있으니 내용으로 구분하세요.)</p>
  <div id="invlist"></div>
  <div style="text-align:right;margin-top:12px"><button id="invclose" class="primary">닫기</button></div>
</div></div>
<main>
  <div id="list"><input id="search" placeholder="이름/번호 검색…"><div id="rows"></div></div>
  <div id="edit"><p class="hint">왼쪽에서 캐릭터를 선택하세요.</p></div>
</main>

<script>
const TABLES = __TABLES__;
const ABIL_MAX = __ABILMAX__;   // 어빌리티별 최대 레벨 (Abi.dat record+0x20). 없으면 기본 9.
const abilMax = id => (ABIL_MAX[id] || 9);
const MARK=[0x30,0x3A,0x10,0x10], REC=0x154;
let buf=null, fileName="G3.sav", records=[], cur=-1, period=0;
const dec949 = new TextDecoder('euc-kr');

const u16=(o)=>buf[o]|(buf[o+1]<<8);
const setu16=(o,v)=>{buf[o]=v&0xFF;buf[o+1]=(v>>8)&0xFF};
const u32=(o)=>(buf[o]|(buf[o+1]<<8)|(buf[o+2]<<16)|(buf[o+3]<<24))>>>0;
const setu32=(o,v)=>{buf[o]=v&0xFF;buf[o+1]=(v>>8)&0xFF;buf[o+2]=(v>>16)&0xFF;buf[o+3]=(v>>24)&0xFF};
function cstr949(o,max){let e=o;while(e<o+max&&buf[e]!==0)e++;return dec949.decode(buf.slice(o,e));}

const F={charId:0x44,faceMsg:0x46,faceStat:0x48,group:0x4A,job:0x4B,exp:0x58,hp:0x7C,combo:0x6A,
  str:0x60,skill:0x61,dex:0x62,int:0x63,luck:0x64,spd:0x65,ac:0x66,mr:0x67,wtp:0x68,
  weap1:0x82,weap2:0x84,armor:0x86,acc1:0x88,acc2:0x8A,abil:0x8C};
// 어빌리티: 레코드 +0x8C부터 200바이트 배열, 인덱스=Abil.txt ID, 0xFF=미보유, 1+=레벨
const ABIL_NONE=0xFF;  // 미보유 마커
const STATS=[["Str","str"],["Skill","skill"],["Dex","dex"],["Int","int"],["Luck","luck"],["Spd","spd"],["Ac","ac"],["Mr","mr"],["Wtp","wtp"]];
// 소지금: 표준 318레코드 세이브 기준 절대 오프셋의 u32 4개 (에피소드별)
// 소지금: u32×4 @0x13B58. 에피소드→슬롯 매핑은 정답값으로 확정(ep0→0, ep1→1, ep2→3). slot2는 비표시 예비 슬롯.
const GOLD=[{label:'시반슈미터',off:0x13B58,ep:0},{label:'크림슨크루세이더',off:0x13B5C,ep:1},
  {label:'예비 슬롯(비표시·추정)',off:0x13B60,ep:null},{label:'아포칼립스',off:0x13B64,ep:2}];

function parse(){
  records=[];
  for(let i=0;i+REC<=buf.length;){
    if(buf[i]===MARK[0]&&buf[i+1]===MARK[1]&&buf[i+2]===MARK[2]&&buf[i+3]===MARK[3]){
      records.push(i); i+=1;
    } else i++;
  }
  computePeriod();
}
function recName(off){return cstr949(off+6,24)||("#"+u16(off+F.charId));}
// 로스터 반복 주기(=블록 크기). 같은 (charId,이름) 시퀀스가 주기적으로 반복됨. 못 찾으면 전체.
function computePeriod(){
  const n=records.length; period=n;
  if(!n)return;
  const ks=records.map(r=>u16(r+F.charId)+':'+recName(r));
  for(let P=1;P<=n>>1;P++){ if(n%P)continue; let ok=true;
    for(let i=P;i<n;i++){ if(ks[i]!==ks[i-P]){ok=false;break;} }
    if(ok){period=P;return;} }
}
// 현재 선택 캐릭터와 같은 슬롯(모든 블록)의 레코드 오프셋들
function slotRecords(){
  if(period>0 && period<records.length){
    const t=[]; for(let idx=cur%period; idx<records.length; idx+=period) t.push(records[idx]); return t;
  }
  return [records[cur]];
}

function renderList(filter=""){
  const rows=document.getElementById('rows'); rows.innerHTML="";
  const blocks = (period>0 && period<records.length) ? Math.round(records.length/period) : 1;
  const shown = (period>0 && period<records.length) ? period : records.length;  // 첫 블록만(중복 제거)
  for(let idx=0;idx<shown;idx++){
    const off=records[idx], nm=recName(off), cid=u16(off+F.charId);
    const hay=(nm+" "+cid+" "+idx).toLowerCase();
    if(filter && !hay.includes(filter)) continue;
    const d=document.createElement('div');
    d.className='row'+(idx===cur?' sel':'');
    d.innerHTML='<span class="nm">'+nm+'</span><span class="meta">#'+cid+(blocks>1?' ·×'+blocks:'')+'</span>';
    d.onclick=()=>{cur=idx;renderList(filter);renderEdit();};
    rows.appendChild(d);
  }
}

function opt(table,val){
  const t=TABLES[table]||{};
  let s='<option value="'+val+'">'+val+' — '+(t[val]!==undefined?t[val]:'(미정의)')+'</option>';
  s+=Object.keys(t).map(Number).sort((a,b)=>a-b).map(k=>'<option value="'+k+'">'+k+' — '+t[k]+'</option>').join("");
  return s;
}
function selField(label,off,table,size){
  const v= size===1? buf[off] : u16(off);
  return '<div class="fld"><label>'+label+' <span class="off">@0x'+off.toString(16)+'</span></label>'+
   '<select data-off="'+off+'" data-size="'+(size||2)+'" data-kind="sel">'+opt(table,v)+'</select></div>';
}
function numField(label,off,size,kind){
  const v= kind==='u32'? u32(off) : size===1? buf[off] : u16(off);
  return '<div class="fld"><label>'+label+' <span class="off">@0x'+off.toString(16)+'</span></label>'+
   '<input type="number" data-off="'+off+'" data-size="'+(size||2)+'" data-kind="'+(kind||'int')+'" value="'+v+'"></div>';
}

function renderEdit(){
  if(cur<0)return;
  const off=records[cur];
  const e=document.getElementById('edit');
  let statg="";
  for(const [lab,key] of STATS){
    statg+='<div class="fld"><label>'+lab+'</label>'+
     '<input type="number" min="0" max="255" data-off="'+(off+F[key])+'" data-size="1" data-kind="int" value="'+buf[off+F[key]]+'"></div>';
  }
  let raw="<table class='raw'><tr><td class='o'>off</td>";
  for(let c=0;c<8;c++) raw+="<td class='o'>+"+(c*2)+"</td>"; raw+="</tr>";
  for(let base=0x44;base<REC;base+=16){
    raw+="<tr><td class='o'>0x"+base.toString(16)+"</td>";
    for(let c=0;c<8;c++){const o=base+c*2; raw+= (o+1<REC)? "<td><input type='number' data-off='"+(off+o)+"' data-size='2' data-kind='int' value='"+u16(off+o)+"'></td>":"<td></td>";}
    raw+="</tr>";
  }
  raw+="</table>";
  let hex="";
  for(let r=0;r<REC;r+=16){
    let line=("000"+r.toString(16)).slice(-3)+"  ";
    for(let c=0;c<16&&r+c<REC;c++) line+=("0"+buf[off+r+c].toString(16)).slice(-2)+" ";
    hex+=line+"\n";
  }
  // 어빌리티: 보유(=값!=0xFF) 목록 + 미보유 추가 드롭다운
  const abase=off+F.abil, alen=REC-F.abil;
  let owned="";
  for(let id=1;id<alen;id++){ const v=buf[abase+id]; if(v!==ABIL_NONE){ const mx=abilMax(id);
    owned+='<div class="invrow"><label style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+id+' — '+((TABLES.Abil&&TABLES.Abil[id])||'?')+' <span class="off">(최대 '+mx+')</span></label>'+
      '<input type="number" min="0" max="'+mx+'" data-abil="'+id+'" value="'+v+'">'+
      '<button class="del smallbtn" data-abildel="'+id+'">✕</button></div>';
  }}
  if(!owned) owned='<p class="hint">보유한 어빌리티가 없습니다.</p>';
  let addopt='<option value="">+ 어빌리티 추가…</option>';
  if(TABLES.Abil) Object.keys(TABLES.Abil).map(Number).filter(id=>id>=1&&id<alen&&buf[abase+id]===ABIL_NONE).sort((a,b)=>a-b)
    .forEach(id=>{ addopt+='<option value="'+id+'">'+id+' — '+TABLES.Abil[id]+' (최대 '+abilMax(id)+')</option>'; });
  e.innerHTML=
  '<div class="grp"><h3>식별 정보 <span class="tag ok">확정</span></h3>'+
    '<div class="fld"><label>이름(읽기전용)</label><input type="text" value="'+recName(off)+'" readonly></div>'+
    selField("캐릭터 ID",off+F.charId,"Char",2)+
    selField("소속",off+F.group,"Group",1)+
    selField("직업",off+F.job,"Job",1)+
    selField("초상화(Face_Stat)",off+F.faceStat,"Face_Stat",2)+
    selField("얼굴대사(Face_Msg)",off+F.faceMsg,"Face_Msg",2)+
  '</div>'+
  '<div class="grp"><h3>능력치 <span class="tag ok">확정</span></h3>'+
    numField("HP",off+F.hp,4,'u32')+
    numField("EXP",off+F.exp,4,'u32')+
    '<div class="combo-grid">'+statg+'</div>'+
  '</div>'+
  '<div class="grp"><h3>장비 <span class="tag ok">확정</span></h3>'+
    selField("무기 1",off+F.weap1,"Item",2)+
    selField("무기 2",off+F.weap2,"Item",2)+
    selField("방어구",off+F.armor,"Item",2)+
    selField("장신구 1",off+F.acc1,"Item",2)+
    selField("장신구 2",off+F.acc2,"Item",2)+
  '</div>'+
  '<div class="grp"><h3>어빌리티 <span class="tag ok">확정</span></h3>'+
    '<p class="hint">보유 어빌리티와 레벨. 레벨을 0으로 두면 미보유 처리됩니다. 최대 레벨은 Abi.dat에서 추출(어빌리티별 상이). 예: 연계기 23~31은 최대 5.</p>'+
    '<div id="abilrows">'+owned+'</div>'+
    '<select id="abiladd" style="margin-top:6px;max-width:320px">'+addopt+'</select>'+
  '</div>'+
  '<div class="grp"><h3>고급: 전체 데이터 <span class="tag guess">raw</span></h3>'+
    '<details><summary>16비트 값 그리드 (직접 편집)</summary>'+raw+'</details>'+
    '<details><summary>HEX 덤프 (읽기전용, 340바이트)</summary><div class="hex">'+hex+'</div></details>'+
  '</div>';
  e.querySelectorAll('[data-off]').forEach(el=>el.addEventListener('change',()=>applyField(el)));
  e.querySelectorAll('[data-abil]').forEach(el=>el.addEventListener('change',()=>{
    const id=+el.dataset.abil, mx=abilMax(id);
    let v=parseInt(el.value,10); if(isNaN(v)||v<0)v=0; if(v>mx){v=mx; el.value=mx;}
    applyAbil(id, v===0?ABIL_NONE:v); if(v===0) renderEdit();
  }));
  e.querySelectorAll('[data-abildel]').forEach(el=>el.addEventListener('click',()=>{
    applyAbil(+el.dataset.abildel, ABIL_NONE); renderEdit();
  }));
  const addsel=document.getElementById('abiladd');
  if(addsel) addsel.addEventListener('change',()=>{ const id=parseInt(addsel.value,10); if(!isNaN(id)){ applyAbil(id,1); renderEdit(); } });
}
function editTargets(){   // 적용 대상 레코드 오프셋: 체크 시 모든 블록의 같은 슬롯, 아니면 현재만
  return document.getElementById('applyall').checked ? slotRecords() : [records[cur]];
}
function applyAbil(id,val){
  for(const t of editTargets()){ buf[t+F.abil+id]=val&0xFF; }
}
function applyField(el){
  const o=+el.dataset.off, size=+el.dataset.size, kind=el.dataset.kind;
  let v=parseInt(el.value,10); if(isNaN(v))return;
  const rel=o-records[cur];
  for(const t of editTargets()){
    const a=t+rel;
    if(kind==='u32') setu32(a,v>>>0);
    else if(size===1) buf[a]=v&0xFF;
    else setu16(a,v&0xFFFF);
  }
  renderList(document.getElementById('search').value.toLowerCase());
}

function renderGlobal(){
  const gb=document.getElementById('globalbar');
  const ok = buf.length > 0x13B68;   // 표준 세이브에서만 소지금 표시
  if(!ok){ gb.style.display='none'; return; }
  const ep = buf.length>4 ? u32(0) : -1;
  const validEp = ep>=0 && ep<3;
  const cur = validEp ? GOLD.find(g=>g.ep===ep) : null;
  const fld=(off)=>'<input type="number" min="0" max="4294967295" data-gold="'+off+'" value="'+u32(off)+'">';
  let html='';
  if(cur){
    html+='<span class="gtitle">💰 현재 소지금 — '+EPISODES[ep]+'</span><span class="gfld">'+fld(cur.off)+'</span>';
  } else {
    html+='<span class="gtitle">💰 소지금</span><span class="hint">진행 중 에피소드 없음(연대표) — 표시 소지금이 없습니다. 아래에서 선택 편집.</span>';
  }
  const others=GOLD.filter(g=>g!==cur);
  html+='<details class="gold-more"><summary>기타 소지금 ('+others.length+') ⚠️</summary>'+
    '<span class="gwarn">다른 에피소드/예비 슬롯입니다. 진행 중이 아닌 값 편집은 게임에 바로 보이지 않을 수 있습니다.</span>';
  for(const g of others){ const nm=g.ep!=null?EPISODES[g.ep]:g.label;
    html+='<span class="gfld"><label>'+nm+'</label>'+fld(g.off)+'</span>'; }
  html+='</details>';
  gb.innerHTML=html; gb.style.display='flex';
  gb.querySelectorAll('[data-gold]').forEach(el=>el.addEventListener('change',()=>{
    let v=parseInt(el.value,10); if(isNaN(v)||v<0)v=0; if(v>0xFFFFFFFF)v=0xFFFFFFFF;
    setu32(+el.dataset.gold, v>>>0);
  }));
}
// ===== 보관함(아이템 저장소) =====
// 구조: [개수:u32][ (아이템ID:u32, 수량:u32) x N ]. 오프셋은 진행도에 따라 이동하므로 스캔으로 탐지.
let invGroups=[], curEpisode=-1;
const EPISODES=['시반슈미터','크림슨크루세이더','아포칼립스'];  // 0x00 = 현재 에피소드 인덱스
// 게임 내장 고정 아이템 목록(모든 세이브에서 동일) — 보관함이 아님. 멀티셋 시그니처로 식별/제외.
const STATIC_SIG='61|2,1;3,1;6,2;7,1;8,1;9,1;10,3;11,2;13,2;14,1;16,3;17,1;19,4;20,1;27,1;28,1;29,1;30,1;32,1;34,1;39,2;43,1;46,4;47,9;51,1;52,1;53,1;54,4;55,1;56,3;62,1;72,2;73,2;77,1;78,3;80,2;81,1;83,1;86,1;88,3;89,4;91,1;92,7;94,2;101,6;103,4;104,4;105,6;112,2;113,3;114,3;122,1;123,1;126,11;127,20;128,5;129,1;130,7;131,8;135,6;142,1';
function scanInv(){
  const found=[];
  let o=4;
  while(o+12<=buf.length){
    const n=u32(o);
    if(n>=2 && n<=120 && u32(o-4)===0 && o+4+n*8<=buf.length){
      let ok=true;
      for(let k=0;k<n;k++){const id=u32(o+4+k*8),q=u32(o+4+k*8+4); if(!(id>=1&&id<=181&&q>=1&&q<=999)){ok=false;break;}}
      if(ok){
        const end=o+4+n*8;
        // 빈 공간 = 배열 뒤 "다음 실제 구조" 전까지의 슬롯 수. 게임은 이 영역(0 또는 잔여 아이템 데이터)에
        // 그대로 덮어쓰며 보관함을 확장함(테스트로 확인). 다음 구조는 보관함 쌍으로 볼 수 없는 값(id>181 또는 qty>999)에서 시작.
        let slack=0,p=end;
        while(p+8<=buf.length){ const fid=u32(p),fq=u32(p+4); if(fid<=181&&fq<=999){slack++;p+=8;if(slack>=250)break;} else break; }
        found.push({off:o,n,slack});
        o=end; continue;                       // 테이블 내부 재탐지 방지
      }
    }
    o+=2;                                       // 2바이트 정렬(테이블이 2바이트 경계에 올 수 있음)
  }
  // 순서 무관(멀티셋) 내용으로 사본 묶기 → 라이브/스냅샷 사본을 함께 수정
  const sigOf=t=>{const a=Array.from({length:t.n},(_,k)=>[u32(t.off+4+k*8),u32(t.off+4+k*8+4)]);
    a.sort((x,y)=>x[0]-y[0]||x[1]-y[1]); return t.n+'|'+a.map(p=>p[0]+','+p[1]).join(';');};
  const map={};
  for(const t of found){ const s=sigOf(t); (map[s]=map[s]||{members:[],slacks:[],n:t.n}); map[s].members.push(t.off); map[s].slacks.push(t.slack); }
  // 현재 에피소드 & "작업영역(소지금 뒤 ~ 블록1 앞)" 보관함 = 현재 진행 중 에피소드의 라이브 보관함
  curEpisode = buf.length>4 ? u32(0) : -1;
  const validEp = curEpisode>=0 && curEpisode<3;     // 0xFFFFFFFF(=-1) = 연대표(진행 에피소드 없음)
  const GOLD_OFF=0x13B58;
  const blk1 = records.length>106 ? records[106] : buf.length;
  invGroups=Object.values(map).map(g=>{
    const o=g.members[0];
    g.items=Array.from({length:g.n},(_,k)=>({id:u32(o+4+k*8),qty:u32(o+4+k*8+4)}));
    g.origN=g.n; g.cap=g.n+Math.min(...g.slacks);
    g.totalQty=g.items.reduce((s,it)=>s+it.qty,0);
    g.minOff=Math.min(...g.members);
    g.sig=g.n+'|'+g.items.map(it=>[it.id,it.qty]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]).map(p=>p[0]+','+p[1]).join(';');
    g.isStatic=(g.sig===STATIC_SIG);
    g.episode=-1;
    g.isCurrent = validEp && !g.isStatic && g.minOff>GOLD_OFF && g.minOff<blk1;  // 소지금 뒤 작업영역 = 현재 에피소드 라이브 보관함
    return g;
  });
  // 나머지 에피소드: 소지금 앞(아카이브) 보관함을 오프셋 순서대로 비현재 에피소드 인덱스에 매핑
  if(invGroups.find(g=>g.isCurrent)) invGroups.find(g=>g.isCurrent).episode=curEpisode;
  const others=invGroups.filter(g=>!g.isStatic && !g.isCurrent && g.minOff<GOLD_OFF).sort((a,b)=>a.minOff-b.minOff);
  const nonCur=[0,1,2].filter(e=>e!==curEpisode);
  others.forEach((g,i)=>{ if(i<nonCur.length) g.episode=nonCur[i]; });
  invGroups.forEach(g=>{
    if(g.isStatic) g.label='게임 기본 아이템 목록 (보관함 아님 · 편집 비권장)';
    else if(g.isCurrent) g.label='🟢 현재 보관함 — '+(EPISODES[curEpisode]||('에피소드 '+curEpisode));
    else if(g.episode>=0 && g.episode<3) g.label=EPISODES[g.episode]+' 보관함 (추정)';
    else g.label='기타 보관함 (다른 시점/아카이브)';
  });
  // 정렬: 현재 → 에피소드 추정 → 기타 → 정적목록
  const rank=g=> g.isCurrent?0 : (g.episode>=0?1+g.episode : (g.isStatic?9:5));
  invGroups.sort((a,b)=> rank(a)-rank(b) || a.minOff-b.minOff);
}
function writeGroup(g){
  for(const off of g.members){
    for(let k=0;k<Math.max(g.origN,g.items.length);k++){ setu32(off+4+k*8,0); setu32(off+4+k*8+4,0); }
    g.items.forEach((it,k)=>{ setu32(off+4+k*8,it.id>>>0); setu32(off+4+k*8+4,it.qty>>>0); });
    setu32(off,g.items.length>>>0);
  }
}
function invBoxHtml(g,gi){
  const loc=g.members.map(o=>'0x'+o.toString(16)).join(', ');
  const rows=g.items.map((it,ri)=>
    '<div class="invrow">'+
     '<select data-g="'+gi+'" data-r="'+ri+'" data-k="id">'+opt("Item",it.id)+'</select>'+
     '<input type="number" min="0" max="999" data-g="'+gi+'" data-r="'+ri+'" data-k="qty" value="'+it.qty+'">'+
     '<button class="del smallbtn" data-g="'+gi+'" data-del="'+ri+'">✕</button>'+
    '</div>').join("");
  const title=g.label+' — '+g.items.length+'종 / 총 '+g.totalQty+'개 (최대 '+g.cap+'종)';
  const hl=g.isCurrent?' style="color:var(--ok);font-weight:600"':(g.isStatic?' style="color:var(--mut)"':'');
  return '<div class="invtbl'+(g.isCurrent?' cur':'')+'"><div class="ih"><span'+hl+'>'+title+'</span>'+
    '<span class="hint">사본 '+g.members.length+'개 @ '+loc+'</span></div>'+rows+
    '<button class="smallbtn" data-add="'+gi+'" '+(g.items.length>=g.cap?'disabled':'')+'>+ 아이템 추가</button>'+
    (g.items.length>=g.cap?'<span class="hint" style="margin-left:8px">빈 공간이 없어 슬롯 추가는 불가합니다. 기존 슬롯의 <b>아이템 종류</b>/<b>수량</b>을 바꿔 교체하세요.</span>':'')+
    '</div>';
}
function renderInv(){
  const wrap=document.getElementById('invlist'); wrap.innerHTML="";
  if(!invGroups.length){ wrap.innerHTML='<p class="hint">편집 가능한 보관함을 찾지 못했습니다.</p>'; return; }
  const validEp = curEpisode>=0 && curEpisode<EPISODES.length;
  const epName = validEp? EPISODES[curEpisode] : '없음 (연대표 상태)';
  let html='';
  // 안내 배너
  html+='<p class="hint">현재 진행 에피소드: <b style="color:var(--ok)">'+epName+'</b> (세이브 0x00='+(curEpisode>>>0)+').</p>';
  const current=[], others=[];
  invGroups.forEach((g,gi)=>{ (g.isCurrent?current:others).push([g,gi]); });
  // 현재 보관함 (안전 편집 영역)
  if(current.length){
    html+='<div class="zone-safe"><div class="zone-h">✅ 현재 진행 중 에피소드 보관함 — 안전하게 편집 가능</div>';
    current.forEach(([g,gi])=>html+=invBoxHtml(g,gi));
    html+='</div>';
  } else {
    html+='<div class="zone-safe"><div class="zone-h">✅ 현재 진행 중 에피소드 보관함</div>'+
      '<p class="hint">현재 진행 중인 에피소드가 없습니다(연대표 상태). 이 세이브에는 <b>안전하게 편집할 현재 보관함이 없습니다.</b> 아래 보관함들은 모두 위험 영역입니다.</p></div>';
  }
  // 위험 영역 (펼치기)
  if(others.length){
    html+='<details class="zone-danger"><summary>⚠️ 위험 영역 — 현재 에피소드가 아닌 보관함 '+others.length+'개 (펼쳐서 접근)</summary>'+
      '<div class="danger-warn">⚠️ <b>주의:</b> 아래는 현재 진행 중이 아닌 다른 에피소드의 아카이브 보관함(추정), 과거 시점 사본, 또는 게임 내부 고정 목록입니다.<br>'+
      '• 라벨은 위치 규칙 기반 <b>추정</b>이며 실제와 다를 수 있습니다 — 반드시 아이템 내용을 확인하세요.<br>'+
      '• 진행 중이 아닌 보관함 편집은 게임에 반영되지 않거나 예기치 않은 동작을 일으킬 수 있습니다.<br>'+
      '• <b>"게임 기본 아이템 목록"은 보관함이 아니므로 편집하지 마세요.</b><br>'+
      '편집 전 반드시 세이브 파일을 백업하세요.</div>';
    others.forEach(([g,gi])=>html+=invBoxHtml(g,gi));
    html+='</details>';
  }
  wrap.innerHTML=html;
  wrap.querySelectorAll('[data-k]').forEach(el=>el.addEventListener('change',()=>{
    const g=invGroups[+el.dataset.g]; const it=g.items[+el.dataset.r];
    let v=parseInt(el.value,10); if(isNaN(v))v=0;
    if(el.dataset.k==='id') it.id=v; else it.qty=Math.max(0,Math.min(999,v));
    writeGroup(g);
  }));
  wrap.querySelectorAll('[data-del]').forEach(el=>el.addEventListener('click',()=>{
    const g=invGroups[+el.dataset.g]; g.items.splice(+el.dataset.del,1); writeGroup(g); renderInv();
  }));
  wrap.querySelectorAll('[data-add]').forEach(el=>el.addEventListener('click',()=>{
    const g=invGroups[+el.dataset.add]; if(g.items.length>=g.cap)return; g.items.push({id:126,qty:1}); writeGroup(g); renderInv();
  }));
}
function loadBuf(arr){
  buf=new Uint8Array(arr);
  for(let i=0;i<buf.length;i++) buf[i]^=0xFF;
  parse();
  document.getElementById('drop').style.display='none';
  document.querySelector('main').style.display='grid';
  document.getElementById('save').disabled=false;
  document.getElementById('invbtn').disabled=false;
  scanInv();
  cur=records.length?0:-1;
  renderGlobal(); renderList(); renderEdit();
}
function doSave(){
  const out=new Uint8Array(buf.length);
  for(let i=0;i<buf.length;i++) out[i]=buf[i]^0xFF;
  // 변조방지 체크섬 재계산: raw 바이트[0..len-3]에 가중치(1,3,5,7) 적용 후 %32000, 끝 2바이트(LE)에 기록
  let acc=0;
  for(let i=0;i<out.length-2;i++){ acc=(acc + out[i]*(2*(i&3)+1))%32000; }
  out[out.length-2]=acc&0xFF; out[out.length-1]=(acc>>8)&0xFF;
  const blob=new Blob([out],{type:'application/octet-stream'});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download=fileName.replace(/\.sav$/i,'')+'_edited.sav';
  a.click();
}

document.getElementById('open').onclick=()=>document.getElementById('file').click();
document.getElementById('file').onchange=e=>{const f=e.target.files[0];if(!f)return;fileName=f.name;document.getElementById('fname').textContent=f.name;f.arrayBuffer().then(loadBuf);};
document.getElementById('save').onclick=doSave;
document.getElementById('invbtn').onclick=()=>{renderInv();document.getElementById('modal').style.display='flex';};
document.getElementById('invclose').onclick=()=>document.getElementById('modal').style.display='none';
document.getElementById('modal').onclick=e=>{if(e.target.id==='modal')document.getElementById('modal').style.display='none';};
document.getElementById('search').oninput=e=>renderList(e.target.value.toLowerCase());
const drop=document.getElementById('drop');
['dragover','dragenter'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('hl');}));
['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('hl');}));
drop.addEventListener('drop',e=>{const f=e.dataTransfer.files[0];if(f){fileName=f.name;document.getElementById('fname').textContent=f.name;f.arrayBuffer().then(loadBuf);}});
</script>
</body>
</html>'''

HTML = HTML.replace("__TABLES__", tables).replace("__ABILMAX__", abil_max)
out = os.path.join(DIST, 'index.html')
open(out, 'w', encoding='utf-8').write(HTML)
print("written:", out, len(HTML), "bytes")
