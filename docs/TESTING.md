# Testes — 16/10/2026

## Evidências da Sprint 1

Nenhum teste manual foi concluído nesta sprint. As execuções abaixo são
estáticas ou automatizadas em X11. O critério de combate estável em uma sessão
humana permanece pendente.

| Verificação | Resultado verificável |
| --- | --- |
| `python3 tests/validate.py` | PASS: 846 sprites, 655 frames AIR, 604 frames com hurtboxes alinhados, por personagem. |
| `python3 -O tests/validate.py` | PASS; validações permanecem ativas com otimização Python. |
| `python3 -m unittest discover -s tests -p 'test_*.py' -v` | 6 testes: defaults/overrides AIR, declaração incompleta, flips/offsets com coordenadas conhecidas, resultados incompletos/inconsistentes, PCX truncado, cadeia SFF corrompida e origem deslocada. |
| `python3 tests/match_smoke.py` | PASS em 30,65 s: dois rounds, placar 0–2, dois KOs, código 0. `tests/rounds-nosound.log`. |
| `python3 tests/match_smoke.py --audio` | PASS em 32,17 s: mesmo cenário, dois KOs, placar 0–2, código 0. `tests/rounds-audio.log`. |
| `python3 tests/keyboard_smoke.py` | PASS: AILevel 0 nos dois lados, vida inicial 900/1000 e final 711/811; código 0. `tests/keyboard-match.log` e `tests/gameplay.png`. |

Motor preservado: IKEMEN GO v1.0.0; SHA256 do executável é
`4a7dbe22218ca2c6785a745c756cdf391edd6f3a3b956f66e101030957c8df29`,
idêntico ao executável em `main` no início da sprint. `docs/engine-lock.json`
fixa esse hash, além do hash histórico do ZIP oficial. Nenhum recurso KFM de
origem, áudio, controle personalizado ou estado de combate foi modificado.

## O que os testes de geometria garantem

O gerador mantém os 242 sprites originais de referência e acrescenta 604
variantes do grupo 30000, uma por contexto de frame com hurtbox. O mesmo sprite
KFM era reutilizado com caixas distintas: escolher pose apenas pelo grupo
produzia desalinhamento em agachamentos, saltos, golpes e quedas.

A arte provisória agora usa uma silhueta preenchida da união das hurtboxes,
com cores da arte original gerada e extensão visível nas hitboxes ativas.
Isso deixa a arte mais geométrica; não representa acabamento artístico.
Offsets e flips AIR são compensados na imagem; o canvas maior evita recortes
nas recuperações e nos frames invertidos. Retratos e frames sem hurtboxes
continuam com a geração anterior. Não há frames com hitboxes e sem hurtboxes
no AIR herdado atual.

A validação decodifica PCX/RLE, confere cadeia/tamanhos/contagens do SFF e compara
ações, duração, offsets, flips e caixas com o AIR KFM de origem. Exige cobertura
de **todos** os pixels das caixas e nenhuma área opaca fora da união. Isso
verifica correspondência geométrica em coordenadas locais; não prova o
comportamento visual de todos os estados no motor, suas escalas, o facing dos
dois jogadores nem os estados de agarrão. Essas verificações são manuais.
As fixtures de offsets/flips têm limites esperados explícitos; testes negativos
rejeitam evidências inválidas. O parser compartilhado gerador/validador continua
sendo uma limitação, mitigada pelas fixtures e pela comparação com a origem.

## Timeout e sequência de rounds

O script `engine/external/script/main.lua`, em `main.f_commandLine`, aplica
`-rounds` a `setMatchWins`: **`-rounds 2` exige duas vitórias**, podendo haver
três rounds decisivos e rounds adicionais por empate. O timeout histórico de
55 segundos com áudio não isolava áudio, foco ou duração total da partida.
Ele continua sem causa conclusiva; esta sprint não altera o backend de áudio.
No Lua distribuído, `-nosound` define `Sound.MasterVolume = 0`; não demonstra
que o dispositivo/backend deixou de ser inicializado. A comparação isola o
volume habilitado versus silenciado, não todo o subsistema. O volume configurado
na execução com áudio era 100 (WAV 80, BGM 75).

