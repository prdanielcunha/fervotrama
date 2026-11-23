# Fervotrama — LEIA PRIMEIRO: método para imagens e vídeos consistentes

Este arquivo vale para os 8 episódios (arquivos **Fervotrama E01 a E08**). Cada episódio tem os clipes na ordem, com **prompt de imagem** e **prompt de vídeo** prontos para copiar.

**Aviso honesto:** com ferramentas gratuitas não dá para garantir 100% de perfeição, e o rosto e a voz podem variar de um clipe para o outro. O método abaixo reduz bastante esse risco. Conte com refazer alguns clipes (2 ou 3 tentativas por clipe é normal).

Formato dos códigos, como no Cenarra: **E01 C01** = episódio 1, clipe 1. Vertical 9:16, 1080x1920, clipes de 10 segundos, prompts com menos de 900 caracteres.

---

## 1. Antes de produzir qualquer episódio (faça uma vez)

### 1.1 Imagens de referência dos personagens
Gere e aprove **uma imagem de cada personagem**, usando o prompt de imagem do arquivo **01 Fervotrama Personagens**. Salve com estes nomes:

| Arquivo | Personagem |
|---|---|
| REF_Vo_Noemia.png | Vó Noêmia (já gerada no teste) |
| REF_Lara.png | Lara |
| REF_Marcos.png | Marcos |
| REF_Rute.png | Rute |
| REF_Seu_Aderbal.png | Seu Aderbal |
| REF_Davi.png | Davi |
| REF_Ricardo.png | Ricardo |

Critério de aprovação: rosto marcante e simpático, mãos normais, roupa igual à ficha, fundo simples e iluminação suave.

### 1.2 Imagens de referência dos cenários
O cenário também muda de um clipe para outro se você não o fixar. Gere cada cenário **vazio, sem pessoas**, aprove e salve. Os prompts estão na seção 4.

| Arquivo | Cenário |
|---|---|
| CEN_cozinha.png | Cozinha de dia/fim de tarde |
| CEN_cozinha_noite.png | Cozinha de madrugada (ep. 4) |
| CEN_sala_jantar.png | Sala de jantar (ep. 3) |
| CEN_quarto_Vo.png | Quarto da Vó (ep. 4 e 5) |
| CEN_garagem.png | Garagem (ep. 3 e 7) |
| CEN_carro.png | Interior do carro (ep. 2) |
| CEN_porta_rua.png | Porta da casa e rua |

### 1.3 Pasta de trabalho
Crie uma pasta por episódio (E01, E02...) e salve cada clipe e cada último frame com o nome exato que o arquivo do episódio indica, por exemplo `E01_C03.mp4`. Assim você nunca se perde na sequência.

---

## 2. Como produzir cada clipe (ordem fixa)

1. **Siga os clipes na ordem** C01, C02, C03... Os clipes de continuação dependem do anterior.
2. Veja o campo **"Anexar como referência"** do clipe e envie essas imagens junto.
3. Veja o campo **"Imagem inicial"**:
   - **"gere nova":** cole o **prompt de imagem** e gere 2 a 3 versões. Escolha a melhor.
   - **"use o ÚLTIMO FRAME":** use o último frame do clipe anterior como imagem inicial (seção 3). O prompt de imagem fica como reserva.
4. Com a imagem aprovada, cole o **prompt de vídeo** e gere 2 a 3 versões do clipe.
5. Escolha a melhor versão e salve como `E0X_C0Y.mp4`.
6. Salve o **último frame** como `E0X_C0Y_ultimo_frame.png` (seção 3).
7. Marque o "Conferir antes de seguir" do clipe e só então vá para o próximo.

**Dica de ritmo:** faça primeiro todas as imagens do episódio e aprove todas. Só depois gere os vídeos. Assim os problemas de rosto e de roupa aparecem antes de você gastar tentativas de vídeo.

---

## 3. Como pegar o último frame de um clipe

