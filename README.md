# Dragon Ball × Mortal Kombat Arcade — protótipo

Jogo de luta local executável no Ubuntu, usando **IKEMEN GO v1.0.0**.
Goku possui uma primeira sequência orgânica gerada para idle, caminhada, soco,
Kamehameha e dano. Vegeta e as demais ações de Goku mantêm arte provisória.
O combate deriva do Kung Fu Man (Elecbyte). A Sprint 2 acrescenta Ki independente, Kamehameha e Galick Gun, com arte
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
A arte é candidata de produção, com revisão humana de contatos, proporções e
transições ainda pendente. Defesa usa direção para trás.

## Desenvolvimento

```bash
python3 scripts/prepare_character_art.py goku
python3 scripts/build_characters.py
python3 tests/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
# Goku nos dois lados; requer X11 e injeta teclas:
python3 tests/sprint4_smoke.py
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

Sprint 4: [contrato gráfico](assets-source/sprites/README.md),
[proveniência e prompts](docs/ART_PROVENANCE.md). SFF v2 PNG32 preserva RGBA;
caixas AIR são independentes da silhueta. Sem aceite artístico final ou merge automático.
