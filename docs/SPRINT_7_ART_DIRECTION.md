# Sprint 7 — padrão de produção e gate da caminhada

Referências permanentes: `assets-source/sprites/{goku,vegeta}/idle/000.png`
(identidade já usada no motor) e folhas candidatas em `reference/sprint7/`.
As comparações ampliadas em `evidence/sprint7/assets/` são prévias, não renders
de um modelo 3D. O padrão abaixo é uma especificação; não certifica que todos
os desenhos atuais o atendem. Não importar sprites comerciais.

| Item | Goku | Vegeta |
| --- | --- | --- |
| Proporção | Adulto musculoso, tronco atlético, pernas com volume sob o tecido; altura normalizada de cabelo a sola próxima de 96 px | Adulto compacto, ombros largos e cintura estreita; mesma ordem de altura em pixels, cabelo vertical responde por parte maior da altura |
| Cabeça/rosto | Mandíbula firme, olhos pretos estreitos, sobrancelhas pretas; não aumentar cabeça entre frames | Mandíbula angulada, olhos estreitos, sobrancelhas inclinadas; entradas em V constantes |
| Cabelo | Preto, mechas laterais pontiagudas e franja; conservar raízes e distribuição das pontas | Preto, volume vertical pontiagudo, linha frontal em V; não trocar por cabelo de Goku |
| Roupa | Gi laranja, camiseta, faixa, munhequeiras e botas azul escuro; detalhe vermelho e cordões dourados nas botas | Macacão azul real, peitoral branco, abdômen e tiras douradas, luvas e botas brancas com biqueira dourada |
| Mãos/pés | Punhos fechados legíveis, cinco dedos quando abertos; bota com sola definida | Luvas com polegar separado, botas com biqueira e sola consistentes |
| Cor/luz | Três massas de valor por material, luz superior esquerda, sombra inferior direita | Mesmo princípio; branco sombreado com cinza frio, ouro sombreado com ocre |
| Contorno | Escuro contínuo, cerca de 1 px no tamanho de jogo; evitar franjas coloridas | Mesmo peso aparente, sem contorno branco nem halos |

Trabalhar em resolução alta com escala uniforme **por sequência**, nunca
esticar o corpo para preencher caixas. Origem de produção (160,240) no canvas
RGBA 320×320; AIR/SFF mantêm essa convenção. O extrator preserva os pixels e
compensa os contextos especificados; não desenha nem interpola membros.

## Model sheet a concluir

Antes de aprovar arte final: frente, perfil direito, três quartos direito,
costas, cabeça ampliada, mão aberta/fechada, bota lateral e paleta amostrada.
Os idles atuais são referências de identidade; as folhas de caminhada são
referências de movimento candidatas, **não um model sheet completo aprovado**.
Todas as novas famílias deverão seguir o mesmo model sheet quando aprovado.

## Ciclo necessário

1. Contato esquerdo: calcanhar esquerdo à frente, ponta direita atrás,
   transferência de peso e quadril baixo.
2. Passagem: perna esquerda suporta, direita passa flexionada, ponta elevada
   apenas o necessário para limpar o piso; quadril sobe discretamente.
3. Contato direito: troca real dos membros próximos/distantes e dos braços,
   sem inverter a direção do personagem.
4. Passagem oposta: direita suporta, esquerda passa; oclusão das coxas e
   direção dos braços precisam ser diferentes da passagem anterior.

Acrescentar breakdowns de descida/impulso entre esses quatro desenhos antes de
aprovar fluidez. Medir posição **do mesmo pé de apoio** no mundo por tick,
usando posição do jogador + coordenada da sola transformada pelo facing e
pela escala real do motor. A faixa inferior de alpha não identifica qual pé
está apoiado. Quatro hashes diferentes não aprovam um ciclo.

Retenções e velocidade atuais são preservadas para comparar somente o efeito
dos desenhos. Ainda haverá deslocamento durante retenções; aprovar trajetória
exige novos breakdowns compatíveis com a velocidade, não offsets globais.

## Integração de substituições

As folhas `walk_sprint7` de cada `production.json` têm retângulos, sementes,
escala, âncoras e bindings explícitos para os 32 contextos de AIR 20/21.
Substituir a fonte por desenhos aprovados, revisar esses parâmetros, executar
`prepare_character_art.py` para ambos e `build_characters.py`. Não editar SFF.
Os demais contextos da família antiga continuam com a fonte da Sprint 6.

Só após revisar os dois ciclos no motor avançar para: soco leve/forte e chute
com antecipação, extensão e recolhimento; defesa alta/baixa com apoio; salto,
compressão de aterrissagem; dano, queda e apoio para levantar; Kamehameha com
mãos na lateral do quadril e empurrão frontal, Galick Gun com preparo próprio
e descarga diagonal das mãos. Produzir poses por ação utilizada, sem expandir
cobertura por repetição. Ki, comandos e projéteis são contratos preservados.
