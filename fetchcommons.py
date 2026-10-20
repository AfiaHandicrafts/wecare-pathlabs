import sys,json,os,re,time,urllib.request,urllib.parse
pick=int(sys.argv[1]) if len(sys.argv)>1 else 0
only=sys.argv[2] if len(sys.argv)>2 else ""
UA={"User-Agent":"WeCarePathlabsSite/1.0 (small lab website)"}
Q={"microscope":"microscope pathology laboratory","doctor":"doctor stethoscope","pathologist":"medical laboratory technician","bloodtest":"nurse drawing blood venipuncture","patient":"doctor patient consultation","checkup":"doctor examining patient","glucose":"blood glucose meter test","heart":"doctor stethoscope heart","thyroid":"thyroid examination neck","vitamin":"vitamin pills supplements","urine":"urine sample specimen cups","woman":"pregnant woman doctor","senior":"elderly patient doctor"}
BAD=re.compile(r"diagram|logo|map|chart|drawing|painting|illustration|poster|stamp|cartoon|statue|icon|screenshot|scheme|anatomy|engraving|woodcut",re.I)
OKL=re.compile(r"^(CC0|Public domain|PD|CC BY)",re.I)
def api(p):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p)
    return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read())
os.makedirs("images",exist_ok=True)
for n,q in Q.items():
    if only and n!=only: continue
    f="images/"+n+".jpg"
    if os.path.exists(f) and os.path.getsize(f)>20000 and not only:
        print("have",n); continue
    try:
        d=api({"action":"query","format":"json","generator":"search","gsrnamespace":6,"gsrsearch":q+" filetype:bitmap","gsrlimit":40,"prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":1280})
        c=[]
        for p in d.get("query",{}).get("pages",{}).values():
            i=p["imageinfo"][0]; m=i.get("extmetadata",{}); lic=m.get("LicenseShortName",{}).get("value","")
            if i["mime"]!="image/jpeg" or i["width"]<1200 or i["width"]<i["height"] or BAD.search(p["title"]) or not OKL.search(lic): continue
            c.append((p.get("index",0),p,i,lic,re.sub("<[^>]+>","",m.get("Artist",{}).get("value","unknown"))))
        c.sort(key=lambda t:t[0])
        _,p,i,lic,art=c[min(pick,len(c)-1)]
        open(f,"wb").write(urllib.request.urlopen(urllib.request.Request(i["thumburl"],headers=UA),timeout=60).read())
        open("credits.txt","a").write("%s: %s by %s (%s) %s\n"%(n,p["title"],art,lic,i["descriptionurl"]))
        print("ok",n,"-",p["title"],"-",lic)
    except Exception as e: print("FAILED",n,e)
    time.sleep(2)
print("finished")
