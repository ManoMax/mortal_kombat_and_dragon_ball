# Sprint 7 — novas caminhadas candidatas, aceite artístico bloqueado

Base: `feat/sprint-6-gameplay-polish`, commit `ab9a28b`.
Branch: `feat/sprint-7-animation-quality`. Data: 17/10/2026.

## Inspeção e decisão de escopo

Lidos AGENTS.md, ROADMAP.md, TESTING.md, ART_PROVENANCE.md e revisão da Sprint 6;
inspecionados fontes de caminhada, planos, manifestos, comparações AIR e frame
do vídeo real anterior. A caminhada antiga de Goku repetia a abertura das
pernas; Vegeta mantinha o mesmo apoio dianteiro. Passagens pouco distinguíveis,
franja das solas, identidade variável entre famílias e reutilização genérica
de golpes/defesa/queda continuam registrados na revisão anterior.

Foi usada produção artística real por `image_gen`, com três iterações para
cada personagem. V1: passagem de marcha com joelhos muito altos e contatos
parecidos. V2: Goku ainda com joelhos altos, Vegeta com bota avançando como
chute. V3: passagens mais estreitas e baixas, braço próximo avançando na segunda
metade. As fontes rejeitadas permanecem rastreáveis.

## Desenhos integrados

| Personagem | Fonte nova | Desenhos | Uso efetivo |
| --- | --- | --- | --- |
| Goku | `reference/sprint7/walk-v3-generated.png` | 4, contato/passagem/contato oposto/passagem oposta candidatos | AIR 20 e 21, sprites 30000,20–51 |
| Vegeta | `reference/sprint7/walk-v3-generated.png` | 4, mesmas fases candidatas | AIR 20 e 21, sprites 30000,20–51 |

São oito desenhos fontes, não 64 desenhos: cada pose atende quatro elementos
de 3 ticks; a ação traseira usa a ordem inversa. Cada ciclo permanece em 48
ticks. A família nova é `walk_sprint7`. A família anterior continua atendendo
os demais contextos; não propagar a mudança para corrida/salto/agarrões.

A extração fixa uma escala comum por personagem, âncoras próximas ao quadril,
retângulos completos e componentes explícitos. A normalização usa o piso do
pipeline existente, sem offsets novos no AIR e sem modificar SFF à mão.
As comparações mostram diferença perceptível das silhuetas da Sprint 6.

## Gate artístico: bloqueado

- As passagens são diferentes dos contatos, mas ainda é necessário confirmar
  a troca anatômica dos membros próximos/distantes nos dois contatos.
- O corpo permanece retido por 12 ticks por desenho enquanto o jogador anda.
  A sola pode deslizar nesse intervalo. Faltam breakdowns que acompanhem a
  translação real; a linha de alpha no chão não prova pé plantado.
- Oscilação do quadril, transferência de peso e oclusão das coxas ainda precisam
  de correção por animador. Vegeta muda a rotação do tronco com intensidade.
- Solas inclinadas e franjas antialias precisam de limpeza. O modelo de rosto,
  cabelo, mãos, luz e contorno ainda varia entre famílias antigas e novas.
- O model sheet completo com vistas e detalhes ainda não foi produzido/aprovado.
  A direção e o contrato de entrega estão em `SPRINT_7_ART_DIRECTION.md`.

Por esse gate, **não se avançou aos desenhos de socos, chutes, defesa, salto,
aterrissagem, dano, queda, recuperação, Kamehameha e Galick Gun**. Essas famílias
continuam com a Sprint 6. Não declarar a Sprint artisticamente implementada.
Isso não é ausência de ferramenta: a ferramenta foi utilizada; falta arte
com qualidade suficiente para passar o gate solicitado.

## Preservação e evidências

`evidence/sprint7/baseline/` preserva os oito PNGs normalizados anteriores e
hashes de AIR/CNS/CMD. `sprint7_evidence.py` rejeita alteração desses contratos.
O diff dos manifestos foi conferido: somente 32 bindings por personagem
mudaram; os outros 605 permanecem idênticos. Ki, projéteis, comandos, HitDefs,
caixas de colisão e comportamento do combate foram preservados.

Comparações PNG e GIFs em `evidence/sprint7/assets/` são prévias de fontes ou
coordenadas AIR, não gameplay. Capturas do motor, telemetria e resultados são
separados em `runtime/`. Testes automatizados não são sessão humana de jogo.
As capturas dedicadas confirmaram as quatro poses de cada ação nos dois
facings de ambos os personagens. Foram inspecionados os frames amostrados;
eles demonstram passagens diferentes no motor, mas não aprovam continuidade.
Os resultados finais e instruções de reprodução ficam no README da evidência
e em TESTING.md. Sem merge automático.
