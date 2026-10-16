# Sprint 2: Ki independente e combate DBZ inicial

Base: `feat/sprint-1-stabilization` → head: `feat/sprint-2-dbz-combat`.
Abrir como draft; aceite final de jogabilidade depende de sessão humana.

Goku e Vegeta podem segurar os dois chutes para carregar Ki até 3.000 e usar
baixo, diagonal, frente+soco forte para disparar Kamehameha/Galick Gun por
1.000 Ki. Tentativas sem energia não executam o especial. Os projéteis têm
dano, guarda, colisões e impacto próprios. O Ki reseta a cada round e usa
var(20), separado do power dos especiais KFM.

O pipeline gera poses e efeitos originais azul/roxo, aura e barra de Ki;
configuração em assets-source/combat.json. A caminhada fica mais rápida e
normais terrestres podem cancelar em contato no especial. O dispatch QCF_y
KFM foi substituído, mantendo seus estados e dependências. Binário, common
states, áudio, controles personalizados e colisões/tempos herdados preservados.

Validação: normal/-O, 10 unittests, reconstrução determinística dos 16 arquivos,
smoke X11 dos especiais com telemetria por frame, dois KOs/placar 0–2 com e
sem áudio e smoke de teclado com dano dos dois humanos. Evidências e limites
em docs/TESTING.md. O cenário anterior de 10 s registrou empate e foi
reprovado; com 30 s mantém as exigências de dois KOs e passou.

Pendente: sessão humana completa (2–0/2–1), facing invertido, colisão entre
especiais simultâneos, avaliação de combos/ritmo, áudio e arte final. Nenhum
teste humano foi declarado aprovado. Não fazer merge automático.
