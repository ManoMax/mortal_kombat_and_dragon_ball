# Revisão dos comandos KFM — Sprint 1

Fonte: `engine/chars/kfm/kfm.cmd`, copiada pelo gerador para Goku/Vegeta.
Esta sprint preserva todos os comandos e os controles em `engine/save/config.ini`.
Nenhum comando abaixo implementa Ki ou outra mecânica DBZ.

| Comandos internos | Destino | Decisão e motivo |
| --- | --- | --- |
| `holdfwd`, `holdback`, `holdup`, `holddown` | Movimento/defesa do motor | Manter; necessários às posturas e guarda direcional. |
| `x`, `y`, `a`, `b` | 200/210/230/240, 400/410/430/440, 600/610/630/640 | Manter; ataques leves/fortes em pé, agachado e no ar. |
| `FF`, `BB` | 100/105 | Manter nesta sprint; corrida/recuo existentes. |
| `recovery` (`x+y`) | Recuperação do motor | Manter; contrato dos estados comuns. |
| `y` + frente/trás perto do adversário | 800 | Manter o agarrão; conferir alcance manualmente. |
| `start` (`s`) | 195 | Manter provocação existente. |
| `blocking` (frente+x ou x+frente) | 1300/1320/1340 | Manter provisoriamente; parry KFM, diferente da guarda para trás. Candidato a substituição em sprint de design de combate. |
| `QCF_x/y/xy` | 1000/1010/1020 | Manter provisoriamente; Palm KFM, versão rápida custa 330. Substituir por golpes originais apenas com especificação futura. |
| `upper_x/y/xy` | 1100/1110/1120 | Manter provisoriamente; Upper KFM, versão rápida custa 330. |
| `QCB_x/y/xy` | 1200/1210/1220 | Manter provisoriamente; defesa especial KFM, versão rápida custa 330. |
| `FF_a/b/ab` | 1050/1060/1070 | Manter provisoriamente; Knee KFM, versão rápida custa 330. |
| `QCF_a/b/ab` | 1400/1410/1420 | Manter provisoriamente; Kick KFM, versão rápida custa 330. |
| `TripleKFPalm`, `SmashKFUpper` | 3000/3050 | Candidatos a substituição futura; super KFM custa 1000. Não renomear como poderes DBZ. |
| `c`, `z`, `down_a`, `down_b` | Sem consumidores explícitos no CMD/CNS local | Candidatos a remoção das **definições** após auditoria dos estados comuns; manter teclas e remapeamento. Não confundir definição sem consumidor local com controle inútil. |

A ordem dos ChangeState permite especiais antes dos normais e cancelamentos
por contato. Remover somente uma definição pode deixar gatilhos inalcançáveis;
remover um estado pode quebrar cancelamentos, helpers e a IA. A estabilização
preserva esses caminhos. Balanceamento, parry, supers e simplificação ficam
para uma mudança com decisão de produto e testes próprios.
