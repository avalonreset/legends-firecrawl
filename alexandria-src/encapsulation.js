const fs=require('fs'),path=require('path'),os=require('os');
const {randomUUID,createHash}=require('crypto');
const MACOS_SYS_LINKS=new Set(['/var','/tmp','/etc']);
function assertNotSymlink(targetPath){
 let cur=path.resolve(targetPath),leaf=true;
 while(true){
  if(!leaf&&process.platform==='darwin'&&MACOS_SYS_LINKS.has(cur)){
   const parent=path.dirname(cur);if(parent===cur)break;cur=parent;continue;
  }
  try{if(fs.lstatSync(cur).isSymbolicLink())throw new Error('Refusing symlink capture path');}
  catch(err){if(err.code!=='ENOENT')throw err;}
  const parent=path.dirname(cur);if(parent===cur)break;cur=parent;leaf=false;
 }
}
function encapsulate(result,root=null){
 const base=path.resolve(root||process.env.LEGENDS_FIRECRAWL_CAPTURE_ROOT||path.join(os.homedir(),'.legends-firecrawl','research'));
 assertNotSymlink(base);
 const stamp=new Date().toISOString(),slug=String(result.provider||'firecrawl').replace(/[^a-zA-Z0-9-]/g,'-');
 const name=stamp.replace(/[:.]/g,'-')+'_'+randomUUID();
 const rawDir=path.join(base,'var','captures',slug),cardDir=path.join(base,'vault','captures',slug);
 assertNotSymlink(rawDir);assertNotSymlink(cardDir);
 fs.mkdirSync(rawDir,{recursive:true});fs.mkdirSync(cardDir,{recursive:true});
 const rawFilePath=path.join(rawDir,name+'.raw.json'),cardFilePath=path.join(cardDir,name+'.md');
 const metadata={timestamp:stamp,provider:result.provider,capability:result.capability,source:result.source,
  request:result.request,workspace:process.env.LEGENDS_WORKSPACE_ID||null,creditsBurned:result.creditsUsed??null};
 const raw=JSON.stringify({metadata,response:result,data:result.data},null,2);
 fs.writeFileSync(rawFilePath,raw,{flag:'wx'});
 const sha256=createHash('sha256').update(raw).digest('hex');
 fs.writeFileSync(cardFilePath,`# Firecrawl capture\n\nObserved: ${stamp}\n\nUnreviewed source material. State: ${result.status||'unknown'}.\n\n[Complete JSON](${path.relative(cardDir,rawFilePath).split(path.sep).join('/')})\n\nSHA-256: ${sha256}\n\nOne response only. Pagination and semantic relevance require review.\n`,{flag:'wx'});
 fs.writeFileSync(rawFilePath.replace(/\.json$/,'.manifest.json'),JSON.stringify({...metadata,status:result.status||'unknown',rawFileName:path.basename(rawFilePath),sha256,bytes:Buffer.byteLength(raw)},null,2),{flag:'wx'});
 return {rawFilePath,cardFilePath,sha256,bytes:Buffer.byteLength(raw)};
}
module.exports={encapsulate};
