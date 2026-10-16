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

Não há mecânicas Dragon Ball novas nesta sprint. Power e especiais continuam
sendo KFM. Arte final, balanceamento e remoção de comandos estão fora do aceite
atual; decisões propostas estão em COMMANDS.md.
