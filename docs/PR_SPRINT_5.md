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

## Publicação bloqueada por acesso externo

Implementação local em `5978cd9`, correção de bordas/evidências finais em
`8237f51`. Branch `feat/sprint-5-complete-fighters`; worktree limpo após commits.

Push no sandbox falhou por DNS. A repetição fora dele alcançou o GitHub, mas
falhou por ausência de credencial HTTPS (`could not read Username`). A alternativa
pelo conector GitHub também foi tentada e recusou criação de blob com HTTP 403
`Resource not accessible by integration`. O plugin está instalado/ativado e
consegue ler o repositório, mas essa operação de escrita foi negada. O agente SSH
não tem identidades carregadas e não há GH_TOKEN/GITHUB_TOKEN configurado.
Nenhuma chave ou token foi exibido ou persistido pelo agente.

**Branch remota Sprint 5 e PR não foram criados.** O acesso de escrita precisa
ser corrigido externamente; não confundir a descrição preparada com um PR real.
Após disponibilizar credencial adequada, executar:

```sh
git push -u origin feat/sprint-5-complete-fighters
```

Criar PR draft com base `feat/sprint-4-character-art` e head
`feat/sprint-5-complete-fighters`, usando a descrição acima. Confirmar CI remoto
após a publicação; nenhum workflow remoto foi declarado aprovado nesta sessão.
Sem merge automático; aceite artístico/humano continua pendente.
