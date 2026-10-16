# Sprint 5 — auditoria visual e limites

## Base auditada

Branch de origem: `feat/sprint-4-character-art`; implementação em
`feat/sprint-5-complete-fighters`. Inspecionados AGENTS.md, ROADMAP.md,
TESTING.md, ART_PROVENANCE.md, fontes RGBA, planos, manifestos e AIR.

Antes da implementação: validate PASS, 21 unittests PASS. O smoke Sprint 4
foi repetido no motor real com Goku × Goku. A captura confirma identidade,
chão e facing do idle, não todas as ações. A base tinha 55 bindings orgânicos
para Goku e nenhum para Vegeta. Os demais contextos eram silhuetas geométricas.

Problemas observados nas referências/capturas: cabelo e volumes musculares
variam entre folhas; mãos e contornos precisam de limpeza; o idle tem longas
retenções herdadas; caminhada de quatro desenhos tem cadência limitada.
A normalização do piso não prova ausência de deslizamento dos pés. Anatomia,
contato natural e qualidade das transições precisam de avaliação humana.

## Integração incremental

1. Primeiro idle/caminhada de Vegeta: mesma extração/SFF PNG32 da Sprint 4,
   captura `tests/sprint5-initial-facings.png` e telemetria correspondente.
2. Folhas separadas com desenhos distintos para normais, salto/agachamento,
   carga, defesa, dano, queda, vitória e especiais. Nada de imagem única para
   todas as ações. Kamehameha/Galick Gun preservam estados/projéteis reais.
3. Folhas irregulares usam componentes de alpha com sementes explícitas e
   retângulos permanentes no plano. Pixels do componente com alpha >=32 e sua
   borda de dois pixels são extraídos; o alpha original dessa região permanece.
   Isso remove resíduos desconectados; não reconstrói anatomia nem inventa frames.
4. Escala é comum por sequência. Origem 160,240; pés das fontes terrestres
   normalizados em y=240. Poses aéreas têm posicionamento explícito, separado
   de compensação inversa dos offsets/flips AIR, sem distorcer o desenho.
5. Duas hurtboxes de cabeça do soco forte foram reposicionadas: Goku contexto
   30000,162 e Vegeta 30000,160. Os overrides estão no plano e manifesto,
   comparados pela regressão. Hitboxes, durações, estados, Ki e controles são
   preservados. A alteração pode afetar alcance defensivo e exige revisão humana.

## Pendências que impedem chamar de arte final

- Revisar uniformidade de cabelo, rosto, luvas, mãos, pernas, iluminação e espessura
  de contorno entre todas as folhas, especialmente recovery e vitória.
- Refinar os ciclos de caminhada; vários desenhos diferem pouco e não produzem
  uma alternância de passos tão boa quanto uma animação desenhada por animador.
- Conferir no motor a trajetória dos pés, continuidade dos centros de massa,
  aterrissagem, recuperação da queda e contatos nos dois sentidos, com debug.
- Os deslocamentos das poses aéreas aproximam o contrato KFM. A interseção das
  caixas não certifica anatomia, leitura do golpe ou balanceamento.
- O inventário `sprint5-animation-audit.json` verifica também todos os contextos
  herdados. Movimentos KFM adicionais reutilizam sequências orgânicas por família
  (palma, uppercut, parry, giro, agarrão), com posicionamento explícito por contexto.
  Essa cobertura técnica não equivale a coreografia final de cada movimento.
  Os offsets adicionais foram escolhidos por compatibilidade com as caixas;
  precisam de revisão visual de contatos, trajetórias e deslizamento dos pés.
- Retratos/ícones e parte da apresentação ainda são provisórios.
- Sessão com duas pessoas, áudio, partida equilibrada 2–1 e aceite artístico
  humano permanecem pendentes. Testes automatizados não contam como sessão humana.

Não foram adicionados personagens, transformações ou vídeos dentro do jogo.
A demonstração gravada é captura da janela do motor executando entradas reais.
O PR deve permanecer em revisão; não autoriza merge nem aceite artístico final.

## Cobertura técnica final

637 bindings por personagem: 604 contextos herdados com caixas, 28 sprites de
corpo herdados sem hurtboxes (derrota, recuperação e agarrão) e cinco poses DBZ
(duas de carga e três de especial). `audit_animations.py --complete` exige
cobertura orgânica de todas essas sequências. Sprites legados não utilizados,
retratos e props/efeitos de introdução não entram nessa afirmação.

As sequências KFM adicionais usam famílias de movimentos candidatas com offsets
explícitos, escolhidos para interceptar todas as caixas sem esticar os desenhos.
Isso evita o retorno a silhuetas geométricas, mas a coerência de agarrões,
parries, supers herdados e trajetórias ainda exige revisão por animador/jogador.
O verificador de SFF compara agora o SHA256 dos pixels RGBA completos, além do
alpha, para detectar também alterações de cor. O cache de compressão PNG do
encoder mantém os bytes gerados e evita recomprimir desenhos idênticos.