**No celular:** reproduza o clipe, pause no fim, tire um print e recorte para 9:16 sem bordas.

**No computador (mais preciso):**
```
ffmpeg -sseof -0.1 -i E01_C07.mp4 -frames:v 1 E01_C07_ultimo_frame.png
```

Se o último frame estiver borrado (movimento rápido), pegue um frame um pouco antes, por exemplo `-sseof -0.4`.

Para clipes de continuação, use essa imagem como imagem inicial (a mesma opção de "imagem para vídeo" que você usou no teste da Vó).

---

## 4. Prompts dos cenários (vazios, sem pessoas)

**CEN_cozinha**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, interior de uma cozinha brasileira simples e aconchegante, sem pessoas. Mesa de madeira com toalha de renda branca, xícaras de porcelana com rosas, janela com cortina de renda deixando entrar luz dourada de fim de tarde, prateleira com vasos de planta e utensílios de cobre, azulejos brancos antigos, fogão antigo. Luz quente e suave, textura realista. Sem texto, sem logo.
```

**CEN_cozinha_noite**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, a mesma cozinha brasileira simples e aconchegante, sem pessoas, de madrugada. Escura, iluminada apenas por um abajur amarelo sobre a mesa de madeira com toalha de renda, xícaras de porcelana com rosas, janela escura com cortina de renda, foto de família na porta da geladeira. Luz amarela suave, sombras profundas, textura realista. Sem texto, sem logo.
```

**CEN_sala_jantar**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, sala de jantar de uma casa de família brasileira simples, sem pessoas. Mesa de madeira com cinco cadeiras, toalha, pratos e uma panela fumegando, lâmpada pendente com luz amarela quente, quadro de família na parede, aparador antigo ao fundo. Clima doméstico e tenso, luz quente e suave, textura realista. Sem texto, sem logo.
```

**CEN_quarto_Vo**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, quarto simples de uma senhora idosa brasileira, sem pessoas. Cama com colcha de crochê, criado-mudo com abajur e um caderno velho de capa azul, cômoda com porta-retratos, caixa de costura antiga no chão, janela com cortina de renda e luz suave de manhã. Luz quente e suave, textura realista. Sem texto, sem logo.
```

**CEN_garagem**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, garagem simples de uma casa brasileira, sem pessoas. Bancada de madeira com ferramentas, um banquinho de madeira, lâmpada amarela pendurada, prateleiras com caixas, parte da frente de um carro popular. Luz amarela suave, sombras leves, textura realista. Sem texto, sem logo.
```

**CEN_carro**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, interior de um carro popular brasileiro limpo, visto do banco de trás, sem pessoas. Banco do motorista, volante, retrovisor com um crachá de aplicativo pendurado, rua de bairro vista pelo vidro com luz dourada de fim de tarde. Luz quente e suave, textura realista. Sem texto, sem logo.
```

**CEN_porta_rua**
```
Vertical 9:16 (1080x1920), realismo cinematográfico, fachada de uma casa de bairro brasileira simples, sem pessoas. Portão baixo de ferro, porta de madeira, caixa de correio ao lado, vasos de planta, rua de bairro tranquila com luz dourada de fim de tarde. Luz quente e suave, textura realista. Sem texto, sem logo.
```

---

## 5. Regras de ouro para manter tudo igual

1. **Nunca edite o bloco fixo** do personagem. Os prompts já vêm com ele colado.
2. **Sempre anexe as referências** do clipe (personagem e cenário).
3. **Mesma roupa em todo o episódio.** Os prompts já cuidam disso. Exceção planejada: no ep. 4 (madrugada), Rute está de uniforme azul-claro de enfermagem e Lara de pijama azul-claro de manga e calça compridas, e voltam à roupa normal no clipe C08.
4. **Se o rosto mudou, regere o clipe.** Não tente "corrigir" na edição, porque o público percebe.
5. **No máximo 2 ou 3 personagens por clipe.** Nas cenas com mais gente (ep. 8), os prompts usam blocos resumidos. Se o rosto de alguém sair diferente, gere a cena em dois planos e alterne na edição.
6. **Evite movimento rápido de câmera ou de cabeça.** Isso derruba a consistência. Os prompts usam aproximações lentas de propósito.
7. **Regere só o clipe que falhou**, sem refazer o episódio inteiro, mas mantenha os mesmos pontos de partida (referências e último frame).

