# FervoTrama Studio

Aplicação privada para direção e produção de novelas originais do FervoTrama. Código independente dos arquivos históricos do repositório.

- Backend Cloudflare Worker com D1 (registros e revisões) e R2 (arquivos enviados).
- Acervo inicial importado do GitHub e das fontes do projeto. O código de importação é reprodutível com `python import_sources.py <checkout-original> <pasta-fontes>`.
- `npm test` valida a sintaxe; `npm run build` gera `dist/server/index.js` e o manifesto.
- Novas alterações no Studio são guardadas no banco hospedado; o código-fonte é versionado no GitHub. Exportação JSON disponível no aplicativo.
- Fontes originais não são alteradas. Sem o Meu Nome v2 é uma revisão editorial separada, mantendo a versão anterior na biblioteca. Imagens importadas são prévias, apontando para arquivos originais do commit de referência.
- Publicação privada pelo Sites: https://fervotrama-studio.ocasalcunha.chatgpt.site

## Reproduzir o acervo inicial

Extraia `project-inputs.zip` em `project_sources/`, instale Pillow e execute, a partir de `studio/`: `python import_sources.py .. project_sources && npm run build`. O seed é um artefato gerado e contém as prévias das imagens. Use o commit original 1c0d80c673b54dd559778b7e7a2c676609a89107 para reproduzir a leitura do acervo.
