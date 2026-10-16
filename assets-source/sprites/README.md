# Pipeline de personagens — Sprint 4

Pillow 9.0.1 fixado em `requirements-assets.txt`. Nenhum Blender necessário.

```sh
python3 scripts/prepare_character_art.py goku
python3 scripts/prepare_character_art.py vegeta
python3 scripts/build_characters.py
python3 tests/validate.py
```

`production.json` documenta folhas RGBA, retângulos de extração explícitos, escala comum, âncoras dos pés e
bindings de imagens para contextos AIR. O extrator compartilhado cria PNGs
320×320 e manifestos; Vegeta usa o mesmo contrato, com folhas ainda pendentes.
`grounded` alinha a borda alpha inferior em y=240 após reamostragem, eliminando
a oscilação de arredondamento. Âncoras horizontais explícitas mantêm a base dos
pés, sem recentrar o personagem pela mão estendida. Não esticar cada pose para
preencher caixas. As folhas geradas são referências preservadas; a geração AI
não é determinística. Extração e reconstrução a partir dessas referências são.

Manifesto por personagem:

```json
{"version":1,"facing":"right","frames":[{"sprite":[30000,0],"file":"idle/000.png","origin":[160,240],"scale":1,"organic":true,"normalized_bounds":[-33,-94,34,0],"sha256":"hash do PNG"}]}
```

Origem em pixels da fonte, escala finita positiva <=8, dimensões da fonte <=2048,
normalização <=1024 antes do canvas. RGBA completo, inclusive alpha parcial,
é preservado sem quantização em SFF 2.0.1 PNG32. O encoder PCX legado continua
rejeitando alpha parcial explicitamente. Nenhuma simulação com alpha binário.
`resample` aceita `nearest` (padrão) ou `lanczos`. O extrator rejeita células que cortem pixels com alpha >=32 antes da redução;
alpha inferior permanece preservado, sem threshold na imagem de saída.
Fontes não podem escapar da
pasta do personagem, inclusive por symlink. Frames vazios, IDs duplicados,
origens fora da fonte, recortes no canvas, fonte orgânica tocando suas bordas,
bounds divergentes e hashes inválidos são rejeitados. `facing` valida metadados;
a orientação semântica do desenho exige revisão visual. A arte deve compensar
os offsets/flips AIR existentes; nos novos contextos selecionados eles são zero.

Sprites herdados usam IDs por contexto no grupo 30000; poses DBZ 7000/7100
podem receber overrides com origem normalizada. Nunca editar SFF à mão.
AIR continua definindo tempos, hitboxes e hurtboxes. O campo opcional
`hurtboxes: [[left,top,right,bottom], ...]` substitui somente Clsn2 do contexto,
com coordenadas ordenadas e limitadas, sem exigir ocupação completa dos pixels.
Hitboxes, tempos e flips permanecem preservados e comparados à referência.

A política orgânica verifica origem/canvas, bounds por frame, alpha exato da
fonte normalizada e interseção com **cada** caixa de colisão. Os placeholders
mantêm a antiga exigência exata de cobertura/união. Interseção não certifica
contato natural nem balanceamento: revisão humana do alcance e de hurtboxes
continua necessária; nenhuma caixa foi ajustada nesta entrega. A extração
comparte uma escala por animação, mantém iluminação do desenho e base dos pés;
proporções entre folhas e qualidade dos contornos ainda precisam de aprovação.

Goku: 4 PNGs por sequência (20 candidatos), bindings para idle (11 elementos),
caminhada frente/trás, soco 200, preparo/execução 7100 e dano 5000/5010.
O disparo usa 3 dos 4 candidatos para preservar os tempos e o spawn do projétil.
Demais poses, carga de Ki e Vegeta continuam geométricos. O arquivo
`reference/motions-generated.png` é uma tentativa rejeitada: a grade gerada
corta poses e não participa do build. Não é entrega artística final.

Licenças, origem e prompts em `docs/ART_PROVENANCE.md`; evidências em TESTING.
