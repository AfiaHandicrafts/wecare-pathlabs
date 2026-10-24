import re
def edit(f,subs,regs):
    s=open(f,encoding="utf-8").read()
    for a,b in subs:
        if s.count(a)!=1:
            print("!! not found once in",f,":",a[:55]);continue
        s=s.replace(a,b)
    for pat,b,fl in regs:
        if len(re.findall(pat,s,fl))!=1:
            print("!! pattern not found in",f,":",pat[:40]);continue
        s=re.sub(pat,lambda m:b,s,flags=fl)
    open(f,"w",encoding="utf-8").write(s);print("done",f)

CSS2=r'''const css2=document.createElement("style");css2.textContent=`.xh .xw{grid-column:1/-1}.xh .xw .xr{background:none!important;border:0!important;border-bottom:1px dashed rgba(255,255,255,.15)!important;border-radius:0!important;padding:6px 0!important;display:flex;justify-content:space-between}.xh .xw .xr.xt{color:#ffc928;font-weight:700}.xh .xw .xr i{color:#ff9a9a;font-style:normal}`;document.head.appendChild(css2);'''
UPD=r'''const upd=()=>{$("xwa").href=wa(msg());const m=closedMsg($("xdt").value,$("xtm").value),b=$("xm");if(m)b.innerHTML='<div class="xerr">'+esc(m)+'</div>';else if(b.firstChild&&b.firstChild.className=="xerr")b.innerHTML=""};'''
MENU=r'''document.addEventListener("click",e=>{const n=$("nav");if(n&&n.classList.contains("open")&&!n.contains(e.target)&&!e.target.closest("#mb"))n.classList.remove("open")});document.addEventListener("keydown",e=>{if(e.key==="Escape"){const n=$("nav");n&&n.classList.remove("open")}});window.addEventListener("scroll",()=>{const n=$("nav");n&&n.classList.remove("open")},{passive:true});
'''
HOURS=r'''function t12(t){if(!t)return"";const p=t.split(":").map(Number);return(p[0]%12||12)+":"+String(p[1]).padStart(2,"0")+(p[0]<12?" AM":" PM")}
function wk(){try{return JSON.parse(S.week)}catch(e){return null}}
const DK=["sun","mon","tue","wed","thu","fri","sat"],DN=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
function closedMsg(d,t){const w=wk();if(!w||!d)return"";const i=new Date(d+"T12:00:00").getDay(),x=w[DK[i]];if(!x)return"";
if(!x.o)return"We are closed on "+DN[i]+"s. Please choose another day (for an emergency, please call us).";
if(x.f&&x.t&&t&&(t<x.f||t>x.t))return"On "+DN[i]+" we are open "+t12(x.f)+" to "+t12(x.t)+". Please choose a time in between.";return""}
function hours(){const w=wk(),td=new Date().getDay();let rows="";
if(w){rows='<div class="xw"><small>&#128197; Weekly schedule</small>'+[1,2,3,4,5,6,0].map(i=>{const x=w[DK[i]]||{o:1};return'<div class="xr'+(i==td?" xt":"")+'"><b>'+DN[i]+(i==td?" (today)":"")+'</b><span>'+(x.o?(x.f&&x.t?t12(x.f)+" - "+t12(x.t):"Open"):"<i>Closed</i>")+'</span></div>'}).join("")+'</div>'}
else rows="<div>&#128197; <small>Working days</small><b>"+esc(S.hours_days)+"</b></div><div>&#9200; <small>Timings</small><b>"+esc(S.hours_time)+"</b></div>";
$("xh").innerHTML=rows+[["&#128680;","Emergency",S.hours_emergency],["&#127968;","Sample collection",S.hours_note]].filter(x=>x[2]).map(x=>"<div>"+x[0]+" <small>"+x[1]+"</small><b>"+esc(x[2])+"</b></div>").join("")}'''
edit("extras.js",[
 ("document.head.appendChild(css);","document.head.appendChild(css);"+CSS2),
 ('$("xdt").min=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,10);','const td0=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,10);$("xdt").min=td0;$("xdt").value=td0;'),
 ('const upd=()=>{$("xwa").href=wa(msg())};',UPD),
 ('const row={first_name:','const dc=closedMsg($("xdt").value,$("xtm").value);if(dc){show(esc(dc),1);return}const row={first_name:'),
 ('const nv=$("nav");if(nv&&nv.tagName=="NAV"){',MENU+'const nv=$("nav");if(nv&&nv.tagName=="NAV"){'),
 ('a.textContent="Make an appointment";nv.insertBefore(a,nv.firstChild)}','a.textContent="Make an appointment";nv.insertBefore(a,nv.firstChild);const c=document.createElement("a");c.href="#";c.innerHTML="&#10005; Close menu";c.onclick=ev=>{ev.preventDefault();nv.classList.remove("open")};nv.insertBefore(c,nv.firstChild)}')],
 [(r'^function hours\(\)\{.*$',HOURS,re.M)])