O cenário controlado usa P1 sem IA com vida/vida máxima 1, P2 IA 8 com vida
1000, tempo 10 e duas vitórias. A vida máxima baixa permite KO após restauração
entre rounds. Uma tentativa apenas com vida inicial assimétrica e tempo 1
terminou com empate no round seguinte; o validador rejeitou o resultado.
Portanto, saída 0 e número de rounds isoladamente não significam aprovação.

Os testes com/sem áudio concluíram em aproximadamente 31/32 segundos. Os logs
registram índices 1 e 2, P1 com vida 0 e P2 `WinKO true` em ambos; as vitórias
acumuladas coincidem com `Wins`, e a partida encerra na segunda vitória.
`WinSide` no log é baseado em zero (1 representa P2). Isso comprova transição
e encerramento no cenário 2–0, sem comprovar restauração de todos os recursos,
uma partida equilibrada 2–1 ou a qualidade audível do som.

## Reprodução

```bash
python3 scripts/build_characters.py
python3 tests/validate.py
python3 -O tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/match_smoke.py
python3 tests/match_smoke.py --audio
python3 tests/keyboard_smoke.py
```

Reconstrução verificada: os 16 arquivos gerados dos dois personagens mantiveram
os mesmos hashes SHA256. O workflow `.github/workflows/validate.yml` repete
reconstrução/diff, validação normal/com `-O` e regressões em push/PR; sua execução
remota ainda depende do GitHub Actions. Os testes
estáticos não requerem desktop. Os testes de jogo requerem X11 desbloqueado e
OpenGL; o de teclado também requer libX11, libXtst, xwininfo e ffmpeg. Executar
os testes gráficos **sequencialmente**. O teste de teclado foca a janela Ikemen
e injeta teclas; não executar durante uso de outra aplicação.

Cada teste de jogo usa um log temporário novo, exige código 0 e só aceita
resultados da execução atual. O smoke de rounds tem limite de 90 s; timeout é
falha, não aprovação, e não substitui os logs anteriores. Em falha de validação
o log final é preservado para diagnóstico, portanto um arquivo presente não
significa PASS. Logs de execuções aprovadas são copiados para `tests/`.
O teste de teclado usa o DISPLAY atual na captura e não modifica controles.

## Ambiente e histórico

Ubuntu 22.04.5 LTS x86_64, Intel UHD 620; nesta execução o motor reportou
OpenGL 4.6 Core, Mesa 23.2.1. O sandbox não acessou X11: a primeira tentativa
falhou em inicialização GTK/GFX, código 2. As execuções aprovadas ocorreram
fora do sandbox, sem instalar pacotes ou modificar o motor.

Os testes históricos `tests/ai-match.log` e `tests/ko-match.log` foram produzidos
antes da sprint. Eles não validam os sprites novos. O launcher continua limpando
variáveis GTK/GIO que causavam conflitos no ambiente VS Code Snap. O aviso de
PosFreeze foi tratado anteriormente somente nas cópias adaptadas.

## Roteiro manual pendente (registrar resultado, versão e evidência)

1. Executar `./scripts/play.sh`; movimentar, virar, pular, agachar, aterrissar,
   defender alto/baixo, receber golpes e cair com ambos os personagens.
   Com as caixas de debug do motor habilitadas, conferir sprites/caixas por
   frame e nos dois sentidos, incluindo recuperação e agarrões.
2. Conferir alcance, recuperação e hitstun de x/y/a/b em pé, agachado e no ar;
   verificar guarda direcional, parry e cancelamentos KFM listados em COMMANDS.md.
3. Jogar melhor de três com `./scripts/play.sh -rounds 2`: concluir 2–0 e 2–1
   por KO; conferir reset de vida, posição, cronômetro e comportamento do power
   entre rounds, placar e encerramento após a segunda vitória.
4. Deixar o tempo terminar com vida diferente e igual. Registrar resultado de
   vitória/empate e a política de rounds adicionais antes de afirmar aprovação.
5. Executar `./scripts/play.sh --menu`; selecionar Versus e os personagens.
6. Repetir uma partida completa com áudio e duas pessoas; avaliar som, latência,
   teclas simultâneas e conforto. Se travar, registrar tempo de parede, round,
   foco/pausa, comando completo, stdout/stderr e uma repetição com `-nosound`.

