import sys,json,os,time,urllib.request,urllib.parse
key=sys.argv[1] if len(sys.argv)>1 else ""
pick=int(sys.argv[2]) if len(sys.argv)>2 else 0
only=sys.argv[3] if len(sys.argv)>3 else ""
UA={"User-Agent":"Mozilla/5.0"}
DIRECT={"lab":8442373,"tubes":8442376,"tray":8442374}
Q={"lab":"medical laboratory equipment","tubes":"blood test tubes","tray":"laboratory samples tray","microscope":"microscope laboratory","doctor":"doctor","pathologist":"laboratory technician","bloodtest":"blood sample nurse","patient":"happy patient doctor","checkup":"doctor patient checkup","glucose":"blood glucose test","heart":"stethoscope heart","thyroid":"thyroid ultrasound doctor","vitamin":"vitamins supplements","urine":"urine sample laboratory","woman":"pregnant woman doctor","senior":"senior patient doctor"}
os.makedirs("images",exist_ok=True)
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
for n,q in Q.items():
    if only and n!=only: continue
    f="images/"+n+".jpg"
    if os.path.exists(f) and os.path.getsize(f)>20000 and pick==0:
        print("have",n); continue
    ok=False
    if n in DIRECT and pick==0:
        try:
            i=DIRECT[n]
            open(f,"wb").write(get("https://images.pexels.com/photos/%d/pexels-photo-%d.jpeg?auto=compress&cs=tinysrgb&w=1280"%(i,i)))
            print("ok",n,"(Pexels)"); ok=True
        except Exception as e: print("direct failed",n,e)
    if not ok and key:
        try:
            u="https://pixabay.com/api/?"+urllib.parse.urlencode({"key":key,"q":q,"image_type":"photo","orientation":"horizontal","per_page":10,"safesearch":"true","min_width":1000})
            h=json.loads(get(u))["hits"]; h=h[min(pick,len(h)-1)]
            open(f,"wb").write(get(h["largeImageURL"]))
            print("ok",n,"(Pixabay)",h["pageURL"]); ok=True
        except Exception as e: print("FAILED",n,e)
    time.sleep(4)
print("finished")
