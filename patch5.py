import shutil, sys
f = "index.html"
s = open(f, encoding="utf-8").read()
shutil.copy(f, "index.backup.html")
bad = 0

def rep(old, new, label):
    global s, bad
    if s.count(old) != 1:
        print("!! not applied:", label); bad += 1; return
    s = s.replace(old, new); print("ok:", label)

rep('const sb=(typeof SUPABASE_URL!=="undefined"&&',
    'const sb=(typeof supabase!=="undefined"&&typeof SUPABASE_URL!=="undefined"&&', "supabase crash guard")
rep('.filter(t=>t.length>2);if(!ts.length)return true;', '.filter(t=>t.length>1);if(!ts.length)return true;', "2-letter search terms")
rep('$("none").style.display=l.length?"none":"block";',
    '$("none").style.display=l.length?"none":"block";if($("rc"))$("rc").textContent=q.trim()?(l.length?l.length+" found":"No match"):"";', "result count")
rep('$("q").oninput=e=>{q=e.target.value;if(q)cat="All";chips();grid()};',
    '''const doSearch=()=>{q=$("q").value;if(q.trim())cat="All";chips();grid();if(q.trim().length>1){const r=$("tests").getBoundingClientRect();if(r.top>innerHeight*.6||r.top<0)$("tests").scrollIntoView({behavior:"smooth",block:"start"})}};
$("q").addEventListener("input",doSearch);$("q").addEventListener("search",doSearch);$("q").addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();$("q").blur()}});''', "search handler")
rep('<section class="ctr"><h2>Book a test online</h2><input id="q" placeholder="Search a test: body checkup, thyroid, sugar, vitamin D..." autocomplete="off">',
    '<div class="sbar"><input id="q" type="search" enterkeyhint="search" placeholder="Search a test: thyroid, sugar, vitamin D..." autocomplete="off"><small id="rc"></small></div>\n<section class="ctr"><h2>Book a test online</h2>', "sticky search bar")
rep('window.addEventListener("load",()=>window.scrollTo(0,0));',
    'window.addEventListener("load",()=>window.scrollTo(0,0));window.addEventListener("pageshow",()=>window.scrollTo(0,0));', "open from top")
rep('<a class="btn" id="fab"',
    '<div class="mbar"><a id="bc" href="#">&#128222; Call</a><a id="bw" href="#" target="_blank" rel="noopener">WhatsApp</a><a href="#tests">&#129514; Tests</a></div>\n<a class="btn" id="fab"', "bottom bar html")
rep('$("fab").href=wa("Hello, please call me back.")}',
    '$("fab").href=wa("Hello, please call me back.");$("bc").href="tel:"+d;$("bw").href=wa("Hello We Care Pathlabs, I want to book a test.")}', "bottom bar links")
rep('load();setInterval(feed,4500);',
    'const hh=()=>document.documentElement.style.setProperty("--hh",document.querySelector("header").offsetHeight+"px");hh();addEventListener("resize",hh);addEventListener("load",hh);\nload();setInterval(feed,4500);', "header height var")

CSS = '''
/* ---- patch5: search + phone/tablet polish ---- */
:root{--hh:60px}
.sbar{position:sticky;top:var(--hh);z-index:14;padding:10px max(14px,calc((100% - 1050px)/2)) 6px;background:rgba(10,42,33,.94);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.sbar #q{display:block;width:100%;max-width:none;-webkit-appearance:none;appearance:none;box-shadow:0 6px 18px #0006}
#rc{display:block;text-align:center;font-weight:700;color:var(--y);min-height:1.1em;margin-top:5px;font-size:.8rem}
#tests{scroll-margin-top:calc(var(--hh) + 78px)}
.mbar{display:none}
.card .b .btn{text-align:center}
@media(max-width:800px){
 .mbar{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;position:fixed;left:0;right:0;bottom:0;z-index:25;background:rgba(6,26,20,.96);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);border-top:2px solid var(--y);padding:8px 10px calc(8px + env(safe-area-inset-bottom))}
 .mbar a{text-align:center;text-decoration:none;font-weight:700;font-size:.85rem;padding:11px 4px;border-radius:12px;background:var(--gl);border:1px solid var(--ln)}
 .mbar a:nth-child(2){background:#25d366;color:#05301a;border:0}
 #fab{display:none}
 body{padding-bottom:calc(76px + env(safe-area-inset-bottom))}
}
@media(max-width:600px){
 .sl{height:350px;margin:10px auto}
 .grid{grid-template-columns:repeat(2,1fr);gap:10px}
 #contact .grid{grid-template-columns:1fr}
 .card{padding:10px;border-radius:14px;gap:6px}
 .im{height:92px}
 .card h3{font-size:.92rem;line-height:1.25}
 .card .new{font-size:1.1rem}
 .card .b{flex-direction:column}
 .card .b .btn{width:100%;padding:10px 6px;font-size:.82rem}
 .cc div{font-size:1.6rem}.cc small{font-size:.7rem}
 .chips{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding-bottom:4px}
 .chips::-webkit-scrollbar{display:none}
 .chip{flex:none;white-space:nowrap}
 .tr{grid-template-columns:1fr 1fr;gap:8px}.tr div{padding:10px;font-size:.78rem}
 #q{font-size:16px;padding:13px 18px}
}
@media(min-width:601px) and (max-width:1000px){.grid{grid-template-columns:repeat(3,1fr)}}
'''
rep('</style>', CSS + '</style>', "css")

if bad:
    print("\n%d step(s) failed - index.html NOT changed. Send me the !! lines." % bad); sys.exit(1)
open(f, "w", encoding="utf-8").write(s)
print("\nAll done. Backup saved as index.backup.html")
