const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const cards=JSON.parse(fs.readFileSync(process.argv[2]||'cards.json'));const T=cards.length;
const css=`@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,800;1,9..144,500&family=Inter:ital,wght@0,400;0,500;0,600;1,500&family=JetBrains+Mono:wght@500&display=block');
*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;background:#f5ecdc;font-family:Inter,sans-serif;color:#2a211b;overflow:hidden;position:relative}
.ph{height:770px;background-size:cover;position:relative}
.ph:after{content:"";position:absolute;inset:auto 0 0 0;height:60px;background:linear-gradient(transparent,rgba(245,236,220,.0))}
.pill{position:absolute;top:36px;left:40px;background:#f5ecdc;color:#2a211b;font:500 22px 'JetBrains Mono',monospace;letter-spacing:.12em;padding:12px 18px;border-radius:999px;box-shadow:0 4px 18px rgba(0,0,0,.25)}
.panel{padding:44px 64px 0;position:relative}
.w{font-family:Fraunces,serif;font-weight:800;font-size:112px;line-height:1;color:#c4231c;letter-spacing:-.02em}
.cat{font:italic 500 32px Fraunces,serif;color:#8a7a66;margin-top:14px}
.def{font-size:38px;line-height:1.32;margin-top:22px;font-weight:500;max-width:930px}
.ej{margin-top:22px;border-left:6px solid #1f9f98;padding-left:22px;font:italic 500 32px/1.4 Inter,sans-serif;color:#3d342c;max-width:930px}
.ej b{font:600 20px 'JetBrains Mono',monospace;font-style:normal;letter-spacing:.12em;color:#1f9f98;display:block;margin-bottom:4px}
.foot{position:absolute;left:64px;right:64px;bottom:36px;display:flex;align-items:center;justify-content:space-between;font:500 22px 'JetBrains Mono',monospace;color:#8a7a66;letter-spacing:.06em}
.foot img{height:64px}`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
const logo='data:image/png;base64,'+fs.readFileSync('logo.png').toString('base64');
const OUT=process.argv[3]||'out';fs.mkdirSync(OUT,{recursive:true});
for(let i=0;i<T;i++){const c=cards[i];const im='data:image/png;base64,'+fs.readFileSync(c.img).toString('base64');
const html=`<style>${css}</style><div class="ph" style="background-image:url(${im});background-position:${c.pos} 50%"><div class="pill">DICCIONARIO CATRACHO</div></div>
<div class="panel"><div class="w">${c.w}</div><div class="cat">${c.cat}</div><div class="def">${c.def}</div><div class="ej"><b>EJEMPLO</b>“${c.ej}”</div></div>
<div class="foot"><img src="${logo}"><span>@honduras.secreta · ${String(i+1).padStart(2,'0')}/${String(T).padStart(2,'0')}</span></div>`;
await p.setContent(html,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const h=await p.evaluate(()=>document.querySelector('.ej').getBoundingClientRect().bottom);
await p.screenshot({path:OUT+`/dicc_${String(i+1).padStart(2,'0')}.png`});console.log(i+1,c.w,'ej bottom',Math.round(h));}
await b.close()})();
