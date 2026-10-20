import sys,json,os,re,time,urllib.request,urllib.parse
pick=int(sys.argv[1]) if len(sys.argv)>1 else 0
only=sys.argv[2] if len(sys.argv)>2 else ""
UA={"User-Agent":"WeCarePathlabsSite/1.0 (small lab website)"}
Q={"microscope":["microscope pathology laboratory"],"doctor":["doctor portrait stethoscope smiling","physician white coat portrait","doctor hospital"],"pathologist":["medical laboratory technician"],"bloodtest":["blood sample collection","phlebotomy","blood donation nurse","blood draw"],"patient":["doctor patient consultation"],"checkup":["doctor examining patient"],"glucose":["blood glucose meter test"],"heart":["doctor stethoscope heart"],"thyroid":["thyroid","thyroid ultrasound","endocrinology doctor"],"vitamin":["vitamin pills supplements"],"urine":["urine sample","urine specimen container","urinalysis","urine test strip"],"woman":["pregnant woman ultrasound","pregnant woman clinic","pregnancy checkup"],"senior":["elderly patient doctor clinic","old man doctor consultation","elderly woman doctor"]}
Q.update({"cbc":["blood smear","blood cells microscope"],"esr":["erythrocyte sedimentation rate"],"platelets":["platelets blood"],"bloodgroup":["blood type test card","blood group test"],"inr":["INR coagulation meter","coagulation test"],"hba1c":["finger prick blood test"],"lipid":["cholesterol test","cholesterol blood test"],"dengue":["Aedes aegypti mosquito"],"malaria":["Anopheles mosquito"],"hiv":["red ribbon AIDS awareness","HIV test"],"culture":["petri dish bacteria colonies","agar plate bacteria"],"pregtest":["pregnancy test"]})
BAD=re.compile(r"diagram|logo|map|chart|drawing|painting|illustration|poster|stamp|cartoon|statue|icon|screenshot|scheme|anatomy|engraving|woodcut|Wellcome V\d|wrongly|computer|hard drive|caricature|print|lithograph|etching|satire",re.I)
OKL=re.compile(r"^(CC0|Public domain|PD|CC BY)",re.I)
def api(p):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p)
    return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read())
def cands(q):
    d=api({"action":"query","format":"json","generator":"search","gsrnamespace":6,"gsrsearch":q+" filetype:bitmap","gsrlimit":50,"prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":1280})
    c=[]
    for p in d.get("query",{}).get("pages",{}).values():
        i=p["imageinfo"][0]; m=i.get("extmetadata",{}); lic=m.get("LicenseShortName",{}).get("value","")
        if i["mime"]!="image/jpeg" or i["width"]<1000 or i["width"]<i["height"] or BAD.search(p["title"]) or not OKL.search(lic): continue
        c.append((p.get("index",0),p,i,lic,re.sub("<[^>]+>","",m.get("Artist",{}).get("value","unknown"))))
    return sorted(c,key=lambda t:t[0])
def credit(n,line):
    L=[l for l in open("credits.txt").read().splitlines() if not l.startswith(n+":")] if os.path.exists("credits.txt") else []
    L.append(line); open("credits.txt","w").write("\n".join(L)+"\n")
os.makedirs("images",exist_ok=True)
for n,qs in Q.items():
    if only and n!=only: continue
    f="images/"+n+".jpg"
    if os.path.exists(f) and os.path.getsize(f)>20000 and not only:
        print("have",n); continue
    try:
        c=[]
        for q in qs:
            for x in cands(q):
                if x[1]["title"] not in [y[1]["title"] for y in c]: c.append(x)
            if len(c)>pick: break
            time.sleep(1)
        if not c: print("none found for",n); continue
        _,p,i,lic,art=c[min(pick,len(c)-1)]
        open(f,"wb").write(urllib.request.urlopen(urllib.request.Request(i["thumburl"],headers=UA),timeout=60).read())
        credit(n,"%s: %s by %s (%s) %s"%(n,p["title"],art,lic,i["descriptionurl"]))
        print("ok",n,"-",p["title"],"-",lic)
    except Exception as e: print("FAILED",n,e)
    time.sleep(2)
print("finished")
