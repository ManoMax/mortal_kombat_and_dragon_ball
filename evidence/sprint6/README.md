# Evidências da Sprint 6

`baseline/`: regressões da base c626c91 antes do polimento, aprovadas no desktop
X11 em 17/10/2026. Nomes internos mantêm a sprint do harness reutilizado.
`assets/`: prévias AIR dos assets após o ajuste de cadência. PNG = elementos
lado a lado, cada célula com os dois facings; GIF = sequência temporal. Não são
capturas de gameplay. `inspection.json` inclui todas as ações e contratos
CNS/CMD; `feet.csv` inclui alinhamento da faixa opaca dos pés/corpo.
`runtime/`: execuções finais reais, capturas, vídeos, telemetria e recursos.
O arquivo `result.json` só registra `pass` se todas as etapas terminarem.
`failed-attempt/`: primeira coleta final reprovada na etapa de interrupção;
não constitui evidência aprovada. A causa de ausência do estado de carga não
foi isolada; o harness agora exige observar a carga antes do ataque e renova foco.

Reprodução, na raiz do repositório:

```sh
python3 scripts/build_characters.py
python3 tests/validate.py
python3 -O tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/audit_animations.py --complete
python3 scripts/inspect_combat.py --hitboxes
python3 tests/sprint6_graphics.py
```

Omitir `--hitboxes` remove as caixas das prévias. `--actions 0,20,800,810,820`
exporta outras ações; usar outro `--output` para não misturar subconjuntos.
O relatório JSON/CSV sempre cobre todas as ações, mesmo selecionando prévias.
As prévias usam origem de jogador (160,240); não simulam câmera, física,
velocidade de caminhada, binds, state controllers nem avanço de rounds.

O último comando requer X11 desbloqueado, OpenGL, libX11/libXtst, xwininfo,
ffmpeg e GNU time. Foca a janela IKEMEN e injeta teclas; executar isoladamente.
Não sobrescreve configuração nem controles e restaura os artefatos históricos
após copiá-los para runtime. Executar testes gráficos sequencialmente.
As gravações são da janela real, sem áudio; entradas são automatizadas.
`reversed-gameplay.mp4` coloca Vegeta à esquerda e Goku à direita. O vídeo com
nome `sprint5-gameplay.mp4` nesta pasta é da execução atual do harness herdado,
com Goku à esquerda e Vegeta à direita, não uma cópia do vídeo histórico.

Medição de desempenho: pico RSS e duração do cenário; limites 1 GiB/90 s.
Não mede FPS, frame time, latência ou qualidade audível. Aprovação automatizada
não é aprovação artística nem teste jogado por pessoas. Revisão e desenhos
necessários em `docs/SPRINT_6_VISUAL_REVIEW.md`.

`build-sha256.json` registra os 753 arquivos do inventário de build herdado,
após repetir extração dos dois personagens e builds de personagens, arena e
interface. Os hashes antes e depois dessa reconstrução coincidiram.