SET=r'''const DY=[["mon","Monday"],["tue","Tuesday"],["wed","Wednesday"],["thu","Thursday"],["fri","Friday"],["sat","Saturday"],["sun","Sunday"]];
async function settings(){const{data}=await sb.from("settings").select("*"),o={};(data||[]).forEach(r=>o[r.key]=r.value);let w={};try{w=JSON.parse(o.week||"{}")}catch(e){}
const F=[["phone","Phone"],["email","E-mail (shown in full on the site)"],["address","Address"],["hours_emergency","Emergency service text"],["hours_note","Extra note (e.g. home collection)"],["hours_days","Short working-days text (used only if no weekly schedule is saved)"],["hours_time","Short timings text (same)"]];
app.innerHTML=`<div class="box"><h2>&#128197; Weekly working schedule</h2><small>Switch a day off when the lab is closed. Times are optional. Patients cannot book appointments on closed days.</small>
${DY.map(d=>{const x=w[d[0]]||{o:1,f:"",t:""};return`<div class="card" style="margin-top:8px"><div class="row"><b style="min-width:92px">${d[1]}</b><label><input type="checkbox" id="wo_${d[0]}" ${x.o?"checked":""}>Open</label></div><div class="g2"><div><label class="k">Opens at</label><input type="time" id="wf_${d[0]}" value="${esc(x.f)}"></div><div><label class="k">Closes at</label><input type="time" id="wt_${d[0]}" value="${esc(x.t)}"></div></div></div>`}).join("")}
<div class="row" style="margin-top:10px"><button class="b" onclick="saveWeek()">Save weekly schedule</button><button class="b gr" onclick="allDays(1)">All days open</button><button class="b" onclick="copyMon()">Copy Monday times to all</button></div></div>
<div class="box"><h2>&#9881; Contact &amp; other details</h2>${F.map(f=>`<label class="k">${f[1]}</label><input id="s_${f[0]}" value="${esc(o[f[0]])}">`).join("")}<br><button class="b" onclick="saveSet()">Save</button></div>
<div class="box"><h2>&#128273; Change admin password</h2><label class="k">New password (at least 8 characters)</label><input id="npw" type="password" autocomplete="new-password"><br><button class="b" onclick="chPw()">Change password</button></div>`}
async function saveWeek(){const w={};DY.forEach(d=>{w[d[0]]={o:$("wo_"+d[0]).checked?1:0,f:$("wf_"+d[0]).value,t:$("wt_"+d[0]).value}});const{error}=await sb.from("settings").upsert({key:"week",value:JSON.stringify(w)});note(error?error.message:"Weekly schedule saved")}
function allDays(v){DY.forEach(d=>$("wo_"+d[0]).checked=!!v)}
function copyMon(){DY.forEach(d=>{$("wf_"+d[0]).value=$("wf_mon").value;$("wt_"+d[0]).value=$("wt_mon").value})}
'''
edit("admin.html",[],[(r'async function settings\(\)\{.*?\}\n(?=async function saveSet)',SET,re.S)])
