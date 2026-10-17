# Roadmap

1. Fase 1: IKEMEN GO v1.0.0 instalado e verificado anteriormente. Motor preservado
   na Sprint 1; hash do executável e evidências em TESTING.md.
2. Fase 2: personagens provisórios com núcleo/áudio KFM e controles locais.
   Avaliação com duas pessoas permanece pendente.
3. **Sprint 1 — estabilização iniciada, aceite manual pendente:**
   - Implementado: sprites originais por contexto AIR, cobrindo hurtboxes e
     alcance das hitboxes sem alterar caixas, tempos, estados ou controles.
   - Automatizado: SFF/PCX, cobertura de colisão, regressões negativas e
     encerramento 0–2 por KO com/sem áudio. Evidências em TESTING.md.
   - Investigado: limite de 55 s não isolava áudio; cenário controlado completa
     com/sem áudio. Causa do timeout original não reproduzida/conclusiva.
   - Revisado: comandos KFM em COMMANDS.md; remoções/substituições propostas,
     sem alteração silenciosa dos controles.
   - Pendente: inspeção visual no motor em todas as posturas, defesa, agarrões,
     partida 2–1, empates, menus e sessão humana com áudio.
   - Limite: silhuetas de colisão são arte de protótipo, não animação final.
4. **Sprint 2 — implementada, testes automatizados aprovados e aceite manual pendente:**
   - Ki independente com carga, máximo 3.000, custo 1.000 e reset por round.
   - Kamehameha/Galick Gun com estados, sprites, projéteis e impacto próprios.
   - Caminhada mais rápida, cancelamento terrestre em contato e recovery punível.
   - Pipeline determinístico; testes de comandos, telemetria e regressões.
   - Pendente: sessão humana, ajuste fino do ritmo MK, arte final e transformações.
   - A Sprint 1 mantém seu aceite manual pendente; não houve merge automático.
5. Fase 4 parcial: interface/seleção do motor. Identidade MK, palco original,
   câmera fixa e apresentação próprias pendentes.
6. Fase 5 pendente: pipeline Blender e arte original/licenciada de maior qualidade.

7. **Sprint 3 — implementação mínima, aceite artístico pendente:**
   - Importador PNG RGBA reproduzível, escala/origem, SFF v1 e AIR preservado.
   - Um exemplo PNG integrado por personagem; demais poses provisórias com
     contorno iluminado. Arte geométrica não aceita como arte final.
   - Arena original Obsidian Rift integrada, parallax e piso delimitado.
   - Interface progressiva: cores por jogador, cronômetro e mensagem de vitória;
     Ki mantido. Fontes, rounds e início da luta ainda usam recursos distribuídos.
   - Falta produzir animações orgânicas e revisar visualmente todos os frames,
     ambos os facings, agarrões e limites. Sem transformações nesta sprint.

8. **Sprint 4 — arte orgânica inicial integrada; aceite humano pendente:**
   - SFF 2.0.1 PNG32, RGBA completo, extração e build determinísticos.
   - Goku: idle de quatro desenhos, caminhada, soco, Kamehameha e dano candidatos.
   - Arte separada das caixas; validações específicas para orgânicos preservam
     testes estritos dos placeholders e tempos/hitboxes herdados.
   - Vegeta preparado com o mesmo plano/manifesto/extrator, sem arte final.
   - Pendente: revisão humana das proporções, iluminação, contornos, contatos,
     facings, todas as ações restantes e licença oficial dos personagens.
   - Não declarar Sprint integralmente concluída; sem merge automático.

9. **Sprint 5 — cobertura orgânica das ações essenciais em revisão:**
   - Goku e Vegeta: ciclos próprios de locomover, atacar, saltar/agachar,
     defender, sofrer dano/cair, carregar, disparar e vencer.
   - Extração por componentes explícitos, offsets/flips compensados e auditoria
     de desenhos distintos, piso, escala e placeholders remanescentes.
   - Captura de gameplay real via X11; estados e especiais DBZ preservados.
   - Ações KFM adicionais reutilizam famílias orgânicas; coreografia e apresentação
     ainda são provisórias. Inventário completo no relatório; aceite humano pendente.
   - Sem novos personagens/transformações; PR para revisão, sem merge automático.

10. **Sprint 6 — polimento técnico e revisão visual:**
    - Cadência de idle sem retenções herdadas de 40/45 ticks.
    - Comparações, sequências GIF, caixas opcionais, relatório de faixa de pés,
      inventário AIR/famílias KFM e contratos de combate exportados.
    - Regressão ampliada com personagens invertidos entre P1/P2 e gravação real.
    - Pendências artísticas e desenhos necessários em SPRINT_6_VISUAL_REVIEW.md.
    - Aceite artístico/humano permanece pendente; sem novos golpes/personagens,
      transformações, alteração de motor ou merge automático.
