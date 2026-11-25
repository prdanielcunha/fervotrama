import fs from 'node:fs';
fs.mkdirSync('dist/server',{recursive:true}); fs.mkdirSync('dist/.openai',{recursive:true});
const html=fs.readFileSync('src/index.html','utf8').replace('/* STYLE */',()=>fs.readFileSync('src/style.css','utf8')).replace('/* CLIENT */',()=>fs.readFileSync('src/client.js','utf8'));
const seed=JSON.parse(fs.readFileSync('src/seed.json','utf8'));
fs.writeFileSync('dist/server/index.js','const HTML='+JSON.stringify(html)+';\nconst SEED='+JSON.stringify(seed)+';\n'+fs.readFileSync('src/server.js','utf8'));
fs.copyFileSync('.openai/hosting.json','dist/.openai/hosting.json');
