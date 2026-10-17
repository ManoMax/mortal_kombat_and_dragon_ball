# Sprint 6: cadência de idle, inspeção visual e regressões de combate

Base: `feat/sprint-5-complete-fighters`
Head: `feat/sprint-6-gameplay-polish`
Estado solicitado: **draft**, sem merge automático.

O idle de Goku e Vegeta retinha poses por 40/45 ticks. O plano de cadência
agora limita as retenções a 10–12 ticks, preservando desenhos, caixas, controles,
Ki e combate. A inspeção exporta sequências, comparações nos dois sentidos,
caixas opcionais, medidas dos pés e inventário completo de ações/famílias KFM
com contratos CNS/CMD. O smoke passa a verificar cada personagem nas duas
posições, incluindo especiais, defesa e interrupção, com gravação real.

Validação e resultados: `docs/TESTING.md`, `evidence/sprint6/README.md` e
`evidence/sprint6/runtime/result.json`. Arte ainda exige desenhos específicos
e avaliação humana: `docs/SPRINT_6_VISUAL_REVIEW.md`. Nenhuma aprovação de
qualidade artística final, sessão humana ou balanceamento completo é alegada.
Motor IKEMEN GO v1.0.0 preservado. Nenhum personagem, transformação ou especial
novo. Fontes/licenças preservadas, sem importação de arte comercial.

Publicação bloqueada: git push HTTPS sem credencial; conector GitHub responde
403 `Resource not accessible by integration` ao tentar escrever blob.
Nenhum PR foi criado; esta descrição está pronta para publicá-lo como draft
quando houver acesso de escrita. Não houve merge.
