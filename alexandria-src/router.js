// Exact capability routing. Catalog classification is not implementation proof.
const fs = require('fs');
const path = require('path');

const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'alexandria_catalog.json'), 'utf8'));
const NATIVE_ADAPTERS = Object.freeze({});
const DIRECT_CAPABILITIES = Object.freeze({});
function getProviderSafety(providerId) {
 return {id:providerId,ipSafety:'SOURCE_LIMITS_APPLY',recommendedRoute:'Official Firecrawl only',ipRisk:'No unlimited-access or IP-shield guarantee'};
}
function plan(providerId,capability,options={},flags={}) {
 if(!options || typeof options!=='object' || Array.isArray(options)) throw new Error('Options must be an object');
 if(flags.dangerDirectIp || flags['danger-direct-ip']) throw new Error('Unverified direct override retired; use managed route');
 const tool=catalog.providers.find(p=>p.id===providerId)?.tools.find(t=>t.capability===capability);
 if(!tool) throw new Error('Unknown provider/capability; inspect official contract');
 return {provider:providerId,capability,routeDecision:'FIRECRAWL_GATEWAY',
  source:'firecrawl-alexandria-gateway',
  coverage:{scope:'single_operation',provider_parity:false},
  listedCredits:tool.creditsCost??null,catalogObservedAt:catalog.extractedAt,
  decisionReason:'Official Firecrawl execution; direct-source substitution is retired.',
  request:{path:'/v2/scrape',body:{alexandria:{provider:providerId,capability,options}}}};
}
function getCredentials(){
 if(process.env.FIRECRAWL_API_KEY) return process.env.FIRECRAWL_API_KEY;
 const location=path.join(process.env.APPDATA||'','firecrawl-cli','credentials.json');
 if(fs.existsSync(location)) return JSON.parse(fs.readFileSync(location,'utf8')).apiKey;
 return null;
}
async function query(providerId,capability,options={},flags={}){
 const proposal=plan(providerId,capability,options,flags);
 if(flags.preview) return {...proposal,status:'preview',creditsUsed:null};
 if(flags.confirm!==true) return {...proposal,status:'confirmation_required',creditsUsed:null};
 const key=getCredentials();if(!key) throw new Error('FIRECRAWL_API_KEY or official CLI credentials required');
 try{
  const res=await fetch('https://api.firecrawl.dev/v2/scrape',{method:'POST',
   headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},
   body:JSON.stringify(proposal.request.body),signal:AbortSignal.timeout(60000)});
  const raw=await res.text();let response;
  try{response=JSON.parse(raw);}catch{return {...proposal,status:'error',creditsUsed:null,httpStatus:res.status,response:raw,requestMayHaveCompleted:true};}
  const items=response?.data?.alexandria,tool=Array.isArray(items)&&items.length===1?items[0]:null;
  const valid=res.ok&&response?.success===true&&tool&&!tool.error&&tool.success!==false&&tool.provider===providerId&&tool.capability===capability&&Object.hasOwn(tool,'data');
  const cost=response?.data?.creditsCost??tool?.creditsCost??null;
  const creditsUsed=typeof cost==='number'&&Number.isFinite(cost)&&cost>=0?cost:null;
  const empty=valid&&(tool.data==null||(Array.isArray(tool.data)&&tool.data.length===0));
  return {...proposal,status:valid?(empty?'empty':'ok'):'error',creditsUsed,httpStatus:res.status,response,data:tool?.data??null};
 }catch(error){return {...proposal,status:'error',creditsUsed:null,data:null,
  error:{type:error.name,message:'Provider transport failed; reconcile before another submission'},requestMayHaveCompleted:true};}
}
module.exports={query,plan,getProviderSafety,NATIVE_ADAPTERS,DIRECT_CAPABILITIES};