O trecho acima registra a Sprint 1. A Sprint 2 abaixo acrescenta Ki e especiais
DBZ; arte final e balanceamento humano continuam pendentes.

## Sprint 2 — 16/10/2026

A validação manual final permanece **pendente**. Testes automatizados não
substituem uma pessoa executar os comandos e disputar uma partida completa.

Implementação: Ki inicial padrão 0, máximo 3.000, carga 25/tick (40 ticks por
especial), custo 1.000. Reset em todos os rounds, sem persistência. Parâmetros
em `assets-source/combat.json`; reconstruir antes de validar alterações.

Reprodução adicional:

```bash
python3 tests/sprint2_smoke.py
```

Esse teste precisa X11 desbloqueado, libX11/libXtst, xwininfo e ffmpeg; foca o
Ikemen e injeta teclas. Copia config.ini para um diretório temporário e ativa
telemetria somente nessa cópia. Não altera controles ou regras persistidas.
Executar isoladamente, depois dos builds, e sequencialmente aos outros testes
gráficos. Exige evidência nova além do código de saída:

- ambos os jogadores tentam QCF+y sem Ki: nem 7100 nem Palm 1010 são executados;
- carga real por teclas e limite 3.000, sem exceder ou ficar negativo;
- entrada de cada especial desconta exatamente 1.000 uma única vez;
- projéteis reais aparecem, colidem e causam o dano nominal configurado;
- guardar para trás registra ProjGuardedTime e mantém vida (chip zero);
- um projétil interrompe Vegeta enquanto carrega: sai de 7000 para gethit;
- ambos os medidores existem durante o combate;
- round real termina por tempo com vidas diferentes; no seguinte ambos têm Ki 0.

`tests/sprint2-trace.csv` é a evidência aprovada por frame; colunas:
tick, player, round, roundstate, stateno, life, Ki, numproj, projHitTime(7100),
projGuardedTime(7100), numexplod(7200). `tests/sprint2-effects.png` captura a
carga dos dois personagens. Em falha a coleta vai para `sprint2-failed.csv`
(ignorada pelo Git), não substituindo a evidência aprovada.

Os testes unitários também rejeitam coleta vazia, jogador ausente, custo
incorreto, ausência de hit/guarda/medidor e reset ausente. Não simulam a física
do motor: fixtures unitárias testam o verificador; somente o smoke X11 comprova
as mecânicas de combate. Os testes de geometria continuam exigindo todos os
604 frames herdados por personagem, sem relaxar sua cobertura/timing.

Na preparação, as validações estáticas da Sprint 1 passaram. O cenário antigo
com tempo de 10 s terminou com um empate intermediário e foi corretamente
reprovado, tanto sem som quanto com áudio. O timeout do cenário foi ampliado
para 30 s por round (limite de parede permanece 90 s), mantendo todas as
exigências de dois KOs, placar e transições. Essa falha não foi contada como PASS.

### Aceite humano pendente

1. Executar com dois jogadores: carregar, soltar um chute, sofrer golpe na
   carga/preparo, confirmar aura, barra e custo, incluindo facing invertido.
2. Acertar e defender cada especial em pé/agachado/no ar; conferir os projéteis
   e impactos azul/roxo e colisão entre dois disparos simultâneos.
3. Confirmar combo normal→especial, erro de comando, tentativa com 999 Ki,
   limite de um projétil, alcance, prioridade e recovery punível.
4. Conferir que supers/EX KFM só consomem power; testar agarrões/parry e todos
   os normais, especialmente sweep e ataques aéreos sem cancelamento DBZ.
5. Disputar melhor de três completa, 2–0 e 2–1, com áudio; avaliar ritmo arcade,
   responsividade, ghosting e reset de Ki. Registrar versão, resultado e evidência.

Nenhuma dessas etapas humanas foi declarada concluída.

### Resultados automatizados da Sprint 2

