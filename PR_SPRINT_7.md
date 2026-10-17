# Sprint 7: novas caminhadas candidatas; aceite artístico bloqueado

Base: `feat/sprint-6-gameplay-polish` → `feat/sprint-7-animation-quality`.
Abrir como **draft**, sem merge automático.

As caminhadas da Sprint 6 mantinham praticamente a mesma abertura de pernas.
Este change integra oito desenhos novos, quatro para Goku e quatro para
Vegeta, com contatos largos e passagens estreitas, nas ações AIR 20/21.
Fontes RGBA, três iterações por personagem, extração, manifestos e SFFs estão
no repositório. Nenhum estado, comando, Ki, projétil, caixa ou tempo AIR mudou.

**Não aprovar como Sprint artisticamente implementada.** As fontes são
candidatas: ainda faltam trajetória de apoio sem deslizamento, breakdowns,
confirmação da alternância anatômica e model sheets completos. A etapa de
combate não avançou porque o pedido exige validar ambas as caminhadas antes.
Há especificação e integração pronta para receber arte corrigida.

Comparações antes/depois, GIFs, fontes rejeitadas e capturas reais estão em
`evidence/sprint7/`. A revisão detalhada está em `docs/SPRINT_7_VISUAL_REVIEW.md`;
direção/model sheets pendentes em `docs/SPRINT_7_ART_DIRECTION.md`;
proveniência e prompts em `docs/ART_PROVENANCE.md` e
`assets-source/sprites/sprint7-prompts.md`.

Validação: validate normal/`-O`, 31 unittests e suíte gráfica herdada completa
PASS. Quatro poses observadas no motor nas ações 20/21, ambos os facings de
ambos os personagens. Vídeos reais de 32,959 s e 33,034 s; capturas dedicadas
de caminhada de 14,167 s e 14,134 s em 60 fps. Reconstrução final com hashes
idênticos em 742 arquivos. Resultados e limites em `evidence/sprint7/README.md`
e `docs/TESTING.md`. Nenhuma sessão humana de jogo foi declarada concluída.
