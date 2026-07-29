const {chromium}=require('playwright');
const fs=require('fs');
const MAP={'Bangkok':'bangkok','Phuket':'phuket','Koh-Samui':'samui','Pattaya':'pattaya','Penang':'penang','Kuala-Lumpur':'kl','Hanoi':'hanoi','Da-Nang':'danang','Saigon':'saigon','Sanur':'sanur','Gili-Air':'giliair','Ubud':'ubud','Boracay':'boracay','Cebu':'cebu','Bohol':'bohol','Seville':'sevilla','Madrid':'madrid','Fuengirola':'fuengirola','Malaga':'malaga','Miami-Beach':'miami','Fort-Lauderdale':'fortlauderdale','Barcelona':'barcelona','Mallorca':'mallorca','Las-Palmas':'grancanaria','Tenerife':'tenerife','Alicante':'alicante','Valencia':'valencia','Mauritius':'mauritius'};
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const ctx=await b.newContext({viewport:{width:820,height:1200},deviceScaleFactor:2});
 const pg=await ctx.newPage();
 await pg.route('**commons.wikimedia.org**', r=>r.abort());
 fs.mkdirSync('prev2x',{recursive:true});
 for(const [file,id] of Object.entries(MAP)){
   const p='pkg/html/Sama-Sama-'+file+'-Guide.html';
   if(!fs.existsSync(p)){console.log('MISSING',p);continue}
   await pg.goto('file://'+process.cwd()+'/'+p,{waitUntil:'load'});
   const n=await pg.locator('.page').count();
   const el=pg.locator('.page').nth(n-2);
   await el.screenshot({path:'prev2x/'+id+'.png'});
   console.log(id,'pages='+n);
 }
 await b.close();
})();