| Verificação | Resultado |
| --- | --- |
| `validate.py`, normal e `-O` | PASS: 861 sprites, 670 frames AIR, 604 frames herdados alinhados por personagem; hash do motor preservado. |
| Unittest | PASS: 10 testes, incluindo as seis regressões anteriores e quatro verificações DBZ. |
| Reconstrução | PASS: mesmos hashes dos 16 arquivos gerados em uma reconstrução sem mudanças de fonte. |
| `sprint2_smoke.py` | PASS: comandos reais, Ki/custo/limite, dano/guarda, interrupção e reset no motor, dois jogadores. |
| `match_smoke.py` | PASS: 30,05 s, dois KOs, dois rounds, placar 0–2, código 0, cenário com 30 s por round. |
| `match_smoke.py --audio` | PASS: 39,59 s, dois KOs, dois rounds, placar 0–2, código 0. |
| `keyboard_smoke.py` | PASS: AILevel 0 nos dois lados; vidas finais 774/874, ambos causaram dano; código 0. |

Execuções gráficas fora do sandbox, OpenGL 4.6/Mesa 23.2.1/Intel UHD 620.
A comparação com áudio verifica conclusão e resultados; qualidade audível,
latência e conforto continuam pendentes de avaliação humana. A captura da
carga confirma aura e medidores azul/roxo; não valida todos os frames/impactos.

## Sprint 3 — 16/10/2026

Prévia estática da Sprint 2: validate normal/-O e 10 unittests aprovados antes
das alterações. Nova branch deriva da referência local Sprint 2.

| Verificação da implementação mínima | Resultado |
| --- | --- |
| validate.py normal e -O | PASS: 861 sprites, 670 frames e 604 contextos alinhados por personagem; hash do motor inalterado. |
| Unittest | PASS: 12 testes; inclui importação real de RGBA, alpha/origem/paleta, alpha parcial e caminho inválidos, SFF da arena, caixas/offsets/flips e verificadores de Ki. |
| match_smoke.py | PASS: 27,12 s, dois KOs, 0–2, saída 0. |
| match_smoke.py --audio | PASS: 54,76 s, dois KOs, 0–2, saída 0. |
| sprint2_smoke.py | PASS: comandos, carga, custo, limite, projéteis, dano, guarda, interrupção, medidores e reset, ambos os jogadores. |
| keyboard_smoke.py | PASS: AILevel 0; ambos causaram dano; vidas finais 711/811; captura tests/gameplay.png. |
| GNU time do smoke DBZ | PASS: 40,16 s; CPU user 11,41 s/system 2,40 s; RSS máximo 418.612 KiB; zero swaps; saída 0. |

`tests/sprint3-performance.txt` contém a medição atual; reproduzir com
`python3 tests/performance_smoke.py` (X11). Limites de recurso desta demonstração:
1 GiB RSS e 90 s para o cenário completo. Validar relatório existente com
`python3 tests/performance_smoke.py --report tests/sprint3-performance.txt`.
Isso mede o processo de teste/motor e captura; não mede percentis de frame,
FPS ou latência de entrada. Benchmark de frame time/GPU permanece pendente.

Captura automática atual de carga/arena: `tests/sprint2-effects.png`.
Telemetria atual de Ki/projéteis: `tests/sprint2-trace.csv`.
Testes gráficos executados sequencialmente fora do sandbox; tentativa inicial
no sandbox falhou ao inicializar GTK/X11 e não foi contada como aprovação.
Ubuntu 22.04/Mesa 23.2.1/Intel UHD 620, OpenGL 4.6 reportado pelo motor.

A inspeção da captura confirma integração do palco, silhuetas laranja/azul e
medidores azul/roxo. **Não constitui aceite visual humano**. Os sprites continuam
geométricos e provisórios, incluindo os PNGs de exemplo. Idle, caminhada,
agachamento, salto, ataques, defesa, dano, queda e vitória mantêm o AIR funcional
herdado; todos ainda exigem arte orgânica e avaliação por pessoa nos dois lados.
O teste automático garante as caixas e tempos herdados por frame; não garante
qualidade artística, contatos naturais ou conforto. Alpha parcial é rejeitado
por limitação explícita do pipeline SFF v1. Roteiros humanos das Sprints 1/2
continuam pendentes, acrescidos da inspeção do cenário, HUD e facing dos PNGs.

Reconstrução completa da Sprint 3: PASS, SHA256 idêntico nos 19 arquivos
(dos dois personagens, SFF/DEF da arena e fight.def). O CI inclui esses alvos;
execução remota do workflow ainda não verificada nesta sessão.


