(function(){
if(typeof SUPABASE_URL==="undefined"||!SUPABASE_URL.startsWith("http")||typeof supabase==="undefined")return;
const xb=supabase.createClient(SUPABASE_URL,SUPABASE_ANON_KEY),$=id=>document.getElementById(id);
const esc=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
let S={phone:"+91-8937827865",hours_days:"Monday to Sunday - 7 days open",hours_time:"Please call us for timings",hours_emergency:"24/7 emergency service",hours_note:"Home sample collection available"},T=[],IMG={};
const css=document.createElement("style");css.textContent=`
.xs{max-width:1050px;margin:0 auto;padding:22px 14px;color:#e8efec;font-family:system-ui,"Segoe UI",Arial,sans-serif}
.xs h2{color:#ffc928;margin:0 0 14px;font-size:1.4rem}.xs h2:after{content:"";display:block;width:46px;height:4px;background:#2e9d77;border-radius:3px;margin-top:6px}
.xf{display:grid;grid-template-columns:1fr 1fr;gap:12px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:18px;padding:18px}
.xf label{font-size:.82rem;font-weight:600;display:block;margin-bottom:4px}
.xf input,.xf select,.xf textarea{width:100%;padding:12px;border-radius:10px;border:1px solid #ffffff44;background:#fffffff2;color:#1d1d1d;font:inherit;font-size:16px;min-height:46px}
.xf .w{grid-column:1/-1}.xb{background:#ffc928;color:#1d1d1d;border:0;border-radius:24px;padding:12px 22px;font-weight:800;cursor:pointer;font-size:1rem;text-decoration:none;display:inline-block;margin:4px 6px 4px 0}.xb.g{background:#25d366;color:#fff}
@media(max-width:600px){.xf{grid-template-columns:1fr;padding:14px}.xb{width:100%;text-align:center;margin:4px 0}}
.xh{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:8px}
.xh div{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-left:4px solid #ffc928;border-radius:12px;padding:12px 14px}.xh small{display:block;opacity:.75;font-size:.75rem}
#xm{margin-top:12px}.xok,.xerr{border-radius:12px;padding:14px}.xok{background:#1b6b52}.xerr{background:#8a2a2a}
#xfab{position:fixed;left:10px;bottom:10px;z-index:20;box-shadow:0 4px 14px #000a;font-size:.85rem;padding:10px 16px;margin:0;width:auto}`;
document.head.appendChild(css);const css2=document.createElement("style");css2.textContent=`.xh .xw{grid-column:1/-1}.xh .xw .xr{background:none!important;border:0!important;border-bottom:1px dashed rgba(255,255,255,.15)!important;border-radius:0!important;padding:6px 0!important;display:flex;justify-content:space-between}.xh .xw .xr.xt{color:#ffc928;font-weight:700}.xh .xw .xr i{color:#ff9a9a;font-style:normal}`;document.head.appendChild(css2);
const sec=document.createElement("section");sec.id="appointment";sec.className="xs";
sec.innerHTML=`<h2>Working hours</h2><div class="xh" id="xh"></div><h2 style="margin-top:28px">Request an Appointment</h2>
<form class="xf" id="xf"><div><label>First name *</label><input id="xfn" required maxlength="80" autocomplete="given-name"></div><div><label>Last name</label><input id="xln" maxlength="80" autocomplete="family-name"></div>
<div><label>Phone *</label><input id="xph" type="tel" required maxlength="20" inputmode="tel" autocomplete="tel"></div><div><label>E-mail (optional)</label><input id="xem" type="email" maxlength="120" autocomplete="email"></div>
<div><label>Date *</label><input id="xdt" type="date" required></div><div><label>Time *</label><input id="xtm" type="time" required></div>
<div class="w"><label>Test or package (optional)</label><select id="xts"><option value="">- Not sure / general checkup -</option></select></div>
<div class="w"><label>Your message</label><textarea id="xms" rows="3" maxlength="1000" placeholder="Tell us anything we should know"></textarea></div>
<input id="xhp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">
<div class="w"><button class="xb" type="submit" id="xsb">&#128197; Make an Appointment</button><a class="xb g" id="xwa" href="#" target="_blank" rel="noopener">&#128172; Send on WhatsApp</a></div></form><div id="xm"></div>`;
const anchor=$("contact")||document.querySelector("footer");
anchor?anchor.parentNode.insertBefore(sec,anchor):document.body.appendChild(sec);
const td0=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,10);$("xdt").min=td0;$("xdt").value=td0;
const wa=m=>"https://wa.me/"+S.phone.replace(/\D/g,"")+"?text="+encodeURIComponent(m);
const msg=()=>"Hello We Care Pathlabs, I want an appointment.\nName: "+($("xfn").value+" "+$("xln").value).trim()+"\nPhone: "+$("xph").value+"\nDate: "+$("xdt").value+"\nTime: "+$("xtm").value+($("xts").value?"\nTest: "+$("xts").value:"")+($("xms").value?"\nMessage: "+$("xms").value:"");
const upd=()=>{$("xwa").href=wa(msg());const m=closedMsg($("xdt").value,$("xtm").value),b=$("xm");if(m)b.innerHTML='<div class="xerr">'+esc(m)+'</div>';else if(b.firstChild&&b.firstChild.className=="xerr")b.innerHTML=""};
["input","change"].forEach(e=>$("xf").addEventListener(e,upd));
function show(h,err){const m=$("xm");m.innerHTML='<div class="'+(err?"xerr":"xok")+'">'+h+'</div>';m.scrollIntoView({behavior:"smooth",block:"center"})}
$("xf").onsubmit=async e=>{e.preventDefault();if($("xhp").value)return;
let last=0;try{last=+localStorage.getItem("x_last")||0}catch(_){}
if(Date.now()-last<30000){show("Please wait a few seconds before sending again.",1);return}
const ph=$("xph").value.replace(/[^\d+]/g,"");if(ph.replace(/\D/g,"").length<10){show("Please enter a valid phone number.",1);return}
const dc=closedMsg($("xdt").value,$("xtm").value);if(dc){show(esc(dc),1);return}const row={first_name:$("xfn").value.trim(),last_name:$("xln").value.trim()||null,phone:ph,email:$("xem").value.trim()||null,appt_date:$("xdt").value,appt_time:$("xtm").value,test_name:$("xts").value||null,message:$("xms").value.trim()||null};
const w=wa(msg());$("xsb").disabled=true;
try{const{error}=await xb.from("appointments").insert(row);if(error)throw error;try{localStorage.setItem("x_last",Date.now())}catch(_){}
$("xf").reset();upd();show("&#10003; Thank you "+esc(row.first_name)+"! Your appointment request was sent. We will call you to confirm.<br><br><a class=\"xb g\" target=\"_blank\" rel=\"noopener\" href=\""+esc(w)+"\">&#128172; Also send on WhatsApp</a>")}
catch(err){show("We could not send this online right now. Please tap the green WhatsApp button below the form instead, or call us.",1)}
$("xsb").disabled=false};
const fb=document.createElement("a");fb.id="xfab";fb.className="xb";fb.href="#appointment";fb.innerHTML="&#128197; Book appointment";document.body.appendChild(fb);
fb.onclick=e=>{e.preventDefault();sec.scrollIntoView({behavior:"smooth"})};
document.addEventListener("click",e=>{const n=$("nav");if(n&&n.classList.contains("open")&&!n.contains(e.target)&&!e.target.closest("#mb"))n.classList.remove("open")});document.addEventListener("keydown",e=>{if(e.key==="Escape"){const n=$("nav");n&&n.classList.remove("open")}});window.addEventListener("scroll",()=>{const n=$("nav");n&&n.classList.remove("open")},{passive:true});
const nv=$("nav");if(nv&&nv.tagName=="NAV"){const a=document.createElement("a");a.href="#appointment";a.textContent="Make an appointment";nv.insertBefore(a,nv.firstChild);const c=document.createElement("a");c.href="#";c.innerHTML="&#10005; Close menu";c.onclick=ev=>{ev.preventDefault();nv.classList.remove("open")};nv.insertBefore(c,nv.firstChild)}
function t12(t){if(!t)return"";const p=t.split(":").map(Number);return(p[0]%12||12)+":"+String(p[1]).padStart(2,"0")+(p[0]<12?" AM":" PM")}
function wk(){try{return JSON.parse(S.week)}catch(e){return null}}
const DK=["sun","mon","tue","wed","thu","fri","sat"],DN=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
function closedMsg(d,t){const w=wk();if(!w||!d)return"";const i=new Date(d+"T12:00:00").getDay(),x=w[DK[i]];if(!x)return"";
if(!x.o)return"We are closed on "+DN[i]+"s. Please choose another day (for an emergency, please call us).";
if(x.f&&x.t&&t&&(t<x.f||t>x.t))return"On "+DN[i]+" we are open "+t12(x.f)+" to "+t12(x.t)+". Please choose a time in between.";return""}
function hours(){const w=wk(),td=new Date().getDay();let rows="";
if(w){rows='<div class="xw"><small>&#128197; Weekly schedule</small>'+[1,2,3,4,5,6,0].map(i=>{const x=w[DK[i]]||{o:1};return'<div class="xr'+(i==td?" xt":"")+'"><b>'+DN[i]+(i==td?" (today)":"")+'</b><span>'+(x.o?(x.f&&x.t?t12(x.f)+" - "+t12(x.t):"Open"):"<i>Closed</i>")+'</span></div>'}).join("")+'</div>'}
else rows="<div>&#128197; <small>Working days</small><b>"+esc(S.hours_days)+"</b></div><div>&#9200; <small>Timings</small><b>"+esc(S.hours_time)+"</b></div>";
$("xh").innerHTML=rows+[["&#128680;","Emergency",S.hours_emergency],["&#127968;","Sample collection",S.hours_note]].filter(x=>x[2]).map(x=>"<div>"+x[0]+" <small>"+x[1]+"</small><b>"+esc(x[2])+"</b></div>").join("")}
function fillTests(){$("xts").innerHTML='<option value="">- Not sure / general checkup -</option>'+T.map(t=>"<option>"+esc(t.name)+"</option>").join("");
const p=new URLSearchParams(location.search).get("test");if(p)$("xts").value=p}
function apply(){document.querySelectorAll('[style*="images/"]').forEach(el=>{const s=el.getAttribute("style"),n=s.replace(/images\/([a-z0-9_-]+)\.jpg/gi,(m,k)=>IMG[k]||m);if(n!==s)el.setAttribute("style",n)});
const m={};T.forEach(t=>{if(t.image_url)m[t.name.trim()]=t.image_url});
document.querySelectorAll(".card").forEach(c=>{const h=c.querySelector("h3"),im=c.querySelector(".im");if(!h||!im)return;const u=m[h.textContent.trim()];if(u&&im.dataset.ov!==u){im.style.backgroundImage="url('"+u+"')";im.dataset.ov=u}})}
function maskEmail(){const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),L=[];while(w.nextNode())L.push(w.currentNode);
L.forEach(n=>{if(false&&!/^(SCRIPT|STYLE|TEXTAREA)$/.test(n.parentNode.nodeName))n.nodeValue=n.nodeValue.replace(/([\w.+-]+)@gmail\.com/gi,"$1")})}
let tm;new MutationObserver(()=>{clearTimeout(tm);tm=setTimeout(()=>{apply();maskEmail()},80)}).observe(document.body,{childList:true,subtree:true});
async function load(){try{const r=await Promise.all([xb.from("settings").select("*"),xb.from("tests").select("name,image_url").eq("active",true).order("id"),xb.from("site_images").select("*")]);
(r[0].data||[]).forEach(x=>S[x.key]=x.value);T=r[1].data||[];(r[2].data||[]).forEach(x=>IMG[x.slot]=x.url)}catch(e){}
hours();fillTests();upd();apply();maskEmail()}
hours();maskEmail();load();
setTimeout(()=>{const n=$("nm");if(n&&n.textContent&&!$("xts").value){$("xts").value=n.textContent.trim();upd()}},1500);
if(/[?&]book=1/.test(location.search))window.addEventListener("load",()=>setTimeout(()=>sec.scrollIntoView(),500));
})();