---

## 6. Voz

As vozes também podem variar entre clipes. Os prompts de vídeo já trazem uma **descrição fixa de voz** para cada personagem:

| Personagem | Descrição de voz usada |
|---|---|
| Vó Noêmia | voz de mulher idosa, suave e grave |
| Lara | voz de adolescente, clara e divertida |
| Marcos | voz de homem de 45 anos, grave e contida |
| Rute | voz de mulher de 40 anos, baixa e suave |
| Seu Aderbal | voz de homem idoso, rouca e lenta |
| Davi | voz de homem jovem, hesitante |
| Ricardo | voz de homem de 38 anos, educada e cansada |

Se a voz de um personagem mudar de um clipe para outro, você tem duas saídas:
- Regerar o clipe até a voz ficar parecida.
- Gerar o clipe sem fala (apague a linha da voz do prompt) e gravar a narração na edição com uma única voz por personagem. É mais trabalhoso, mas dá a voz 100% igual.

---

## 7. Checklist por episódio

- [ ] Referências de personagens e cenários prontas
- [ ] Imagens de todos os clipes geradas e aprovadas
- [ ] Vídeos gerados na ordem, com os últimos frames salvos
- [ ] Rosto, roupa, cenário e voz conferidos em cada clipe
- [ ] Montagem na ordem do mapa, com música baixa
- [ ] Legenda e referência bíblica na tela
- [ ] Rótulo de conteúdo feito com IA ativado

---

## 8. O que aprendemos com o teste do E01 C01 (e o que mudou nos prompts)

Analisei a imagem e o vídeo que você gerou do E01 C01. O que funcionou: o rosto, o óculos, o cardigã, o caderno, a xícara e a luz ficaram fiéis. O que precisou de ajuste, e já foi aplicado em **todos os 65 clipes**:

| Problema visto | Correção nos prompts |
|---|---|
| O enquadramento mudou no meio do clipe e o rosto chegou a ficar cortado no topo | "Câmera parada, enquadramento fixo, sem cortes nem troca de plano, rosto inteiro no quadro". Zooms e aproximações saíram dos prompts. Se quiser movimento, faça um zoom leve na edição. |
| A emoção passou de "marejada" para choro forte, com careta | "Emoção contida: olhos marejados, lágrimas discretas, sem soluçar alto e sem careta de choro". |
| A boca se mexeu por quase todo o clipe | Cada prompt diz que os lábios só se movem durante a fala, dita uma vez, devagar, em uma janela de segundos calculada pelo tamanho da frase. |
| Rugas mais fortes e rosto mais velho que a referência anterior | Bloco fixo da Vó atualizado: "aparência de 70 anos, rugas leves e discretas, sem rugas profundas", com aliança e botões marrons. |
| O texto do caderno ficou legível e depois mudou de forma | No E01 C01 e C04 o texto é fixo ("1998" e "Senhor, não deixa esse homem sozinho."). Nos demais clipes, a escrita é desfocada e sem palavras legíveis. |
| "Corte seco" nos prompts conflita com "uma única tomada" | O corte para o preto agora é feito na edição, e o clipe avisa quando for o caso. |

**Importante:** escolha **uma** imagem como referência oficial da Vó e não troque mais. Se você prefere o rosto mais marcado da imagem do teste, adote ela como referência e remova "rugas leves e discretas (sem rugas profundas)" do bloco, para o texto não brigar com a imagem.

**Sobre a voz:** os prompts descrevem a voz de cada personagem, mas não consegui transcrever o áudio do seu vídeo, então confira de ouvido se a frase saiu certa e uma só vez.
