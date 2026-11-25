const json=(v,status=200)=>Response.json(v,{status,headers:{'cache-control':'no-store'}});
const now=()=>new Date().toISOString();
const kinds=new Set(['series','season','episode','scene','character','setting','object','generation','publication','template','source','task','tool']);
let seeded=false;
async function init(db){
 if(seeded)return;
 const done=await db.prepare("SELECT value FROM metadata WHERE key='seed-v1'").first();
 if(!done){
 for(let i=0;i<SEED.length;i+=40){await db.batch(SEED.slice(i,i+40).map(r=>db.prepare('INSERT OR IGNORE INTO records(id,kind,parent,data,updated_at) VALUES(?,?,?,?,?)').bind(r.id,r.kind,r.parent||null,JSON.stringify(r.data),now())))}
 await db.prepare("INSERT OR IGNORE INTO metadata(key,value) VALUES('seed-v1','1')").run();
 } seeded=true;
}
const row=r=>({...r,data:JSON.parse(r.data)});
export default {async fetch(req,env){
 const u=new URL(req.url),p=u.pathname;
 if(!p.startsWith('/api/'))return new Response(HTML,{headers:{'content-type':'text/html; charset=utf-8','cache-control':'no-cache'}});
 try {
 const db=env.DB;if(!db)return json({error:'Banco de dados indisponível.'},503);
 await init(db);
 if(p==='/api/bootstrap'&&req.method==='GET'){
 const [r,f]=await Promise.all([db.prepare('SELECT * FROM records ORDER BY updated_at,id').all(),db.prepare('SELECT * FROM files ORDER BY created_at DESC').all()]);
 return json({records:r.results.map(row),files:f.results,storage:!!env.BUCKET});
 }
 if(p==='/api/records'&&req.method==='POST'){
 const v=await req.json(); if(!kinds.has(v.kind)||!v.data||typeof v.data!=='object')return json({error:'Registro inválido'},400);
 const id=crypto.randomUUID(),t=now();await db.prepare('INSERT INTO records(id,kind,parent,data,updated_at) VALUES(?,?,?,?,?)').bind(id,v.kind,v.parent||null,JSON.stringify(v.data),t).run();
 return json({id,kind:v.kind,parent:v.parent||null,data:v.data,updated_at:t});
 }
 const rec=p.match(/^\/api\/records\/([^/]+)(\/history)?$/);
 if(rec){
 const id=rec[1],r=await db.prepare('SELECT * FROM records WHERE id=?').bind(id).first();
 if(!r)return json({error:'Registro não encontrado'},404);
 if(rec[2]&&req.method==='GET'){const list=await db.prepare('SELECT * FROM revisions WHERE record_id=? ORDER BY id DESC LIMIT 100').bind(id).all();return json(list.results.map(row))}
 if(req.method==='PATCH'){
 const v=await req.json();if(v.updated_at&&v.updated_at!==r.updated_at)return json({error:'Registro atualizado em outro dispositivo. Recarregue antes de salvar.'},409);
 const data={...JSON.parse(r.data),...v.data}; const t=now();
 const result=await db.batch([db.prepare('INSERT INTO revisions(record_id,data,created_at) VALUES(?,?,?)').bind(id,r.data,t),db.prepare('UPDATE records SET data=?,updated_at=? WHERE id=?').bind(JSON.stringify(data),t,id)]);
 return json({...r,data,updated_at:t});
 }
 }
 if(p==='/api/files'&&req.method==='POST'){
 if(!env.BUCKET)return json({error:'Armazenamento indisponível'},503);
 const fd=await req.formData(),f=fd.get('file');if(!f||typeof f==='string')return json({error:'Arquivo inválido'},400);
 if(f.size>95*1024*1024)return json({error:'Arquivo acima de 95 MB'},413);
 const id=crypto.randomUUID(),t=now(),record_id=String(fd.get('record_id')||''),role=String(fd.get('role')||'Arquivo');
 const type=f.type||'application/octet-stream';await env.BUCKET.put(id,f.stream(),{httpMetadata:{contentType:type}});
 await db.prepare('INSERT INTO files(id,record_id,name,type,size,created_at,role) VALUES(?,?,?,?,?,?,?)').bind(id,record_id,f.name,type,f.size,t,role).run();
 return json({id,record_id,name:f.name,type,size:f.size,created_at:t,role});
 }
 const file=p.match(/^\/api\/files\/([^/]+)$/);
 if(file&&req.method==='GET'){
 const f=await db.prepare('SELECT * FROM files WHERE id=?').bind(file[1]).first();if(!f)return json({error:'Arquivo não encontrado'},404);
 const obj=await env.BUCKET.get(f.id);if(!obj)return json({error:'Arquivo não encontrado'},404);
 const allowed=/^(image\/(png|jpeg|gif|webp|avif)|video\/(mp4|webm|quicktime)|audio\/(mpeg|wav|mp4|ogg))$/i.test(f.type);
 return new Response(obj.body,{headers:{'content-type':allowed?f.type:'application/octet-stream','content-disposition':allowed?'inline':'attachment', 'x-content-type-options':'nosniff','cache-control':'private, max-age=3600','content-length':String(f.size)}});
 }
 return json({error:'Operação não encontrada'},404)
 }catch(e){console.error(e);return json({error:'Não foi possível concluir a operação. '+String(e.message||e)},500)}
}};
