import re
f="fetchcommons2.py";s=open(f,encoding="utf-8").read()
new='Q.update({"fullbody":["pediatrician examining child","doctor examining child stethoscope","doctor checking child health","pediatric checkup child doctor","child medical examination"]})'
s2,n=re.subn(r'^Q\.update\(\{"fullbody":.*\}\)$',lambda m:new,s,flags=re.M)
if n==1: open(f,"w",encoding="utf-8").write(s2);print("ok: child photo search set")
else: print("!! fullbody line not found")
