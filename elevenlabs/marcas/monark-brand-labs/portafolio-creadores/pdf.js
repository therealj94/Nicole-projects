const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
await p.goto('file://'+process.cwd()+'/port.html');await p.waitForTimeout(800);
await p.pdf({path:'Portafolio_Kassandra_Lenyn.pdf',width:'13.333in',height:'7.5in',printBackground:true});
const els=await p.$$('.pg');for(let i=0;i<els.length;i++)await els[i].screenshot({path:`pv_${i+1}.png`});await b.close();})();
