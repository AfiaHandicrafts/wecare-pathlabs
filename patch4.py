import re
f="fetchcommons2.py";s=open(f,encoding="utf-8").read()
ADD=r'''Q.update({"cbc":["blood smear","blood cells microscope"],"esr":["erythrocyte sedimentation rate"],"platelets":["platelets blood"],"bloodgroup":["blood type test card","blood group test"],"inr":["INR coagulation meter","coagulation test"],"hba1c":["finger prick blood test"],"lipid":["cholesterol test","cholesterol blood test"],"dengue":["Aedes aegypti mosquito"],"malaria":["Anopheles mosquito"],"hiv":["red ribbon AIDS awareness","HIV test"],"culture":["petri dish bacteria colonies","agar plate bacteria"],"pregtest":["pregnancy test"]})
'''
if s.count("BAD=re.compile(")==1 and "Q.update(" not in s:
    s=s.replace("BAD=re.compile(",ADD+"BAD=re.compile(");open(f,"w",encoding="utf-8").write(s);print("done",f)
else:print("!! fetchcommons2.py not changed (already patched or missing)")
f="index.html";s=open(f,encoding="utf-8").read()
NEW=r'''const KW=[["senior|elder","senior"],["pregnancy test","pregtest"],["pregnan|women|woman","woman"],["hba1c","hba1c"],["diabet|sugar|glucose","glucose"],["lipid","lipid"],["heart|cardiac","heart"],["thyroid|tsh","thyroid"],["vitamin|iron|anaem|b12|ferritin","vitamin"],["urine|stool","urine"],["dengue","dengue"],["malaria","malaria"],["hiv","hiv"],["culture","culture"],["widal|typhoid|crp|hepatitis|fever","microscope"],["liver|kidney|uric|electrolyte","tubes"],["cbc|complete blood","cbc"],["esr","esr"],["platelet","platelets"],["blood group","bloodgroup"],["inr","inr"],["hemoglobin","bloodtest"],["biopsy|fnac|pap smear|psa|ca-125","pathologist"],["men's|male","doctor"],["full body|checkup|health|package|employment","checkup"]];'''
if len(re.findall(r'^const KW=\[.*\];$',s,re.M))==1:
    s=re.sub(r'^const KW=\[.*\];$',lambda m:NEW,s,flags=re.M);open(f,"w",encoding="utf-8").write(s);print("done",f)
else:print("!! KW line not found in index.html")
