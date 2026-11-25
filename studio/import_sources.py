import re,json,pathlib,zipfile,hashlib,urllib.parse,base64,io,sys
from PIL import Image
from xml.etree import ElementTree as ET
repo=pathlib.Path(sys.argv[1]); project=pathlib.Path(sys.argv[2]); out=[]
def add(id,kind,parent=None,**data):
 out.append(dict(id=id,kind=kind,parent=parent,data=data));return id
def read(p):return p.read_text(encoding='utf-8-sig')
def blocks(txt):return re.findall(r'```(?:\w+)?\s*\n(.*?)\n```',txt,re.S)
def split(txt,pattern):
 matches=list(re.finditer(pattern,txt,re.M));return [(m,txt[m.end():matches[i+1].start() if i+1<len(matches) else len(txt)].strip()) for i,m in enumerate(matches)]
def blob(path):return 'https://github.com/prdanielcunha/fervotrama/blob/1c0d80c673b54dd559778b7e7a2c676609a89107/'+urllib.parse.quote(str(path),safe='/')
def source(name,txt,origin,link='',parent=None):
 id='src-'+hashlib.sha256((origin+name).encode()).hexdigest()[:16];add(id,'source',parent,title=name,document=txt,origin=origin,url=link);return id
def docx_text(raw):
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  x=ET.fromstring(z.read('word/document.xml'))
  return '\n'.join(''.join(t.text or '' for t in el.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')) for el in x.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))
# Preserve complete textual sources, including prior variants.
for p in sorted(repo.rglob('*')):
 if '.git' in p.parts or 'studio' in p.relative_to(repo).parts or not p.is_file():continue
 rel=p.relative_to(repo)
 if p.suffix=='.md':source(str(rel),read(p),'GitHub oficial',blob(rel))
 if p.suffix=='.docx':source(str(rel),docx_text(p.read_bytes()),'GitHub oficial · texto do DOCX',blob(rel))
 if p.suffix=='.zip':
  source(str(rel),'Arquivo ZIP original preservado no repositório. Conteúdo textual indexado abaixo.','GitHub oficial',blob(rel))
  with zipfile.ZipFile(p) as z:
   for n in z.namelist():
    if n.endswith('.md'):source(n,z.read(n).decode('utf-8-sig'),'GitHub · '+str(rel),blob(rel))
for p in sorted(project.glob('*')):
 if p.suffix=='.md':source(p.name,read(p),'Fontes do projeto')
 if p.suffix=='.docx':source(p.name,docx_text(p.read_bytes()),'Fontes do projeto · texto DOCX')
 if p.suffix=='.zip':
  with zipfile.ZipFile(p) as z:
   for n in z.namelist():
    if n.endswith('.md'):source(n,z.read(n).decode('utf-8-sig'),'Fontes do projeto · '+p.name)
def series(id,title,editorial='',status='Roteiro',**data):
 return add(id,'series',title=title,status=status,editorial=editorial,publication_days='Terça, sexta',**data)
def season(id,s,title='Temporada 1',**data):return add(id,'season',s,title=title,status='Roteiro',**data)
def episode(id,s,num,title,txt,**data):return add(id,'episode',s,title=title,number=num,status=data.pop('status','Roteiro'),format='9:16',script=txt,**data)
def scene(id,e,num,title,**data):return add(id,'scene',e,title=title,number=num,status='Prompt pronto',duration=10,**data)
# Vó Noêmia
v=repo/'fontes/Fervotrama_Temporada_1_Todos_os_Episodios.md';raw=read(v)
overview=raw.split('# EPISÓDIO 1')[0]
series('vo','O Caderno da Vó Noêmia','Série casa — manter; reeditar abertura do E01 conforme Molde Isca e Parábola.',story=overview,origin=str(v.relative_to(repo)))
season('vo-t1','vo',story=overview)
for m,t in split(raw,r'^# EPISÓDIO (\d+)\s+—\s+"?([^"\n]+)"?\s*$'):
 n=int(m[1]);e=f'vo-t1-e{n:02d}';episode(e,'vo-t1',n,m[2],t,planned_duration=80,origin=str(v.relative_to(repo)))
 for cm,ct in split(t,r'^### Clipe (\d+) — (.+)$'):
  k=int(cm[1]);b=blocks(ct);img=re.search(r'\*\*Imagem-base:\*\*\s*(.+)',ct)
  scene(f'{e}-c{k:02d}',e,k,cm[2],visual=img[1] if img else '',image_prompt=img[1] if img else '',video_prompt=b[0] if b else '',script=ct,origin=str(v.relative_to(repo)))
# Official actor sheets
charraw=read(repo/'fontes/01_Fervotrama_Personagens.md')
for m,t in split(charraw,r'^## [1-9]\. (.+)$'):
 title=re.split(r' \(| — ',m[1])[0]
 if title.startswith('Elenco bíblico'): 
  for bm,bt in split(t,r'^### (.+)$'):
   b=blocks(bt);add('char-bib-'+str(len(out)),'character',None,title=bm[1],description=bt,fixed_prompt=b[0] if b else '',origin='Ficha bíblica · fontes/01_Fervotrama_Personagens.md')
  continue
 b=blocks(t);cid='vo-char-'+str(len(out));age=re.search(r'(\d+) anos',m[1]+' '+t)
 add(cid,'character','vo' if title!='Jesus' else None,title=title,age=age[1] if age else '',description=t,fixed_prompt=b[0] if b else '',image_prompt=b[1] if len(b)>1 else '',origin='fontes/01_Fervotrama_Personagens.md')
 if title=='Vó Noêmia':vochar=cid
 if title=='Lara':larachar=cid
guid=read(repo/'fontes/00_Fervotrama_LEIA_PRIMEIRO_Consistencia-1-.md')
for m,t in split(guid,r'^\*\*(CEN_[^*]+)\*\*\s*$'):
 b=blocks(t);add('vo-setting-'+m[1],'setting','vo',title=m[1],description=b[0] if b else t,image_prompt=b[0] if b else '',origin='Guia de consistência')
add('vo-obj-1','object','vo',title='Caderno velho de capa azul',description='Caderno velho de capa azul.',origin='Ficha de Vó Noêmia')
# complete five public source seasons
maps=[('domingo','Foto_de_Domingo','Encurtar para quatro episódios conforme decisão editorial; texto completo preservado.'),('nome','Sem_o_Meu_Nome','Reescrita v2 (arquivo mais recente) é a versão de trabalho.'),('plateia','A_Plateia','Arquivar conforme Molde Isca e Parábola.'),('linha','Na_Linha','Ideia reaproveitada em Faltou Um; acervo anterior preservado.'),('ausentes','Foto_dos_Ausentes','Expandir conforme decisão editorial; dois episódios completos existentes.')]
for sid,fname,ed in maps:
 p=repo/'temporadas'/f'{fname}_Temporada_Completa.md';t=read(p);title=t.splitlines()[0][2:];pre=t.split('# Episódio')[0].strip()
 series(sid,title,ed,story=pre,origin=str(p.relative_to(repo)))
 tid=sid+'-t1';season(tid,sid,'Temporada 1 · versão anterior' if sid=='nome' else 'Temporada 1',story=pre,edition='Histórico' if sid=='nome' else 'Original',origin=str(p.relative_to(repo)))
 for m,et in split(t,r'^# Episódio (\d+) — (.+)$'):
  n=int(m[1]);e=f'{tid}-e{n:02d}';planned=80 if sid=='ausentes' else 100;episode(e,tid,n,m[2],et,planned_duration=planned,origin=str(p.relative_to(repo)))
  for cm,ct in split(et,r'^## E\d+ C(\d+) · ([^\n]+)$'):
   k=int(cm[1]);b=blocks(ct);scene(f'{e}-c{k:02d}',e,k,cm[2].split(' · ')[-1] if ' · ' in cm[2] else 'Clipe '+str(k).zfill(2),image_prompt=b[0] if b else '',video_prompt=b[1] if len(b)>1 else '',script=ct,origin=str(p.relative_to(repo)))
 # Preserve exact reference section in library
 ref=pre.split('## Referências para gerar uma vez')[-1].split('## Duração')[0].strip()
 add(sid+'-ref','setting',sid,title='Referências de produção',description=ref,origin=str(p.relative_to(repo)))
# v2 from supplied ZIP (separate revision of temporada 1)
z=zipfile.ZipFile(next(project.glob('*FervoTrama_v2.zip')))
def zread(n):return z.read('FervoTrama_v2/'+n).decode()
guide=zread('00_LEIA_PRIMEIRO.md')
for sid,folder in [('nome','05_Sem_o_Meu_Nome_v2'),('faltou','06_Faltou_Um')]:
 h=zread(folder+'/01_Historia.md');im=zread(folder+'/02_Prompts_de_Imagem.md');vi=zread(folder+'/03_Prompts_de_Video.md');ed=zread(folder+'/04_Edicao_e_Postagem.md')
 title=h.splitlines()[0][2:];summary=h.split('## E01')[0].strip()
 if sid=='faltou':series(sid,title,'Novela nova — parábola da ovelha perdida.',story=summary,origin=folder)
 else:
  next(r for r in out if r['id']=='nome')['data'].update(story=summary)
 tid=sid+'-v2';season(tid,sid,'Temporada 1 · v2',story=summary,edition='Versão atual',origin=folder)
 ei={int(m[1]):t for m,t in split(im,r'^## E(\d+) · .+$')};ev={int(m[1]):t for m,t in split(vi,r'^## E(\d+) · .+$')};ee={int(m[1]):t for m,t in split(ed,r'^### E(\d+) · .+$')}
 for m,t in split(h,r'^## E(\d+) · (.+)$'):
  n=int(m[1]);e=f'{tid}-e{n:02d}';hook=re.search(r'\*\*Gancho .*?\*\*\s*(.+)',t)
  episode(e,tid,n,m[2],t,planned_duration=100,hook=hook[1] if hook else '',publishing_notes=ee.get(n,''),origin=folder+'/01_Historia.md')
  i_s={int(k[1]):s for k,s in split(ei.get(n,''),r'^### E\d+ C(\d+) · .+$')};v_s={int(k[1]):s for k,s in split(ev.get(n,''),r'^### E\d+ C(\d+) · .+$')}
  for cm,ct in split(t,r'^### E\d+ C(\d+) · (.+)$'):
   k=int(cm[1]);ib=blocks(i_s.get(k,''));vb=blocks(v_s.get(k,''));scene(f'{e}-c{k:02d}',e,k,'Clipe '+str(k).zfill(2),script=ct,image_prompt=ib[0] if ib else '',video_prompt=vb[0] if vb else '',backup_prompt=vb[1] if len(vb)>1 else '',origin=folder,visual=cm[2])
 if sid=='faltou':
  for n in (4,5):
   pat=r'\*\*E0'+str(n)+r' · (.*?)\.\*\*\s*(.+)'
   m=re.search(pat,guide)
   if m:episode(f'{tid}-e{n:02d}',tid,n,m[1],m[2],status='Ideia',origin='00_LEIA_PRIMEIRO.md · esboço')
# exact named references from guide and prior seasons
for m in re.finditer(r'^- \*\*(Lígia|Nair|Raul|Rita|Aurélio|Dona Vera|Caio):\*\* (.+)$',guide,re.M):
 title=m[1];sid='nome' if title in ['Lígia','Nair','Raul','Rita'] else 'faltou';age=re.search(r'(\d+) anos',m[2]);add('ref-'+str(len(out)),'character',sid,title=title,description=m[2],age=age[1] if age else '',origin='FervoTrama_v2/00_LEIA_PRIMEIRO.md')
chars={'domingo':[('Helena','30, cachos escuros e camisa verde'),('Celina','60, trança prata e vestido azul'),('Artur','62, bigode e avental marrom'),('Márcio','24 no passado, jaqueta jeans com cotovelo remendado')],'plateia':[('Marina','29, cachos pretos, camisa jeans'),('Vera','54, mecha branca, blusa mostarda'),('Cida','52, tranças, casaco vinho'),('Filha adulta de Cida','30, tranças curtas, blusa creme; voz infantil somente na gravação antiga')],'linha':[('Lia','41, corte chanel, casaco ferrugem'),('Rui','antigo zelador, 68, cego, camisa cinza e bengala'),('Dina','50, corta-vento amarelo')],'ausentes':[('Elisa','22 anos, cachos castanhos e casaco vinho'),('Irene','52 anos, mãe de Elisa, camisa bege e cabelo preso'),('Joana','36 anos, fotógrafa de jardineira jeans')],'nome':[('Orlando','Só existe em foto, letra e voz de gravador. Não gere o rosto dele em vídeo.')]}
for sid,cs in chars.items():
 for title,desc in cs:add('char-'+str(len(out)),'character',sid,title=title,description=desc,origin='Referências oficiais · roteiro/guia')
sets={'nome':[('Padaria','Padaria com caixa junto à porta, oficina de costura da avó nos fundos.'),('Oficina de costura','Oficina de costura da avó nos fundos da padaria.')],'domingo':[('Padaria','Padaria com espelho atrás do balcão e degrau vermelho nos fundos.')],'ausentes':[('Escola noturna','Corredor e portão azuis, sala com carteiras verdes.'),('Balcão de Joana','Balcão de madeira de Joana.')],'plateia':[('Cabine de rádio','Console cinza, deck à esquerda, vidro ao fundo.')],'linha':[('Central de bairro','Balcão azul e campainha de latão rachada.')]}
for sid,ss in sets.items():
 for title,desc in ss:add('setting-'+str(len(out)),'setting',sid,title=title,description=desc,origin='Referências para gerar uma vez')
for sid,title,desc in [('nome','Recorte de jornal','Usar um único recorte de jornal antigo dobrado numa moldura.'),('nome','Máquina de Nair','A avó de Raul consertava aventais com a máquina comprada de Nair.'),('ausentes','Duas fotografias da turma','Na primeira, a carteira está vazia. Na segunda, o pequeno retrato impresso de Elisa está apoiado sobre a carteira. Só a mão e parte de um antebraço de manga cinza entram pela borda direita da foto.'),('domingo','Duas fotografias','Fixar as duas fotografias antes de animar.'),('linha','Campainha','Campainha de latão rachada.')]:
 add('obj-'+str(len(out)),'object',sid,title=title,description=desc,origin='Referências para gerar uma vez')
m=re.search(r'\*\*A Mesa Que Ficou Posta\*\* (.+)',guide)
if m:series('mesa','A Mesa Que Ficou Posta','Fila de desenvolvimento',status='Ideia',story=m[1],origin='FervoTrama_v2/00_LEIA_PRIMEIRO.md')
# image catalogue: indexed previews only, full originals untouched at pinned GitHub commit
def preview(p):
 im=Image.open(p);im.thumbnail((340,550));buf=io.BytesIO();im.convert('RGB').save(buf,'JPEG',quality=78,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
for p in sorted(list((repo/'imagens').rglob('*'))+list((repo/'originais').rglob('*'))):
 if not p.is_file():continue
 rel=p.relative_to(repo);parent='vo';role='Referência do acervo (aprovação não informada)'
 if p.name=='40C984D5-AA29-4572-B20B-A1F563D7E5D9.jpeg':parent=vochar;role='Retrato oficial · biblioteca visual'
 elif p.name=='IMG_8804.jpeg':parent=larachar;role='Retrato oficial · biblioteca visual'
 elif re.match(r'E01_C(\d+)',p.name):
  parent='vo-t1-e01-c'+re.match(r'E01_C(\d+)',p.name)[1];role='Quadro inicial / alternativa do acervo'
 add('media-'+hashlib.sha256(str(rel).encode()).hexdigest()[:16],'source',parent,title=p.name,origin='GitHub oficial · prévia reduzida',url=blob(rel),preview=preview(p),role=role)
# working tools and reusable guides (user-defined)
for name,limit,notes in [('YouTube Create',900,'Prompt em inglês quando exigido; falas em português brasileiro.'),('Grok',5000,'Alternativa de geração de vídeo.'),('Flow','','Registrar resultados e créditos reais.'),('Gemini','','Registrar resultados e créditos reais.'),('CapCut','','Somente montagem, cortes, áudio e exportação.')]:
 add('tool-'+name.lower().replace(' ','-'),'tool',title=name,limit=limit,notes=notes)
add('template-continuidade','template',title='Continuidade fixa',prompt='Preservar rostos, figurino, objetos e iluminação. Apenas quem fala em quadro movimenta a boca. Falas em português brasileiro. Sem extras nem objetos inesperados.',origin='Regras de produção solicitadas')
add('template-isca','template',title='Molde Isca e Parábola',prompt=read(next(project.glob('*Molde_Isca*'))),origin='Fontes do projeto')
json.dump(out,open('src/seed.json','w'),ensure_ascii=False,separators=(',',':'))
from collections import Counter
print(Counter(x['kind'] for x in out),len(out));print([(x['id'],x['data']['title']) for x in out if x['kind']=='series'])
