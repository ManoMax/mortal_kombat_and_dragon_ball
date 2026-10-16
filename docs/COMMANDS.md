# Comandos — Sprint 2

Segurar **a+b** (os dois chutes: P1 Z+X, P2 F+G) carrega Ki no chão.
Soltar qualquer chute encerra a carga. Receber golpe interrompe o estado e
remove a aura; manter as teclas permite retomar apenas ao recuperar controle.
Durante carga não há defesa, movimento, invulnerabilidade ou cancelamento.

**D, DF, F+y** executa Kamehameha (Goku) ou Galick Gun (Vegeta). Direções são
relativas ao facing: P1 inicial ↓, ↓+→, →+S; P2 inicial K, K+J, J+T.
Custo 1.000 Ki; exige chão e um projétil próprio ausente. A tentativa sem Ki
não dispara projétil e pode resultar num ataque normal. Ki é var(20), separado
de power; os especiais/supers KFM nunca leem ou escrevem essa variável.

| Família herdada | Decisão após auditoria |
| --- | --- |
| Movimento/guarda, FF/BB, recuperação x+y, agarrão, provocação | Mantidos com seus destinos originais. |
| x/y/a/b em pé, agachado e no ar | Geometria e tempos AIR preservados. Caminhada passa de 2,4/-2,2 para 2,8/-2,5. |
| QCF_y → 1010 | Dispatch removido: esse comando pertence ao especial DBZ. Estado 1010 e suas dependências permanecem. |
| QCF_x/xy, upper_x/y/xy, QCB_x/y/xy, FF_a/b/ab, QCF_a/b/ab | Mantidos; versões EX consomem apenas power KFM. |
| TripleKFPalm/SmashKFUpper → 3000/3050 | Mantidos como legado, custam power KFM e não Ki. O dispatch DBZ vem antes, evitando roubar QCF_y. |
| Parry frente+x → 1300/1320/1340 | Mantido; guarda principal continua trás (baixo+trás para baixo). |
| c/z/down_a/down_b e recovery | Definições e remapeamento preservados; nenhum estado comum removido. |

O especial cancela ataques terrestres 200–429 em contato (acerto ou defesa),
mas não sweep, golpes aéreos ou outro especial. Um projétil por personagem;
prioridade de projétil 1, HitDef 4, um hit e até 90 ticks de viagem. Projéteis
possuem Clsn1 e Clsn2 para atingir o adversário e colidir entre si.

| Parâmetro (ticks a 60 Hz) | Goku | Vegeta |
| --- | --- | --- |
| Startup / recovery após disparo | 20 / 24 | 22 / 26 |
| Dano nominal / chip | 150 / 0 | 160 / 0 |
| Velocidade horizontal | 7 | 6 |
| Hitstun / blockstun | 24 / 14 | 24 / 14 |
| Knockback no chão / guarda | -6 / -3 | -6 / -3 |

Dano final segue defesa/escala do motor. Guarda MA permite defesa alta, baixa
e aérea; não é golpe unblockable. Não há rastreamento ou teleporte. A inspiração
MK está no avanço mais rápido, disparo previsível e recuperação punível; alcance,
startup/active/recovery dos normais e cancelamentos KFM foram revisados e
preservados para a primeira solução incremental. Balanceamento fino depende
de sessão humana e não é considerado validado pelo teste automatizado.