## Sprint 4 — 16/10/2026

Esta seção substitui as limitações de alpha/cobertura descritas historicamente
nas Sprints 1–3. **Nenhum teste manual foi declarado concluído.** O critério de
Goku orgânico foi demonstrado em uma partida automatizada real; o aceite
artístico/humano da Sprint permanece pendente.

O SFF dos dois personagens é 2.0.1 PNG32, sem quantização RGBA. São 861 entradas
por personagem; imagens idênticas compartilham payload/textura por links para
índices anteriores. Goku: 233 imagens únicas e 628 links; Vegeta: 225 imagens
únicas e 636 links. O parser rejeita seções inválidas, links cíclicos/futuros,
geometria divergente e PNGs corrompidos. Não há alterações de motor, estados de
combate, entradas, áudio KFM, controles personalizados ou parâmetros de Ki.

A validação compara os 604 contextos herdados, mantendo tempos, offsets,
flips e hitboxes. Somente frames explicitamente orgânicos substituem a
ocupação exata da união por bounds previstos, origem/canvas, SHA256 da fonte,
alpha reconstruído exato e interseção por caixa. Os demais placeholders ainda
precisam cobrir exatamente a união. Ajustes de hurtbox opcionais no manifesto
são comparados às caixas aplicadas e testados sem alterar tempos/hitboxes.
Interseção não certifica alcance natural ou balanceamento; revisar no motor.
Metadados de facing são validados; a orientação semântica do desenho requer
inspeção. A captura de Goku × Goku mostra os dois sentidos no motor real.

Goku possui 55 bindings orgânicos (52 herdados e 3 DBZ) usando 19 PNGs distintos.
Há 20 desenhos normalizados disponíveis: o quarto follow-through do Kamehameha
fica como candidato, pois o AIR original tem três elementos. Caminhada frente
usa quatro desenhos mantidos por quatro elementos herdados cada, ciclo de
48 ticks; para trás inverte a ordem. Os pés ficam em y=240 após reamostragem.
Não se alonga a imagem para preencher caixas. Extração por retângulos explícitos
rejeita recorte visível antes da redução; o alpha parcial é preservado.

### Regressões desta execução

- `validate.py`, normal e `-O`: PASS, 861 sprites/670 elementos AIR/604 contextos
  por personagem; SHA256 do motor preservado.
- Unittest: PASS, 21 testes. Incluem as regressões anteriores, alpha parcial
  real, determinismo, links inválidos, hash/crop/origem/escala/facing, caixas
  independentes e evidência de sprites incompleta.
- `sprint4_smoke.py`: PASS, Goku nos dois jogadores, quatro primeiros elementos
  de idle, caminhada frente/trás e soco; telemetria fresca e captura real.
- `keyboard_smoke.py`: PASS, dois humanos simulados por teclado (AILevel 0),
  ambos causaram dano; vidas finais 711/811; saída 0.
- `match_smoke.py`: PASS, 32,51 s, dois rounds/dois KOs, placar 0–2; saída 0.
- `match_smoke.py --audio`: PASS, 39,03 s, dois rounds/dois KOs, placar 0–2;
  saída 0. Qualidade audível não foi avaliada por pessoa.
- `sprint2_smoke.py`, executado por `performance_smoke.py`: PASS, carga, teto,
  custo, hit/guard, projéteis, interrupção, medidores e reset para ambos.
- Recursos após deduplicação: PASS, 482.984 KiB RSS máximo, 39,90 s, zero swaps;
  limite 1 GiB/90 s. Isso não mede FPS, latência ou percentis de frame.

Evidências atuais: `tests/sprint4-facings.png`, `tests/sprint4-sprites.csv`,
`tests/gameplay.png`, `tests/sprint2-effects.png`, `tests/sprint2-trace.csv`,
logs de rounds/teclado e `tests/sprint4-performance.txt`. O relatório Sprint 3
foi preservado como histórico. A primeira medição sem links chegou a
1.004.512 KiB; `sprint4-performance-before-dedup.txt` registra o custo que motivou
a deduplicação. Tentativa no sandbox sem X11 e uma execução interrompida com
código 143 não foram contadas como PASS. As execuções gráficas aprovadas foram
sequenciais, fora do sandbox, OpenGL 4.6/Mesa 23.2.1/Intel UHD 620.

