# Arte da Sprint 4 — proveniência e limites

Data: 16/10/2026. Ferramenta: `image_gen` integrada nesta sessão, skill imagegen.
Não foi usado Blender, download de sprites comerciais, extração de jogos ou
modelo 3D de terceiros. As imagens foram geradas nesta sessão e depois
fatiadas/normalizadas pelo extrator Pillow do projeto. A geração não é
reproduzível bit a bit; os PNGs de referência abaixo são a fonte permanente.

## Inventário e licenças

- `assets-source/sprites/goku/reference/{idle,walk,punch,kamehameha,damage}-generated.png`:
  cinco folhas candidatas, quatro desenhos cada; geração AI de fan art de Goku.
  Nenhuma licença oficial de Dragon Ball ou autorização de seus titulares foi
  fornecida/registrada. Não atribuir licença oficial, CC0 ou procedência manual
  a esses arquivos. Os direitos sobre personagens/marcas não são concedidos
  pelo código MIT do projeto. Distribuição comercial não foi autorizada aqui.
- `reference/motions-generated.png`: tentativa de grade 4×4 rejeitada por
  isolamento/recorte dos frames. Arquivo de auditoria; não utilizado pelo build.
- `idle/`, `walk/`, `punch/`, `kamehameha/`, `damage/`: 20 PNGs normalizados,
  derivados das cinco folhas. O manifesto aponta os utilizados pelo AIR.
- Placeholders/efeitos: código procedural original do projeto, MIT sobre o
  código/desenho; nenhuma concessão de direitos dos personagens.
- Combate/AIR base/áudio KFM: Elecbyte, licença Creative Commons Noncommercial
  incluída em `engine/chars/goku/readme.txt`; avisos preservados.
