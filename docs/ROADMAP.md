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
