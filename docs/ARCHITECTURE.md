# Arquitetura

`engine/` contém a distribuição Linux oficial completa, binário, bibliotecas,
Lua/ZSS, common states, interface, fontes e cenário de treinamento.
`engine/chars/goku` e `vegeta` contêm definições, comandos, constantes,
estados, animações AIR e sprites SFF v1. Os estados são derivados do KFM;
common states do motor resolvem caminhada, pulo, defesa e reação a golpes.
O motor executa colisões, hitstun, cronômetro, rounds e condições de vitória.

`scripts/build_characters.py` gera 242 imagens indexadas PCX por personagem,
empacotadas em SFF, usando apenas a biblioteca padrão Python. Os desenhos
são originais; AIR, comandos, som e estados vêm de KFM. O gerador preserva
nomes desses arquivos para facilitar comparação com upstream. Remove os
parâmetros x/y ignorados de PosFreeze que causavam warning no KFM original.
Cada personagem tem sua própria pasta para permitir diferenciação futura.

`scripts/play.sh` resolve cwd, bibliotecas locais e entradas dos jogadores.
Remove variáveis GTK/GIO herdadas do Snap apenas no processo do jogo.
`engine/save/config.ini` contém controles e regras; demais arquivos save são
estado de execução ignorado pelo Git. O menu utiliza data/select.def.

A estrutura assets-source está reservada para arte e áudio futuros; o código
fonte da arte provisória está no gerador. Não há dependência de servidor/browser.

## Camada de combate Sprint 2

`assets-source/combat.json` configura Ki inicial (0–3.000), carga por tick,
dano, velocidade, startup e recovery por personagem. Reconstruir com
`python3 scripts/build_characters.py`. O máximo é 3.000 e o custo é 1.000.
O gerador valida limites e compõe `scripts/dbz_combat.py` com o KFM preservado.
Não editar os CMD/CNS/AIR/SFF gerados. Não há alteração no executável, common
states, controle personalizado, áudio ou arquivos KFM de origem.

Ki usa var(20), não usada pelo KFM (que reserva vars 1/2). IntPersistIndex=60
reseta as variáveis entre rounds; o statedef -2 aplica o Ki inicial durante a
introdução de cada round, independentemente do power herdado. Não há
persistência de Ki entre rounds, partidas ou processos. Normais, dano recebido
e supers KFM não geram/consomem Ki. A barra própria é um par de Explods de tela
7200/7201; ModifyExplod acompanha var(20)/3000, inclusive durante hitpause.

Estados próprios 7000 (carga interrompível) e 7100 (preparo/disparo/recovery)
compartilham infraestrutura e parâmetros individuais. O Projectile nativo usa
animações 7110 (viagem) e 7120 (impacto/cancelamento), Clsn1/2, guarda MA e
reações comuns. O custo é pago uma vez na entrada e não é devolvido se o
preparo for interrompido. Aura 7020 é removida imediatamente ao sair da carga.

Quinze sprites adicionais por personagem são desenhos procedurais originais:
poses de carga/preparo/disparo, aura, projétil, impacto e medidor. Goku e Vegeta
usam paletas compartilhadas coerentes com SFF v1, azul/roxo nos índices 6–8;
a arte herdada mantém seus índices 0–5. Todas as 604 silhuetas herdadas,
colisões e tempos AIR continuam comparados ao KFM. Estados antigos permanecem
para helpers, cancelamentos e IA; apenas o dispatch conflitante QCF_y é retirado.

`tests/sprint2_smoke.py` usa uma cópia temporária do config com Common.Lua
apontando para `engine/external/mods/-dbz-probe.lua`. O prefixo '-' impede
carregamento automático no jogo normal. A coleta lê estados, Ki, vida,
projéteis e contato/guarda a cada frame; não injeta valores nas mecânicas.
O modo quick versus inicia antes da descoberta de módulos, por isso a coleta
é configurada em Common.Lua. Os controles personalizados não são alterados.
