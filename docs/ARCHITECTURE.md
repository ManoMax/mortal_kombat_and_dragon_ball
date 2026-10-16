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