- Motor IKEMEN GO v1.0.0: MIT, avisos em `engine/LICENSES.txt`.
- Pillow 9.0.1: licença distribuída pelo Pillow; dependência fixada em
  `requirements-assets.txt`. Ver [licença do Pillow](https://github.com/python-pillow/Pillow/blob/9.0.1/LICENSE).

A implementação de PNG32 segue a leitura de cabeçalhos e payloads do
[IKEMEN GO image.go](https://github.com/ikemen-engine/Ikemen-GO/blob/v1.0.0/src/image.go),
formato 12, profundidade 32, payload precedido de tamanho decodificado.
Não foi copiado código Go. O comportamento foi conferido no motor fixado.

## Prompts e processamento

Os prompts completos estão em `assets-source/sprites/goku/reference/prompts.json`.
A primeira folha foi gerada sem referência. As demais usaram o idle original
como referência de identidade/iluminação. Não se utilizou imagem oficial como
referência. O pedido de grade 4×4 falhou e foi substituído por folhas individuais.

`production.json` registra células, escala comum por sequência, âncoras de pés,
normalização do chão e bindings explícitos de PNG → contexto AIR. A escala não
segue as caixas de colisão. A iluminação é parte dos desenhos; não há filtro
procedural simulando acabamento artístico. Para reconstruir:

```sh
python3 scripts/prepare_character_art.py goku
python3 scripts/build_characters.py
```

## Estado artístico

A animação idle usa quatro desenhos orgânicos reconhecíveis em combate real.
Caminhada, soco, Kamehameha e dano foram integrados como candidatos. Não houve
aprovação humana final: há variação de anatomia/cabelo entre folhas, contornos
que precisam de limpeza e contatos/hurtboxes que precisam de inspeção por
frame. Os tempos, hitboxes e hurtboxes permanecem os herdados. A carga de Ki,
demais ataques, saltos, defesa, quedas e vitória ainda usam placeholders.

Vegeta: contrato/manifesto/plano preparado, arte orgânica pendente. Não há
transformações. A Sprint não está integralmente concluída.

## Hashes das referências

| Arquivo | SHA256 |
| --- | --- |
| `damage-generated.png` | `a187eea86c5da210d89be6759a19e824cba022b09a18caca33c612cb9492735c` |
| `idle-generated.png` | `6f81b5b7032c5a765f3323b28f1365021534ee9e2a82ae4cdf65720d1eb252a3` |
| `kamehameha-generated.png` | `4d759817b99c12c084b5666fce3163a6dd0fdfa7ebd7230b4dd5572dcdda6618` |
| `motions-generated.png` | `c82a26e3c49cca03eaf079ddef8ba327554a7d77a3be356dbadde1539fe4e53c` |
| `punch-generated.png` | `994a2fe3be5c980d42ae09a157a0dc9ecb28755dd41abb30f7c7c5c520f95fbf` |
| `walk-generated.png` | `0c8a5be1004bff487ef165ed7ee9e0810f62f19ddddcf64390bac48bf10811ce` |

# Sprint 5 — novas fontes candidatas

Ferramenta: `image_gen` integrada, skill imagegen, sem CLI/API externa, Blender,
modelos 3D, sprites comerciais, extração de jogos ou referências oficiais.
As referências de identidade são as folhas geradas neste próprio projeto.
As ressalvas de direitos de personagens, KFM e motor acima continuam válidas.
Nenhuma licença oficial de Dragon Ball foi obtida ou alegada.

Novas folhas em `assets-source/sprites/{goku,vegeta}/reference/`:
`core-generated.png` (chute/salto/carga), `defense-fall-generated.png`,
`extra-generated.png` (chute baixo/soco agachado/vitória),
`air-sweep-generated.png` e `power-generated.png` (soco forte/uppercut).
Vegeta acrescenta `locomotion-generated.png`, `locomotion-transparent.png`,
`combat-generated.png` e `damage-generated.png`. A primeira locomotion foi
preservada para rastrear a iteração de remoção do fundo; só a segunda é consumida.
A folha combat fornece soco/Galick Gun; seu dano foi substituído pela folha
individual para manter melhor a altura em pé. As imagens não são arte final.

Especificação dos prompts: fan art de cada personagem em estilo anime orgânico,
contorno limpo/sombreado, câmera ortográfica 3/4 voltada à direita, corpo inteiro,
mesmas proporções/roupas em cada desenho, alpha transparente, sem texto, grade,
efeitos ou sombras. Cada linha pede quatro fases consecutivas da ação indicada
no nome/plano: antecipação, preparo, execução e recuperação; idle/carga pedem
respiração; caminhada pede alternância dos pés; queda pede inclinação, voo,
corpo deitado e apoio de cotovelo; vitória Goku pede erguer o punho e Vegeta
cruzar os braços. Alguns resultados não seguiram perfeitamente esses requisitos;
os problemas estão em SPRINT_5_VISUAL_REVIEW.md. As folhas preservadas, e não a
reexecução não determinística dos prompts, são as fontes reproduzíveis do build.

`production.json` fixa sementes de componentes, retângulos, âncoras, escala,
bindings, posicionamento aéreo, compensação AIR e dois overrides de hurtbox.
O extrator preserva alpha parcial da região extraída; não pinta nem interpola
novas poses. Hashes das folhas usadas em `sprint5-animation-audit.json`.

# Sprint 6 — cadência e inspeção

Nenhuma fonte artística nova foi gerada ou importada. Referências, desenhos e
licenças das Sprints 4/5 permanecem os mesmos. O plano
`assets-source/animation-polish.json` altera somente retenções do idle; não
produz desenhos. PNG/GIF em `evidence/sprint6/assets/` são renderizações de
inspeção das fontes existentes com coordenadas/caixas AIR. Vídeos em
`evidence/sprint6/runtime/` são capturas reais da janela do motor e não são
conteúdo do jogo. Nenhum desses artefatos implica aprovação artística humana.

# Sprint 7 — caminhadas candidatas novas

Ferramenta: `image_gen` integrada, skill imagegen; sem CLI/API externa ou
sprites extraídos de jogos. Seis folhas de fan art geradas nesta sessão,
três iterações por personagem, em `assets-source/sprites/{goku,vegeta}/reference/sprint7/`.
A v1 foi gerada a partir da descrição; v2/v3 editaram a folha anterior do
próprio projeto. As fontes iniciais/comerciais de terceiros não foram usadas.
As ressalvas sobre direitos dos personagens, KFM e motor continuam válidas;
não é alegada licença oficial ou CC0 sobre personagens/marcas.

Somente `walk-v3-generated.png` de cada personagem é consumida pela nova
família `walk_sprint7`: quatro desenhos por personagem, oito no total.
As v1/v2 são tentativas rejeitadas, mantidas para auditoria. Briefs e prompts
finais em `assets-source/sprites/sprint7-prompts.md`; rastreio por personagem
em `reference/sprint7/generation.json`; hashes das fontes usadas no relatório
`evidence/sprint7/animation-audit.json`.

O processamento usa o extrator existente: componentes alpha, retângulos,
escala comum e âncoras explícitas; não sintetiza nem desloca uma pose única
para simular passos. Os 32 contextos de caminhada 20/21 por personagem são
substituídos. Os outros 605 bindings mantêm desenhos e pixels anteriores.
AIR, caixas, tempos, CNS, CMD e Ki não foram alterados. As novas poses são
candidatas: continuidade, troca anatômica de apoio e deslizamento ainda
impedem aceite artístico. Não foram produzidos novos desenhos de combate.
