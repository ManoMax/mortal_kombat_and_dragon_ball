# Testes — 16/10/2026

## Ambiente confirmado

Ubuntu 22.04.5 LTS x86_64, kernel 6.8.0-138, glibc 2.35.
Renderer reportado pelo motor: OpenGL 4.6 Core, Mesa 23.2.1,
Intel UHD Graphics 620 (WHL GT2). /dev/dri não estava visível no sandbox;
a inicialização gráfica fora dele identificou a GPU.
Git, curl, unzip, Python 3, FFmpeg e libXtst já existiam. Nenhum pacote global instalado.

## Implementado e testado

- Download v1.0.0 com SHA256 idêntico ao manifesto oficial.
- Binário executa e inicializa GFX/fontes. Distribuição contém suas bibliotecas.
- `python3 tests/validate.py`: PASS para ambos os personagens, 242 sprites cada,
  cadeia SFF válida e todas as referências AIR resolvidas.
- IA vs IA, 10 segundos, um round: processo saiu com código 0. Log
  `tests/ai-match.log`: Goku 875/1000, Vegeta 1000/1000, vitória por tempo.
- IA vs IA, vida inicial 80, 30 segundos: código 0; `tests/ko-match.log`
  registra Goku 0, Vegeta 80, WinKO true. Confirma dano e nocaute.
- Captura `tests/gameplay.png` inspecionada: ambos os sprites, cenário,
  barras de vida reduzidas, nomes e cronômetro renderizados corretamente.

- `python3 tests/keyboard_smoke.py`: PASS. Dois jogadores com AILevel 0;
  vida final Goku 711/1000 (início 900), Vegeta 811/1000. Ambos causaram dano;
  processo encerrou com código 0 e resultado em `tests/keyboard-match.log`.

## Procedimentos reproduzíveis

```bash
python3 tests/validate.py
./scripts/play.sh -nosound -p1.ai 8 -p2.ai 8 -time 10 -rounds 1 -log ../tests/ai-match.log
./scripts/play.sh -nosound -p1.ai 8 -p2.ai 8 -p1.life 80 -p2.life 80 -time 30 -rounds 1 -log ../tests/ko-match.log
python3 tests/keyboard_smoke.py
```

O teste de teclado requer X11 desbloqueado, libX11, libXtst, xwininfo e ffmpeg.
Foca exclusivamente a janela Ikemen GO, simula movimento, socos, pulos,
agachamentos e chutes nos dois jogadores. Não executar enquanto alguém usa
outra aplicação. Vida inicial assimétrica evita empate e round extra.

## Implementado, ainda sem validação manual completa

Defesa alta/baixa, hitstun, combos, todos os ataques em todas as posturas,
seleção no menu e melhor de três configurada pelo motor.
Entradas automatizadas não substituem uma partida com duas pessoas.
Áudio disponível no pacote, mas testes de combate usaram -nosound.

## Roteiro manual pendente

1. Executar play.sh; mover ambos, pular e agachar.
2. Conferir alcance e recuperação de cada soco/chute no chão e no ar.
3. Defender alto/baixo e conferir redução de dano/hitstun.
4. Ganhar dois rounds por KO; verificar transição e encerramento.
5. Deixar tempo terminar com vida diferente e igual; verificar vitória/empate.
6. Abrir --menu, escolher Versus e ambos os personagens.
7. Conferir som, latência, teclas simultâneas e conforto em partida real.

## Problemas e limites

O ambiente VS Code Snap induzia conflitos GLIBCXX/pthread por módulos GTK/GIO.
O launcher limpa essas variáveis por processo e usa lib/ mais libs do Ubuntu.
KFM original emite aviso sobre parâmetros x/y de PosFreeze; a adaptação remove
esses parâmetros ignorados e os personagens iniciam sem esse aviso.
Um primeiro teste de teclado expirou após entradas simétricas; a captura mostrou
dano dos dois lados, mas não houve log final. Repetição usa vida assimétrica.
Sprites genéricos não acompanham com precisão todas as caixas AIR herdadas;
arte por frame e ajuste de hitboxes são o próximo incremento.
Sem bloqueio de inicialização no hardware testado. Mecânicas DBZ e estética MK
continuam pendentes e não fazem parte deste resultado.
