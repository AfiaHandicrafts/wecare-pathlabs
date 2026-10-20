import sys,json,os,urllib.request,urllib.parse
key=sys.argv[1]; pick=int(sys.argv[2]) if len(sys.argv)>2 else 0
Q={"lab":"medical laboratory analyzer machine","tubes":"blood test tubes rack laboratory","tray":"laboratory sample tray vials","microscope":"microscope laboratory scientist","doctor":"doctor stethoscope portrait","pathologist":"lab technician white coat laboratory","bloodtest":"nurse taking blood sample patient","patient":"happy patient smiling doctor clinic","checkup":"doctor checking patient health checkup"}
os.makedirs("images",exist_ok=True)
UA={"User-Agent":"Mozilla/5.0"}
for n,q in Q.items():
    try:
        u="https://api.pexels.com/v1/search?"+urllib.parse.urlencode({"query":q,"orientation":"landscape","per_page":8})
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"Authorization":key,**UA})))
        p=d["photos"][min(pick,len(d["photos"])-1)]
        r=urllib.request.urlopen(urllib.request.Request(p["src"]["large2x"],headers=UA))
        open("images/"+n+".jpg","wb").write(r.read())
        print("ok",n,"-",p["photographer"],p["url"])
    except Exception as e:
        print("FAILED",n,e)
