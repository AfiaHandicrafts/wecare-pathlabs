import re
def patch(f,reps):
    s=open(f,encoding="utf-8").read()
    for a,b in reps:
        if s.count(a)!=1:
            print("!! could not patch in",f,":",a[:60]);continue
        s=s.replace(a,b)
    open(f,"w",encoding="utf-8").write(s);print("done",f)

MOB=r'''html{-webkit-text-size-adjust:100%}body{overflow-x:hidden}@media(hover:none){body{background-attachment:scroll}}header{-webkit-backdrop-filter:blur(10px)}
@media(max-width:600px){header h1{font-size:1rem}header img{height:38px;width:38px}.top{font-size:.68rem;padding:5px 10px}.top div:last-child{display:none}.btn{padding:8px 14px;font-size:.85rem}#feed{top:74px;right:6px;width:68vw}.tx h2{font-size:1.25rem}.qs span{font-size:.7rem;padding:4px 9px}section{padding:18px 12px}.grid{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}#fab{bottom:10px;right:10px;font-size:.8rem}#hw{display:none}}'''
TOP=r'''if("scrollRestoration"in history)history.scrollRestoration="manual";if(location.hash)history.replaceState(null,"",location.pathname+location.search);window.scrollTo(0,0);window.addEventListener("load",()=>window.scrollTo(0,0));'''
KWJS=r'''const KW=[["senior|elder","senior"],["pregnan|women|woman","woman"],["diabet|sugar|hba1c|glucose","glucose"],["heart|cardiac|lipid","heart"],["thyroid|tsh","thyroid"],["vitamin|iron|anaem|b12|ferritin","vitamin"],["urine|stool","urine"],["dengue|malaria|widal|typhoid|crp|hiv|hepatitis|culture|fever","microscope"],["liver|kidney|uric|electrolyte","tubes"],["blood group|cbc|hemoglobin|platelet|esr|inr","bloodtest"],["biopsy|fnac|pap smear|psa|ca-125","pathologist"],["men's|male","doctor"],["full body|checkup|health|package|employment","checkup"]];
function pic(x){const n=(x.name+" "+x.category).toLowerCase();for(const[k,v]of KW)if(new RegExp(k).test(n))return v;return IM[x.category]||"lab"}
'''
patch("index.html",[
 ("</style></head><body>",MOB+"</style></head><body>"),
 ("const IM={",KWJS+"const IM={"),
 (r'''<div class="im" style="background-image:url('images/${IM[x.category]||"lab"}.jpg')"></div>''',r'''<div class="im" style="background-image:url('images/${pic(x)}.jpg'),url('images/${IM[x.category]||"lab"}.jpg')"></div>'''),
 ("const sb=(typeof SUPABASE_URL",TOP+"const sb=(typeof SUPABASE_URL"),
 ("Not valid for medico legal purpose</footer>","Not valid for medico legal purpose &bull; Photos: Pixabay &amp; Pexels</footer>")])

patch("test.html",[
 ("</style></head><body>",r'''html{-webkit-text-size-adjust:100%}body{overflow-x:hidden}@media(hover:none){body{background-attachment:scroll}}@media(max-width:600px){header h1{font-size:1rem}.sl{height:360px}.cap{border-radius:34px;padding:16px}}</style></head><body>'''),
 ("const sb=(typeof SUPABASE_URL",r'''if("scrollRestoration"in history)history.scrollRestoration="manual";window.scrollTo(0,0);const sb=(typeof SUPABASE_URL''')])

NEWLOGIN=r'''let cap={};
function newCap(){cap={a:Math.floor(Math.random()*9)+1,b:Math.floor(Math.random()*9)+1};if($("cq"))$("cq").textContent=cap.a+" + "+cap.b+" = ?"}
function login(){app.innerHTML=`<div class="box" style="max-width:380px;margin:10vh auto 0"><div style="text-align:center;font-size:2.4rem">&#128274;</div><h2 style="text-align:center">Admin login</h2><small>Email</small><input id="e" type="email" placeholder="Email" autocomplete="username"><small>Password</small><div style="position:relative"><input id="p" type="password" placeholder="Password" autocomplete="current-password" style="padding-right:48px" onkeydown="if(event.key==='Enter')doLogin()"><button type="button" id="eye" onclick="toggleEye()" style="position:absolute;right:4px;top:6px;background:none;font-size:1.2rem;padding:4px 8px">&#128065;</button></div><small>Security question: <b id="cq"></b></small><input id="cv" type="number" placeholder="Your answer" onkeydown="if(event.key==='Enter')doLogin()"><br><button onclick="doLogin()" style="width:100%;padding:10px">Login</button></div>`;newCap()}
function toggleEye(){const p=$("p"),h=p.type=="password";p.type=h?"text":"password";$("eye").innerHTML=h?"&#128584;":"&#128065;"}
async function doLogin(){if(+$("cv").value!==cap.a+cap.b){note("Wrong answer to the security question");newCap();$("cv").value="";return}const{error}=await sb.auth.signInWithPassword({email:$("e").value,password:$("p").value});if(error){note(error.message);newCap();$("cv").value=""}else panel()}'''
s=open("admin.html",encoding="utf-8").read()
n1=len(re.findall(r'^function login\(\)\{.*$',s,re.M));n2=len(re.findall(r'^async function doLogin\(\)\{.*$',s,re.M))
if n1==1 and n2==1:
    s=re.sub(r'^function login\(\)\{.*$',lambda m:NEWLOGIN,s,flags=re.M)
    s=re.sub(r'^async function doLogin\(\)\{.*$',lambda m:"",s,flags=re.M)
    open("admin.html","w",encoding="utf-8").write(s);print("done admin login")
else: print("!! admin login not found",n1,n2)