Reconstrução completa: PASS, duas execuções idênticas de 19 artefatos do motor
e 24 fontes/manifestos. Hashes finais: `docs/sprint4-build-sha256.json`.
CI inclui extração dos PNGs e reconstrução; execução remota precisa ser
confirmada após publicação do PR. Não reutilizar evidência histórica como se
fosse uma execução nova. Testes gráficos focam Ikemen/injetam teclas e exigem
desktop X11 desbloqueado; não executar enquanto se usa outra aplicação.

### Reprodução adicional

```sh
python3 scripts/prepare_character_art.py goku
python3 scripts/prepare_character_art.py vegeta
python3 scripts/build_characters.py
python3 scripts/build_arena.py
python3 scripts/build_interface.py
python3 tests/validate.py
python3 -O tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/sprint4_smoke.py
python3 tests/keyboard_smoke.py
python3 tests/match_smoke.py
python3 tests/match_smoke.py --audio
/usr/bin/time -v -o tests/sprint4-performance.txt python3 tests/sprint2_smoke.py
python3 tests/performance_smoke.py --report tests/sprint4-performance.txt
```

### Aceite artístico/humano pendente

Inspecionar Goku nos dois sentidos, todos os desenhos e as transições para
placeholders; conferir estabilidade de proporções/iluminação/pés, contornos,
contato do soco e posição das mãos no spawn do Kamehameha. Revisar caixas com
debug do motor e testar agarrões, todas as posturas, partida 2–1, áudio e dois
jogadores reais. Produzir arte restante/carga de Ki/Vegeta. Proveniência e
limites de licença em `ART_PROVENANCE.md`; não há licença oficial registrada.

## Sprint 5 — 16/10/2026

Avaliação humana/artística: **pendente**. As verificações abaixo são estáticas
ou automatizadas no motor; não são uma sessão de jogo com pessoas.

Antes das mudanças, validate e 21 unittests da Sprint 4 passaram; seu smoke
Goku × Goku também foi repetido no X11. Primeiro idle/caminhada de Vegeta foi
capturado em `tests/sprint5-initial-facings.png`, com telemetria fresca.

Implementação final: 637 bindings orgânicos por personagem (604 contextos com
caixas, 28 sprites de corpo sem caixas, duas poses de carga e três de disparo).
`audit_animations.py --complete` passa sem placeholders nas sequências de corpo
verificadas, incluindo recuperação do chute e agarrões sem hurtboxes. Props de
introdução, retratos e sprites legados não utilizados não são certificados como
orgânicos. As famílias adicionais KFM reutilizam candidatos; ver limites visuais.

| Verificação estática | Resultado desta execução |
| --- | --- |
| validate normal e `-O` | PASS: 861 sprites / 670 elementos AIR / 604 contextos com caixas por personagem; motor fixado preservado. |
| Integridade RGBA | PASS: hash dos pixels completos e alpha do SFF iguais à fonte normalizada em todos os bindings orgânicos, inclusive links. |
| Unittest | PASS: 26 testes, incluindo rejeição de sequência estática, binding ausente, pé fora do piso, extração com alpha parcial e offsets/flips com coordenadas explícitas. |
| Auditoria completa | PASS: desenhos distintos por sequência, origem/canvas, piso terrestre, variação de altura de idle/walk <=8 px; zero ações de corpo herdadas com placeholders. |
| Reconstrução | PASS: fontes/manifestos/SFF, arena e interface iguais em duas execuções; 753 arquivos retidos em `sprint5-build-sha256.json`, após retirar oito variantes órfãs criadas nesta sprint. Cache PNG preservou os bytes anteriores do SFF. |

Reprodução:

```sh
python3 scripts/prepare_character_art.py goku
python3 scripts/prepare_character_art.py vegeta
python3 scripts/build_characters.py
python3 scripts/build_arena.py
python3 scripts/build_interface.py
python3 tests/validate.py
python3 -O tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/audit_animations.py --complete --report docs/sprint5-animation-audit.json
python3 tests/sprint5_graphics.py
```

