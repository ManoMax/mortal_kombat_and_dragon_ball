# Sprint 3: pipeline PNG e fundação visual arcade

Base: `feat/sprint-2-dbz-combat`. Head: `feat/sprint-3-visual-identity`.
Status: **rascunho — aceite artístico e humano pendente**.

O protótipo usava apenas silhuetas geométricas dependentes das caixas. Este
incremento permite importar PNGs RGBA por contexto AIR, normaliza escala/origem,
reserva transparência e empacota PCX/SFF v1 sem alterar o combate. Inclui um
PNG provisório integrado por personagem, iluminação de borda nos placeholders,
arena original Obsidian Rift e personalização progressiva do HUD.

Preserva IKEMEN GO v1.0.0, controles, KFM/licenças, tempos e caixas, Ki,
Kamehameha e Galick Gun. CI reconstrói personagens, arena e interface.

Limitação de aceite: sprites ainda geométricos e provisórios. O importador
rejeita alpha parcial e não permite ultrapassar a política de ocupação completa
das caixas herdada. Arte orgânica final exige produção artística e política
revisada com revisão humana por frame. Não afirmar identidade artística final,
FPS estável ou validação humana concluída. Sem Super Saiyajin e sem merge.

Validação e métricas da execução atual em docs/TESTING.md; captura automatizada
em tests/sprint2-effects.png e tests/gameplay.png. A medição /usr/bin/time mede
recursos do cenário completo, não tempos de frame da GPU.
