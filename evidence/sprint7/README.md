# Sprint 7 — evidência e limites

Entrega parcial: oito desenhos de caminhada novos, integrados. **Aceite
artístico bloqueado** por apoio, transições e consistência anatômica.
Não há desenhos novos de combate nem model sheet completo aprovado.

## Comparações e animações

- `assets/{goku,vegeta}-walk-before-after.png`: quatro poses da Sprint 6 em
  cima, quatro candidatas da Sprint 7 embaixo, mesma escala de exibição.
- `assets/*-walk-source.gif`: ciclo dos quatro PNGs normalizados, 200 ms por
  desenho. São prévias de arte, não capturas do motor.
- `assets/*-{20,21}.gif` e `*-frames.png`: elementos AIR, caixas e dois
  facings. Relatórios em `inspection.json`, `feet.csv`, `animation-audit.json`.
- `runtime/{goku,vegeta}-walk-engine.gif`: trechos da janela real do IKEMEN,
  extraídos de `walk-review.mp4`. Sem montagem de sprites sobre cenário.
- `runtime/walk-engine-samples.png`: oito frames reais amostrados da captura
  dedicada; originais individuais `walk-sample-*.png`.

## Motor real

`runtime/sprint5-gameplay.mp4`: **32,959 s**, Goku à esquerda, Vegeta à direita.
`runtime/reversed-gameplay.mp4`: **33,034 s**, personagens invertidos.
São novas gravações desta branch pelo harness herdado, apesar do nome
`sprint5`. Ambos incluem gameplay real, Ki e especiais; não são vídeos
inseridos no jogo. Metadados ffprobe acompanham os arquivos. Gravações sem áudio.

`runtime/walk-review.mp4`: **14,167 s a 60 fps**, três repetições de ciclos
completos de avanço/recuo de cada personagem, entradas automatizadas.
`walk-coverage.json` comprova as quatro poses fontes nas ações 20 e 21 de
ambos, incluindo todos os sprites 30000,20–51. Isso comprova integração,
não ausência de deslizamento ou aprovação artística.

`runtime/walk-review-reversed.mp4`: **14,134 s a 60 fps**, mesma verificação
com Vegeta à esquerda e Goku à direita. `walk-reversed-coverage.json` confirma
as quatro poses nas duas ações também nessa ordem. GIFs `*-engine-reversed.gif`
e dois frames individuais permitem inspecionar cada personagem no facing oposto.

Suite herdada completa: **PASS**, em `runtime/result.json`. Inclui Goku × Goku,
duas ordens dos personagens, dano por teclado, dois rounds/dois KOs/placar 0–2
com e sem áudio, Ki/carga/custo/projéteis/dano/guarda/interrupção/medidores/reset.
Recursos: 344.920 KiB/55,52 s no cenário principal, 344.676 KiB/38,58 s no
invertido; limites 1 GiB e 90 s por cenário medido.

Estáticos: validate normal e `-O` PASS, 31 unittests PASS, auditoria completa
PASS. Motor fixado preservado: 861 sprites e 670 elementos AIR por personagem,
604 contextos herdados com caixas. `baseline/contracts.json` fixa AIR/CNS/CMD;
os hashes permanecem iguais. Somente 32 dos 637 bindings mudaram por personagem.

Primeira tentativa gráfica no sandbox: falhou antes de abrir o motor, por
ausência de acesso ao X11; registrada em `failed-sandbox-result.json`, sem
contar como aprovação. As execuções aprovadas ocorreram no desktop X11,
OpenGL 4.6 Core/Mesa 23.2.1/Intel UHD 620. Controles e artefatos históricos dos
testes herdados foram preservados. Nenhuma sessão humana foi feita.

A primeira comparação de reconstrução detectou somente ordenação diferente
dos dois manifestos: uma ordenação manual para reduzir o diff discordava da
ordem do extrator. Os registros passaram a usar diretamente a ordem do
extrator. Nenhum PNG/SFF/AIR/CNS/CMD mudou nessa correção. Tentativa preservada
em `rebuild-first-attempt.json`; resultado final em `rebuild-result.json`.
Reconstrução final: **PASS, os mesmos hashes em 742 arquivos** após repetir
extração dos dois personagens e builds de personagens, arena e interface.

## Reprodução

Na raiz do repositório:

```sh
python3 scripts/prepare_character_art.py goku
python3 scripts/prepare_character_art.py vegeta
python3 scripts/build_characters.py
python3 tests/validate.py
python3 -O tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/audit_animations.py --complete --report evidence/sprint7/animation-audit.json
python3 scripts/sprint7_evidence.py
python3 scripts/inspect_combat.py --output evidence/sprint7/assets --actions 20,21 --hitboxes
python3 tests/sprint6_graphics.py --output evidence/sprint7/runtime
python3 tests/sprint4_smoke.py --opponent vegeta --prefix sprint7-walk --organic --walk-review evidence/sprint7/runtime/walk-review.mp4
python3 tests/sprint4_smoke.py --fighter vegeta --opponent goku --prefix sprint7-walk-reversed --organic --walk-review evidence/sprint7/runtime/walk-review-reversed.mp4
```

Executar os três últimos sequencialmente, em X11 desbloqueado: focam o jogo
e injetam teclas. O último gera também `tests/sprint7-walk-{facings.png,sprites.csv}`;
nesta entrega foram movidos para runtime. Build e previews são determinísticos;
a geração artística é preservada em PNG e não se reproduz por seed.

Revisão e problemas ainda abertos: `docs/SPRINT_7_VISUAL_REVIEW.md`.
Prompts finais: `assets-source/sprites/sprint7-prompts.md`.