O último comando roda as regressões gráficas anteriores sequencialmente e depois
`capture_demo.py` sob GNU time: captura Goku × Vegeta e Vegeta × Goku, confirma
idle/caminhada/soco orgânicos por telemetria e grava o teste real de Ki/especiais.
O vídeo MP4 captura a janela X11 em tempo real e nunca é conteúdo do jogo.
A medição agora cobre as duas capturas de sprites e o smoke Ki, portanto o tempo
de parede não é comparável diretamente ao cenário Ki isolado das sprints antigas.
Mantidos os limites 1 GiB/90 s; sem afirmação de FPS ou latência.

Evidências: `sprint5-facings.png`, `sprint5-reversed-facings.png`, respectivos CSVs,
`sprint5-gameplay.mp4`, `sprint5-performance.txt`, `sprint2-trace.csv`, captura de
carga e logs de rounds/teclado. Contact sheets `sprint5-{goku,vegeta}-contact.png`
são prévias dos assets, explicitamente não capturas de gameplay.

A comparação de caixas preserva todos os tempos/hitboxes e todas as hurtboxes
exceto dois overrides explícitos de cabeça no soco forte. Essas mudanças precisam
de revisão de balanceamento. Interseção não prova contato natural. Normalização
de pés e hashes distintos não comprovam anatomia, passos ou fluidez. Inspeção das
folhas/capturas pelo agente está separada do aceite humano em
`SPRINT_5_VISUAL_REVIEW.md`. Roteiros humanos anteriores continuam pendentes,
incluindo menu/seleção, 2–1 equilibrado, duas pessoas, áudio e agarrões.

### Resultados gráficos finais da Sprint 5

| Teste no motor | Resultado |
| --- | --- |
| Sprint 4 Goku × Goku | PASS: idle, caminhar frente/trás e soco, telemetria fresca e captura nos dois lados. |
| Teclado, AILevel 0 | PASS: ambos causaram dano, vidas finais 711/811, saída 0. |
| Partida sem som | PASS: dois rounds, dois KOs, 0–2, 34,80 s, saída 0. |
| Partida com áudio | PASS: dois rounds, dois KOs, 0–2, 31,55 s, saída 0; qualidade audível não avaliada. |
| Goku × Vegeta e ordem invertida | PASS: idle, caminhada frente/trás e soco; sprites observados orgânicos em ambos os jogadores; capturas e CSVs novos. |
| Ki e especiais + gravação | PASS: carga/teto/custo, projéteis, dano nominal, guarda, interrupção, medidores e reset de round; saída 0. |
| Recursos, captura dupla + Ki | PASS: 338.140 KiB RSS máximo, 56,30 s; limites 1 GiB/90 s. |

Vídeo `tests/sprint5-gameplay.mp4`; metadados em `sprint5-video.json` e frame
extraído em `sprint5-video-frame.png`. Captura real, sem áudio e sem uso como
conteúdo do jogo. Os resultados não comprovam toda a coreografia ou arte final.

Duas tentativas de captura foram reprovadas antes da execução aprovada: uma
falhou com X11 BadMatch ao focar uma janela ainda não visível; outra confirmou
as mecânicas, mas excedeu o timeout ao enviar Escape após a gravação. O harness
passou a aguardar `IsViewable` e restaurar o foco antes de encerrar. Repetida
somente a etapa afetada com `tests/sprint5_graphics.py --capture-only`; saída 0,
telemetria fresca e gravação nova. Nenhuma dessas falhas foi contada como PASS.
O sandbox também bloqueou o display no começo da auditoria; os testes gráficos
aprovados rodaram fora dele, sequencialmente, OpenGL 4.6/Mesa 23.2.1/UHD 620.

Após a primeira gravação, a inspeção de um frame revelou recorte de idle/guarda
na borda da viewport. `screenleft/screenright` passaram de 15 para 40. A regressão
da arena agora compara a margem ao extremo negativo real dos PNGs de idle, walk
e guard (nos dois facings), em vez de apenas fixar um número. Todas as regressões
gráficas foram repetidas após esse ajuste; a tabela acima registra essa execução
final. Os hashes da arena foram atualizados após duas reconstruções idênticas.

