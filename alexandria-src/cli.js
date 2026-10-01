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
  const providers=catalog.providers.filter(p=>command==='inspect'?p.id===term:command==='search'?JSON.stringify(p).toLowerCase().includes(term):true);
  if(command==='inspect'&&!providers.length)throw Error('Unknown provider');
  console.log(JSON.stringify(providers.map(p=>({...p,tools:p.tools.map(t=>({...t,listedCredits:t.creditsCost??null,route:direct(p.id,t.capability)?'accepted_direct':'paid_preview'}))})),null,2));return;
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
  const root=path.join(__dirname,'..','var','captures');
  console.log(fs.existsSync(root)?fs.readdirSync(root).join('\n'):'No captures');return;
 }
 if(command!=='help')throw Error('Unknown command');
 console.log('legends-firecrawl Alexandria: offline catalog and bounded query routing\nCommands: audit, providers, search <term>, inspect <provider>, captures\nquery <provider> <capability> [--options JSON] [--preview] [--gateway] [--confirm] [--no-save] [--json]\nAll queries use official Firecrawl and require --confirm. No direct-source substitutes or savings claims.');
}
main().catch(error=>{console.error(JSON.stringify({status:'error',message:error.message}));process.exitCode=1;});
