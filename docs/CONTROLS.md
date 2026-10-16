# Controles

| Comando | P1 Goku | P2 Vegeta |
|---|---|---|
| Esquerda / direita | ← / → | J / L |
| Pular / agachar | ↑ / ↓ | I / K |
| Socos fraco / forte (x/y MUGEN) | A / S | R / T |
| Chutes fraco / forte (a/b MUGEN) | Z / X | F / G |
| Start | Enter | Shift direito |

Segure para trás para defender alto; baixo + trás defende baixo.
Ataques também funcionam agachado e no ar. Esc encerra a luta rápida.
O menu oferece Versus e configuração de controles. O launcher fixa P1 e P2
nas entradas 1 e 2, com IA desligada. No menu escolha Versus para dois humanos.

Os golpes adicionais e combos herdados de KFM estão descritos em
`engine/chars/goku/readme.txt`. O comando QCF+y foi substituído pelos especiais DBZ; veja COMMANDS.md.
Teclados podem limitar combinações simultâneas (ghosting); avaliar no hardware alvo.

Carregar Ki: segurar Z+X / F+G. Especial: baixo, diagonal para frente,
frente+soco forte (S / T). Inverta as direções conforme o lado. Custa 1.000 Ki.

Capturar a demonstração Sprint 5: `python3 scripts/capture_demo.py` (desktop X11
aberto, ffmpeg/xwininfo/libXtst). O script foca o jogo e injeta entradas reais;
evite usar outras aplicações durante a captura. Grava
`tests/sprint5-gameplay.mp4`, screenshots nos dois sentidos e telemetria.
Para repetir todas as regressões gráficas: `python3 tests/sprint5_graphics.py`.