Publicação/CI remoto: bloqueados por autenticação/escrita. Push HTTPS fora do
sandbox não tem credencial; o conector GitHub retornou 403 ao criar blob.
Implementação local commitada; nenhum PR Sprint 5 foi criado. Detalhes e descrição
preparada em `PR_SPRINT_5.md`. Isso não invalida os resultados locais, mas impede
confirmar o workflow remoto até que a branch possa ser publicada.

## Sprint 6 — 17/10/2026

Auditoria antes das mudanças: validate normal e `-O` PASS, 26 unittests PASS;
`tests/sprint5_graphics.py` PASS no X11, incluindo teclado, dois KOs 0–2 com
som/sem som, ordem invertida de personagens e Ki/especiais com gravação.
Evidências preservadas em `evidence/sprint6/baseline/`.

Reprodução e distinção entre prévia de assets e captura real:
[evidence/sprint6/README.md](../evidence/sprint6/README.md). Novos testes de
coordenadas conhecidas cobrem offsets/flips/facing, piso/franja opaca,
arte vazia/recortada e preservação de todos os contratos fora do idle.
O verificador anterior de piso, escala, hashes distintos, integridade SFF/AIR,
Ki, colisões e rounds permanece ativo. A nova coleta mede diferença de alpha;
não certifica continuidade perceptual. Estados comuns continuam fornecidos
pelo motor fixado; não foram reimplementados.

A primeira execução final passou teclado e rounds, mas falhou na interrupção
da carga. Não foi contada como PASS. Coleta preservada em
`evidence/sprint6/failed-attempt/`: o alvo não entrou em 7000 nessa etapa.
Não foi isolada causa no combate; o harness passou a renovar foco antes do
comando e confirmar entrada em carga antes do disparo. A repetição mantém
as mesmas exigências de dano, guarda, interrupção e reset, sem relaxamento.

### Resultados finais da Sprint 6

| Verificação | Resultado automatizado |
| --- | --- |
| validate normal / `-O` | PASS; 861 sprites, 670 frames AIR, 604 contextos herdados por personagem; motor fixado preservado. |
| Unittests | PASS: 31; inclui todos os contextos orgânicos espelhados, inventário e alteração restrita de idle. |
| Auditoria completa | PASS: 637 bindings orgânicos por personagem; isso não aprova coreografia KFM nem arte. |
| Idle | Retenções máximas de 45 para 12 ticks, ciclo de 151 para 118; mesmas poses/caixas. |
| Goku × Goku e ordens Goku/Vegeta | PASS: progressão de sprites, caminhada frente/trás e soco, ambos os jogadores. |
| Teclado | PASS: ambos causaram dano; vidas finais 711/811. |
| Dois rounds / dois KOs / placar 0–2 | PASS sem som (42,78 s) e com áudio (34,38 s), saída 0. |
| Ki, projéteis, dano nominal, defesa, interrupção, medidores, reset | PASS com Goku à esquerda e Vegeta à direita; PASS com personagens invertidos. |
| Recursos captura dupla + Ki | PASS: 338.400 KiB RSS, 55,87 s; limites 1 GiB/90 s. |
| Recursos Ki invertido + vídeo | PASS: 338.328 KiB RSS, 38,82 s; mesmos limites. |

A suíte completa demorou 211,46 s; o limite de 90 s é por cenário medido,
não para a suíte inteira. `runtime/result.json` registra PASS, e os relatórios
GNU time têm código 0. Os dois MP4 são capturas reais atuais; metadados ffprobe
e frames extraídos estão junto dos vídeos. Renderização: OpenGL 4.6 Core,
Mesa 23.2.1, Intel UHD 620, X11 fora do sandbox. Nenhum teste manual foi feito.

Todos os entregáveis locais ficam na branch da Sprint 6. Publicação/PR draft
não concluídos: push HTTPS sem credencial e conector GitHub com 403 de escrita.
Descrição pronta em `PR_SPRINT_6.md`; CI remoto não executado por esta entrega.

Reconstrução final: prepare_character_art de ambos os personagens, build de
personagens, arena e interface repetidos; os mesmos hashes SHA256 em **753
arquivos** antes/depois. Inventário em `evidence/sprint6/build-sha256.json`.
Nenhum sprite/SFF, fonte ou arquivo do motor teve alteração incidental.
Somente os AIR adaptados têm a mudança intencional de duração do idle.
