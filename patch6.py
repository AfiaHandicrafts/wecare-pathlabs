import shutil, sys, os, subprocess
f = "index.html"
s = open(f, encoding="utf-8").read()
if "const DICT=" in s:
    print("patch6 is already applied. Nothing to do."); sys.exit(0)
if "const doSearch=" not in s:
    if os.path.exists("patch5.py"):
        print("patch5 not found in index.html - running patch5.py first...")
        subprocess.run([sys.executable, "patch5.py"])
        s = open(f, encoding="utf-8").read()
    if "const doSearch=" not in s:
        print("!! Run patch5.py first, then run patch6.py again."); sys.exit(1)
shutil.copy(f, "index.backup6.html")
bad = 0

def rep(old, new, label):
    global s, bad
    if s.count(old) != 1:
        print("!! not applied:", label); bad += 1; return
    s = s.replace(old, new); print("ok:", label)

lines = s.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("function match(x,s){")]
if len(idx) != 1:
    print("!! not applied: match function"); bad += 1
else:
    lines[idx[0]] = r'''const STOP=new Set(["test","tests","for","the","and","of","my","a"]);
const EXP={cbc:"complete blood count",lft:"liver function",kft:"kidney function",rft:"kidney function",sugar:"glucose",diabetes:"glucose hba1c",diabetic:"glucose hba1c",anemia:"anaemia hemoglobin",anaemia:"hemoglobin iron",cholesterol:"lipid",fever:"widal dengue malaria typhoid",hb:"hemoglobin",vitd:"vitamin",d3:"vitamin",thyroid:"tsh",pregnancy:"pregnan hcg"};
function toks(s){return norm(String(s).toLowerCase().replace(/check\s*-?\s*up/g,"checkup")).split(" ").filter(t=>t.length>1&&!STOP.has(t))}
function sc(t,nw,dw){if(nw.some(w=>w.startsWith(t)))return 3;if(t.length>2&&nw.some(w=>w.includes(t)))return 2.5;
if(t.length>=5&&nw.some(w=>lev(t,w)<=1||(w.length>t.length&&lev(t,w.slice(0,t.length))<=1)))return 2;if(dw.some(w=>w.startsWith(t)))return 1;return 0}
function score(x,s){const ts=toks(s);if(!ts.length)return 1;const nw=norm(x.name).split(" ").filter(Boolean),dw=norm((x.description||"")+" "+x.category).split(" ").filter(Boolean);let tot=0;
for(const t of ts){let b=sc(t,nw,dw);if(!b&&EXP[t])for(const e of EXP[t].split(" "))b=Math.max(b,sc(e,nw,dw)*.8);if(!b)return 0;tot+=b}return tot}
function match(x,s){return score(x,s)>0}'''
    s = "\n".join(lines); print("ok: smarter matching")

rep('const l=T.filter(x=>(cat=="All"||x.category==cat)&&match(x,q));',
    'let l=T.filter(x=>(cat=="All"||x.category==cat)&&match(x,q));if(q.trim())l.sort((a,b)=>score(b,q)-score(a,q));', "best matches first")

rep('<small id="rc"></small></div>', '<small id="rc"></small><div id="sg" class="sgl"></div></div>', "dropdown markup")

