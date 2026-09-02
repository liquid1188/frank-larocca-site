import { chromium } from 'playwright';
import fs from 'fs';
const b = await chromium.launch({args:['--no-sandbox']});
const pages=['/','/works/','/works/mass-of-the-americas/','/works/alleluia/','/listen/','/recordings/','/performances/','/biography/','/reviews/','/news/','/news/ever-ancient-ever-new/','/directors/','/press-kit/','/contact/','/404.html'];
const issues=[];
for (const w of [390,1280]) {
  const p = await b.newPage({viewport:{width:w,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error') errs.push(m.text())});
  for (const url of pages) {
    errs.length=0;
    const r=await p.goto('http://localhost:8080'+url,{waitUntil:'load'}).catch(e=>null); await p.waitForTimeout(300);
    const res = await p.evaluate(()=>{
      const out={};
      out.sw=document.documentElement.scrollWidth; out.vw=innerWidth;
      out.title=document.title; out.h1=document.querySelectorAll('h1').length;
      out.noAlt=[...document.images].filter(i=>!i.hasAttribute('alt')).map(i=>i.getAttribute('src'));
      out.broken=[...document.images].filter(i=>i.complete && i.naturalWidth===0 && !i.src.includes('youtube')).map(i=>i.getAttribute('src'));
      out.tinyText=[...document.querySelectorAll('p,a,span,li,cite')].filter(e=>{const s=getComputedStyle(e);return parseFloat(s.fontSize)<12 && e.innerText.trim()}).length;
      out.smallTap=[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0 && (r.height<32)}).length;
      out.desc=document.querySelector('meta[name=description]')?.content?.length||0;
      out.emptyLinks=[...document.querySelectorAll('a')].filter(a=>!a.getAttribute('href')||a.getAttribute('href')==='#').length;
      out.hrefs=[...document.querySelectorAll('a[href^="/"]')].map(a=>a.getAttribute('href'));
      return out;
    });
    issues.push({w,url,status:r&&r.status(),...res,errs:[...errs]});
  }
  await p.close();
}
await b.close();
fs.writeFileSync('/tmp/audit.json',JSON.stringify(issues));
for (const i of issues) { const flags=[]; if(i.sw>i.vw) flags.push('OVERFLOW '+i.sw); if(i.h1!==1) flags.push('h1='+i.h1); if(i.noAlt.length) flags.push('noalt '+i.noAlt.length); if(i.broken.length) flags.push('broken '+i.broken.join(',')); if(i.tinyText) flags.push('tiny '+i.tinyText); if(i.smallTap) flags.push('tap<32 '+i.smallTap); if(i.desc<50) flags.push('desc '+i.desc); if(i.emptyLinks) flags.push('emptylinks '+i.emptyLinks); if(i.errs.length) flags.push('JS '+i.errs.join(' | ').slice(0,120)); console.log(i.w, i.url, i.status, flags.join('; ')||'ok'); }
