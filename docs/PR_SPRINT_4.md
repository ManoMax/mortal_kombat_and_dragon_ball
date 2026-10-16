# Sprint 4: Goku orgânico e pipeline RGBA independente das colisões

Base: `feat/sprint-3-visual-identity`. Head: `feat/sprint-4-character-art`.
Preparar como **draft**, sem merge automático; revisão artística/humana pendente.

O importador anterior rejeitava alpha parcial e exigia que a arte preenchesse
exatamente a união das colisões. Este incremento preserva RGBA em SFF 2.0.1
PNG32, deduplica imagens idênticas por links nativos e aplica validações próprias
para arte orgânica: integridade, origem, escala, recorte, bounds e interseção
com cada caixa. Placeholders mantêm a validação geométrica estrita.
Hurtboxes opcionais são aplicadas por contexto AIR sem alterar hitboxes/tempos.

Goku recebeu quatro desenhos de idle, caminhada, soco, preparação/disparo de
Kamehameha e dano. As folhas AI originais, prompts, extração, âncoras dos pés e
hashes estão no repositório. O idle é reconhecível em uma luta real. Vegeta usa
o mesmo contrato/extrator, com arte orgânica pendente. Ki, projéteis, controle,
motor e recursos/licenças KFM foram preservados.

Validação: ver resultados finais em `docs/TESTING.md`, captura de Goku nos dois
facings em `tests/sprint4-facings.png`, telemetria de sprites e Ki em `tests/`.
CI reconstrói fontes e artefatos; execução remota ainda precisa ser confirmada.

Limites: arte candidata AI, sem licença oficial de Dragon Ball registrada;
proporções, contornos, contatos e hurtboxes precisam de revisão humana.
Demais ações/carga de Ki/Vegeta continuam provisórias. Não considerar a Sprint
integralmente concluída e não afirmar testes manuais executados.