DICTJS = r'''const DICT=[
["blood|rbc|wbc|haem|hema",["CBC","Platelets","Hemoglobin","ESR","Blood group","Blood sugar","PT INR"]],
["sugar|diabetes|glucose|diabetic",["Blood sugar","Fasting glucose","HbA1c","Diabetes package","Urine sugar"]],
["thyroid|tsh|goitre",["Thyroid profile","TSH","T3","T4"]],
["liver|jaundice|hepatitis",["LFT","SGPT","SGOT","Bilirubin","Hepatitis B","Hepatitis C"]],
["kidney|renal|urea",["KFT","Creatinine","Urea","Uric acid","Electrolytes"]],
["fever|typhoid|infection",["Widal","Typhoid","Dengue","Malaria","CRP","CBC"]],
["heart|cardiac|cholesterol|lipid",["Lipid profile","Cholesterol","HDL","LDL","Triglycerides"]],
["vitamin|weakness|tired",["Vitamin D","Vitamin B12","Iron","Ferritin"]],
["anaemia|anemia|iron",["Hemoglobin","CBC","Iron","Ferritin","Vitamin B12"]],
["urine|pee",["Urine routine","Urine culture","Urine sugar"]],
["stool|motion",["Stool routine","Stool culture"]],
["pregnancy|pregnant|women|woman",["Pregnancy test","Beta HCG","Thyroid profile","Hemoglobin","Women's health"]],
["cancer|tumor|tumour|marker",["PSA","CA-125","Biopsy","FNAC","Pap smear"]],
["joint|arthritis|pain|bone",["Uric acid","RA factor","CRP","ESR","Calcium","Vitamin D"]],
["hormone|infertility|pcos",["TSH","Prolactin","FSH","LH","Testosterone"]],
["body|checkup|health|package",["Full body checkup","Senior citizen","Diabetes package","Cardiac package","Women's health"]],
["allergy|asthma",["IgE","CBC"]],
["hiv|aids|std",["HIV","Hepatitis B","VDRL"]]
];
const SG=$("sg");
function sugg(v){v=v.trim().toLowerCase();if(v.length<2)return[];const out=[],seen=new Set();
const add=(label,note)=>{const k=label.toLowerCase();if(seen.has(k)||k===v)return;const n=T.filter(x=>match(x,label)).length;if(!n)return;seen.add(k);out.push({label,note,n})};
for(const[keys,rel]of DICT){const ks=keys.split("|");if(ks.some(k=>k.startsWith(v)||(v.length>=4&&lev(v,k.slice(0,v.length))<=1)))rel.forEach(r=>add(r,ks[0]))}
T.forEach(x=>{if(norm(x.name).split(" ").some(w=>w.startsWith(v)))add(x.name,x.category)});return out.slice(0,7)}
function showSg(){const a=sugg($("q").value);SG.innerHTML=a.map(o=>`<button type="button" class="sg" data-v="${esc(o.label)}"><span>&#128270;</span><b>${esc(o.label)}</b><small>${esc(o.note)} &bull; ${o.n} test${o.n>1?"s":""}</small></button>`).join("");SG.style.display=a.length?"block":"none"}
SG.addEventListener("mousedown",e=>e.preventDefault());
SG.addEventListener("click",e=>{const b=e.target.closest(".sg");if(b){$("q").value=b.dataset.v;doSearch();SG.style.display="none";$("q").blur()}});
document.addEventListener("click",e=>{if(!e.target.closest(".sbar"))SG.style.display="none"});
$("q").addEventListener("focus",()=>{if($("q").value.trim().length>1)showSg()});
$("up").onclick=()=>scrollTo({top:0,behavior:"smooth"});addEventListener("scroll",()=>$("up").classList.toggle("show",scrollY>600),{passive:true});
'''
rep('const doSearch=()=>{', DICTJS + 'const doSearch=()=>{', "dictionary + dropdown code")
rep('chips();grid();if(q.trim().length>1){', 'chips();grid();showSg();if(q.trim().length>1){', "show suggestions while typing")
rep('e.preventDefault();$("q").blur()}', 'e.preventDefault();SG.style.display="none";$("q").blur()}', "Enter closes dropdown")
rep('<div class="mbar">', '<button id="up" aria-label="Back to top">&#8593;</button>\n<div class="mbar">', "back-to-top button")

CSS = r'''
/* ---- patch6: suggestions + extra polish ---- */
.sgl{display:none;position:absolute;left:max(14px,calc((100% - 1050px)/2));right:max(14px,calc((100% - 1050px)/2));top:64px;background:#fff;color:#1d1d1d;border-radius:16px;box-shadow:0 14px 36px #000b;overflow:hidden;overflow-y:auto;max-height:60vh;z-index:40}
.sg{display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:none;border:0;border-bottom:1px solid #eef1ef;padding:13px 16px;cursor:pointer;font:inherit;color:#1d1d1d;min-height:48px}
.sg:last-child{border-bottom:0}.sg:hover,.sg:active{background:#fff3c4}
.sg b{flex:1;font-weight:700}.sg small{color:#667;font-weight:500;white-space:nowrap}
#up{position:fixed;right:14px;bottom:78px;z-index:22;width:44px;height:44px;border-radius:50%;border:0;background:var(--y);color:#1d1d1d;font-size:1.3rem;font-weight:800;box-shadow:0 4px 14px #000a;opacity:0;pointer-events:none;transform:translateY(10px);transition:.25s;cursor:pointer}
#up.show{opacity:1;pointer-events:auto;transform:none}
.card{animation:up .45s ease both}@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.card:active{transform:scale(.98)}
.top span:first-child:before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#4cd98c;margin-right:6px;animation:pl 1.6s infinite}
@keyframes pl{0%{box-shadow:0 0 0 0 #4cd98c99}100%{box-shadow:0 0 0 9px #4cd98c00}}
.btn:focus-visible,.chip:focus-visible,#q:focus-visible{outline:3px solid #fff;outline-offset:2px}
.tag.c{backdrop-filter:blur(4px)}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
@media(max-width:600px){
 #cg{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:10px;margin:0 -12px;padding:0 12px 8px;scrollbar-width:none}
 #cg::-webkit-scrollbar{display:none}
 #cg .cc{flex:0 0 150px;scroll-snap-align:start}
 .tr{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:10px;padding:0 12px 8px;scrollbar-width:none}
 .tr::-webkit-scrollbar{display:none}
 .tr div{flex:0 0 74%;scroll-snap-align:start}
 .sgl{top:62px}
 #up{bottom:84px}
}
@media(min-width:801px){#up{bottom:70px}}
@media(min-width:601px) and (max-width:1000px){.sl{height:380px}.tx{max-width:70%}section{padding:26px 20px}}
'''
rep('</style>', CSS + '</style>', "css")

if bad:
    print("\n%d step(s) failed - index.html NOT changed. Send me the !! lines." % bad); sys.exit(1)
open(f, "w", encoding="utf-8").write(s)
print("\nAll done. Backup saved as index.backup6.html")
