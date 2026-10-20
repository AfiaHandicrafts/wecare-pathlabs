def patch(f,reps):
    s=open(f,encoding="utf-8").read()
    for a,b in reps:
        if s.count(a)!=1:
            print("!! could not patch in",f,":",a[:60]);continue
        s=s.replace(a,b)
    open(f,"w",encoding="utf-8").write(s);print("done",f)

CSS=r'''.sl .s{background-size:cover!important;background-position:center!important;color:#fff!important}.sl .s .btn{background:#ffc928!important;color:#1d1d1d!important}.pic{display:none!important}.sl{height:340px}.tx{max-width:60%}.tx h2{font-size:clamp(1.3rem,4vw,2.3rem)}
.qs{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 16px}.qs span{background:#ffffff22;border:1px solid #ffffff55;padding:5px 12px;border-radius:16px;font-size:.8rem;font-weight:600}
.im{background-size:cover;background-position:center;height:140px}.im svg{display:none}
.tr{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;max-width:1050px;margin:0 auto 10px;padding:0 14px}.tr div{background:var(--gl);border:1px solid var(--ln);border-left:4px solid var(--y);border-radius:12px;padding:12px 14px;font-weight:600;font-size:.9rem}.tr small{display:block;font-weight:400;opacity:.8;margin-top:2px}
@media(max-width:600px){.sl{height:380px}.tx{max-width:92%}}'''
STRIP=r'''<div class="tr"><div>&#10003; Accurate reports<small>Careful quality checks on every sample</small></div><div>&#10003; Hygienic collection<small>Sterile, single-use needles and tubes</small></div><div>&#10003; Trained team<small>Qualified lab professionals</small></div><div>&#10003; Quick E-reports<small>Sent to your phone or email</small></div><div>&#10003; Home collection<small>We come to you</small></div><div>&#10003; Open 7 days<small>24/7 emergency service</small></div></div>'''
HERO=r'''const DEF=["lab","pathologist","checkup","bloodtest","tubes","patient","doctor","microscope"],QS=[["Accurate reports","Hygienic collection","Trained staff"],["Quick E-reports","Home sample collection","Open 7 days"],["Affordable packages","24/7 emergency service","Friendly care"]];
function hero(){$("sl").innerHTML=A.map((a,i)=>{const k=a.kind||"info",img=a.image_url||("images/"+DEF[i%DEF.length]+".jpg");
return `<div class="s ${k}" style="background-image:linear-gradient(90deg,#0a2a21f2 30%,#0a2a2166 70%,#0a2a2133),url('${esc(img)}')"><div class="tx"><small>${IC[k]||""} ${k.toUpperCase()}</small><h2>${esc(a.text)}</h2><div class="qs">${QS[i%3].map(q=>`<span>&#10003; ${q}</span>`).join("")}</div><a class="btn" target="_blank" rel="noopener" href="${wa("Hello, I saw this on your site: "+a.text)}">Book now</a></div></div>`}).join("")+'<button class="ar l">&#10094;</button><button class="ar r">&#10095;</button><div class="dots"></div>';slider($("sl"),5500)}
'''
IMS=r'''const IM={"Packages":"checkup","Hematology":"bloodtest","Biochemistry":"tubes","Hormones & Vitamins":"tubes","Infection":"microscope","Clinical Pathology":"tray","Histopathology":"pathologist","Tumor Markers":"lab"};const AM={'''
SL2=r'''const P2=["pathologist","bloodtest","patient"];document.querySelectorAll("#sl2 .s").forEach((e,i)=>e.style.backgroundImage="linear-gradient(90deg,#0a2a21f2 30%,#0a2a2166 70%,#0a2a2133),url('images/"+P2[i]+".jpg')");slider($("sl2"),6000);'''

patch("index.html",[
 ("</style></head><body>",CSS+"</style></head><body>"),
 ('<div class="sl" id="sl"></div>','<div class="sl" id="sl"></div>'+STRIP),
 ('function hero(){$("sl")',HERO+'function heroOld(){$("sl")'),
 ("const AM={",IMS),
 (r'''<div class="im">${art(AM[x.category]||"report")}</div>''',r'''<div class="im" style="background-image:url('images/${IM[x.category]||"lab"}.jpg')"></div>'''),
 (r'''document.querySelectorAll(".pic[data-a]").forEach(p=>p.innerHTML=art(p.dataset.a));slider($("sl2"),6000);''',SL2)])

patch("test.html",[
 ("</style></head><body>",".pic{display:none}</style></head><body>"),
 ("const ST=[",'const PH={book:"patient",blood:"bloodtest",microscope:"microscope",report:"checkup"};const ST=['),
 ('<div class="s"><div class="tx"><small>',r'''<div class="s" style="background-image:linear-gradient(90deg,#0a2a21f2 32%,#0a2a2166 75%,#0a2a2133),url('images/${PH[s[0]]}.jpg');background-size:cover;background-position:center"><div class="tx"><small>''')])

patch("admin.html",[
 ('$("b1").innerHTML=art("doctor");$("b2").innerHTML=art("blood");',r'''document.body.style.background="linear-gradient(#0a2a21e8,#0a2a21e8),url('images/doctor.jpg') center/cover fixed";''')])
