# Sprint 5: Goku e Vegeta orgânicos com captura de gameplay real

Base: `feat/sprint-4-character-art` → head: `feat/sprint-5-complete-fighters`.

Vegeta não tinha sprites orgânicos e Goku voltava a silhuetas geométricas em
muitas ações. Ambos agora têm 637 bindings orgânicos, cobrindo as ações essenciais,
contextos KFM adicionais e sprites de corpo sem hurtboxes usados em recuperação,
derrota e agarrões. Os especiais continuam sendo projéteis reais do IKEMEN.

- Folhas de referência próprias geradas, extração reproduzível, normalização de
  piso, alpha parcial, posicionamento e compensação de offsets/flips por contexto.
- Verificações completas de RGBA, cobertura, desenhos distintos, drift de piso,
  escala de locomover e reconstrução idêntica. CI exige zero placeholders de corpo.
- Dois ajustes explícitos de hurtbox de cabeça no soco forte; hitboxes, durações,
  estados, Ki, áudio, controles e motor v1.0.0 preservados.
- Margem lateral do cenário de 15 para 40 para manter idle/guarda visíveis
  nos extremos; regressões repetidas após o ajuste.
- Script de screenshots nos dois sentidos e gravação da janela durante entradas
  reais, carga, Kamehameha, Galick Gun e defesa.

Validação estática: validate normal/-O, 26 unittests, auditoria completa e
reconstrução determinística aprovados. Regressões gráficas aprovadas: Goku espelhado, teclado nos dois lados, dois KOs
em 0–2 com/sem áudio, ordem dos lutadores invertida, Ki/especiais/guarda/reset e
gravação real. Captura completa: 338.140 KiB RSS / 56,30 s. Evidências e falhas
do harness corrigidas estão em TESTING.md. CI remoto ainda precisa de confirmação.

**Revisão artística/humana pendente; manter como draft e sem merge automático.**
As poses KFM adicionais reutilizam famílias de movimentos e precisam de revisão
de coreografia/contatos; há variação anatômica, passos limitados e contornos para
refinar. Não chamar de arte final. Ver SPRINT_5_VISUAL_REVIEW.md, auditoria JSON
e ART_PROVENANCE.md. Sem novos personagens ou transformações.
