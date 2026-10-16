# Dragon Ball × Mortal Kombat Arcade — protótipo

Jogo de luta local executável no Ubuntu, usando **IKEMEN GO v1.0.0**.
Goku e Vegeta possuem sprites geométricos originais provisórios e combate derivado
do Kung Fu Man (Elecbyte). A Sprint 2 acrescenta Ki independente, Kamehameha e Galick Gun, com arte
original provisória e um primeiro ajuste arcade. Aceite humano pendente.

## Executar

```bash
cd /home/manomax/Documents/code/personal/games/DBZ-MK
./scripts/play.sh
```

A luta começa diretamente com dois jogadores humanos, melhor de três rounds,
99 segundos por round. Esc sai. Para o menu e seleção: `./scripts/play.sh --menu`.
Não é preciso instalar Go, Blender ou Python packages para jogar.
Requer Linux x86_64, glibc 2.35+, desktop gráfico e OpenGL; bibliotecas de mídia
acompanham o pacote. Áudio usa o dispositivo configurado no sistema.
Se áudio impedir inicialização, teste `./scripts/play.sh -nosound`.

| Ação | Goku / P1 | Vegeta / P2 |
|---|---|---|
| Mover, pular, agachar | Setas | J/L, I, K |
| Soco fraco / forte | A / S | R / T |
| Chute fraco / forte | Z / X | F / G |
| Defesa | Segurar direção contrária ao adversário | Igual |
| Carregar Ki (segurar os dois chutes) | Z + X | F + G |
| Kamehameha / Galick Gun (virado para a direita) | ↓, ↘, → + S | K, K+L, L+T |
| Start | Enter | Shift direito |

Há hitboxes, dano, hitstun, ataques em pé/agachado/no ar, defesa,
barras de vida, cronômetro, rounds e vitória/derrota fornecidos pelo motor e KFM.
Ki começa em 0, vai até 3.000 e reseta a cada round; cada projétil custa 1.000.
A barra fina azul/roxa abaixo da vida indica Ki; a barra power herdada continua
sendo exclusiva do KFM. Inverta as direções quando estiver virado à esquerda.
Sprites são deliberadamente simples. Defesa ainda usa direção para trás.

## Desenvolvimento

```bash
python3 scripts/build_characters.py
python3 tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
# Teste dos especiais, requer X11 e injeta teclas:
python3 tests/sprint2_smoke.py
# Requer desktop X11 desbloqueado; envia teclas à janela Ikemen:
python3 tests/keyboard_smoke.py
```

Veja [arquitetura](docs/ARCHITECTURE.md), [controles](docs/CONTROLS.md),
[testes](docs/TESTING.md), [assets/licenças](docs/ASSETS.md) e [roadmap](docs/ROADMAP.md).

## Local de instalação

O projeto foi criado neste workspace autorizado, em vez de `~/Projetos/DBZ-MK`.
A pasta é portátil: mova-a e execute `scripts/play.sh`; o script resolve caminhos
relativos. Nenhuma dependência global foi instalada.
