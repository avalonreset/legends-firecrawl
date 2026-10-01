#!/usr/bin/env node
const fs=require('fs'),path=require('path');
const {query,DIRECT_CAPABILITIES}=require('./router');
const catalog=JSON.parse(fs.readFileSync(path.join(__dirname,'..','data','alexandria_catalog.json'),'utf8'));
const args=process.argv.slice(2),command=args[0]||'help';
const direct=(p,c)=>!!DIRECT_CAPABILITIES[p]?.includes(c);
async function main(){
 if(command==='audit'||command==='stats'){
  console.log(JSON.stringify({catalogProviders:catalog.providers.length,catalogCapabilities:catalog.providers.reduce((n,p)=>n+p.tools.length,0),acceptedDirectOperations:DIRECT_CAPABILITIES,measuredUserSavings:null,scaleValidated:false},null,2));return;
 }
 if(['providers','list','search','inspect'].includes(command)){
  const term=(args[1]||'').toLowerCase();
  if(['search','inspect'].includes(command)&&!term)throw Error('A search term or provider ID is required');
  const matches=(x)=>[x.id,x.name,x.description,x.capability].filter(Boolean).join(' ').toLowerCase().includes(term);
  const providers=catalog.providers.filter(p=>command==='inspect'?p.id===term:command==='search'?matches(p)||p.tools.some(matches):true);
  if(command==='inspect'&&!providers.length)throw Error('Unknown provider');
  const full=args.includes('--full');
  console.log(JSON.stringify(providers.map(p=>({... (full?p:{id:p.id,name:p.name,description:(p.description||'').slice(0,300),catalogPath:path.join(__dirname,'..','data','alexandria_catalog.json')}),tools:(command==='search'&&!matches(p)?p.tools.filter(matches):p.tools).map(t=>({... (full?t:{capability:t.capability,name:t.name}),listedCredits:t.creditsCost??null,route:'paid_preview'}))})),null,2));return;
 }
 if(command==='query'){
  if(!args[1]||!args[2])throw Error('query requires provider and capability');
  const flags={},allowed=new Set(['--preview','--confirm','--gateway','--no-save','--json']);let options={};
  for(let i=3;i<args.length;i++){
   if(args[i]==='--options'){if(!args[i+1])throw Error('Missing options JSON');options=JSON.parse(args[++i]);}
   else if(allowed.has(args[i]))flags[args[i].slice(2)]=true;
   else throw Error('Unknown flag: '+args[i]);
  }
  const result=await query(args[1],args[2],options,flags);
  if(result.status==='ok'&&!flags['no-save'])result.capture=require('./encapsulation').encapsulate(result);
  console.log(JSON.stringify(result,null,2));
  if(!['ok','preview'].includes(result.status))process.exitCode=2;
  return;
 }
 if(command==='captures'){
  const root=path.join(process.env.LEGENDS_FIRECRAWL_CAPTURE_ROOT||path.resolve(__dirname,'..'),'var','captures');
  const captures=[],errors=[];
  if(fs.existsSync(root))for(const entry of fs.readdirSync(root,{withFileTypes:true})){
   if(!entry.isDirectory())continue;
   for(const name of fs.readdirSync(path.join(root,entry.name)).filter(n=>n.endsWith('.raw.json'))){
    const rawFilePath=path.join(root,entry.name,name);
    try{const raw=JSON.parse(fs.readFileSync(rawFilePath,'utf8')),m=raw.metadata||{};
     captures.push({provider:m.provider,capability:m.capability,source:m.source,status:raw.response?.status??null,creditsUsed:m.creditsBurned??raw.response?.creditsUsed??null,timestamp:m.timestamp,rawFilePath});
    }catch{errors.push({rawFilePath,reason:'unreadable_capture'});}
   }
  }
  captures.sort((a,b)=>(b.timestamp||'').localeCompare(a.timestamp||''));
  console.log(JSON.stringify({captures:captures.slice(0,50),total:captures.length,limit:50,errors},null,2));return;
 }
 if(command!=='help')throw Error('Unknown command');
 console.log('legends-firecrawl Alexandria: offline catalog and bounded query routing\nCommands: audit, providers, search <term>, inspect <provider> [--full], captures\nquery <provider> <capability> [--options JSON] [--preview] [--gateway] [--confirm] [--no-save] [--json]\nAll queries use official Firecrawl and require --confirm. No direct-source substitutes or savings claims.');
}
main().catch(error=>{console.error(JSON.stringify({status:'error',message:error.message}));process.exitCode=1;});
