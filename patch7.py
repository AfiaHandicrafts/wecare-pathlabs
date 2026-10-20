f="index.html";s=open(f,encoding="utf-8").read()
if '["full body","fullbody"]' in s: print("index.html already has it")
elif s.count("const KW=[[")==1:
    s=s.replace("const KW=[[",'const KW=[["full body","fullbody"],[',1);open(f,"w",encoding="utf-8").write(s);print("ok: index.html")
else: print("!! KW line not found in index.html")
f="fetchcommons2.py";s=open(f,encoding="utf-8").read()
ADD='Q.update({"fullbody":["full body health checkup","health screening medical checkup","annual physical examination","doctor medical checkup"]})\n'
if '"fullbody"' in s: print("fetchcommons2.py already has it")
elif s.count("BAD=re.compile(")==1:
    s=s.replace("BAD=re.compile(",ADD+"BAD=re.compile(",1);open(f,"w",encoding="utf-8").write(s);print("ok: fetchcommons2.py")
else: print("!! BAD line not found in fetchcommons2.py")
