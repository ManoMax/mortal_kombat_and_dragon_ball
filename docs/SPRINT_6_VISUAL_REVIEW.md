# Sprint 6 — revisão técnica e pendências de arte

Base local `feat/sprint-5-complete-fighters` em `c626c91`; branch
`feat/sprint-6-gameplay-polish`. Data: 17/10/2026. Goku e Vegeta apenas.
IKEMEN GO v1.0.0, controles, Ki, HitDefs e especiais preservados.

## Alteração visual implementada

O idle tinha retenções de 45 e 40 ticks no ciclo herdado. O plano explícito
`assets-source/animation-polish.json` passa os onze elementos para
12/10/10/12/10/10/10/12/10/10/12 ticks (118 ticks, anteriormente 151).
São os mesmos quatro desenhos e a mesma ordem de respiração; não há desenhos
novos, interpolação ou poses simuladas com offsets. A redução das pausas é
mensurável; naturalidade da respiração não foi aprovada por uma pessoa.
O teste dedicado compara todos os frames e exige que somente durações do idle
mudem. A validação continua exigindo os contratos de combate herdados.

## Evidência e limites de medição

`evidence/sprint6/assets/` contém comparações PNG e sequências GIF dos dois
facings para idle, caminhada frente/trás, salto/preparo, aterrissagem, normais,
queda/recuperação e especial. São **prévias dos assets em coordenadas AIR**,
não capturas do jogo. Linhas verdes: chão; eixo vertical: posição do jogador;
vermelho: Clsn1; ciano: Clsn2. GIFs aproximam as durações AIR positivas à resolução temporal do formato; uma duração
indefinida é exibida por 1 segundo para inspeção, não simula a saída do estado.

`inspection.json` inventaria as 124 ações AIR por personagem e os 61 estados
CNS locais (resumo em `kfm-state-inventory.csv`), seus sprites, família fonte,
caixas, medidas e contratos textuais CNS/CMD (HitDef, Projectile, ChangeState,
TargetBind/TargetState, TargetVelSet, HitOverride). As rotinas comuns do motor são referenciadas com hash e não são resolvidas
por esse inventário estático. Todos os movimentos continuam
usando estados KFM, exceto carga/especial DBZ. Ter sprite orgânico não remove a
dependência da coreografia KFM. Ações com famílias repetidas, como 800/810/820
(agarrão), 1000+ (movimentos herdados), 5000+ (dano/recuperação), precisam de
revisão específica; o inventário fornece a lista por ação, não apenas essenciais.

`feet.csv` mede a faixa dos últimos três pixels com alpha >=32. `bottom_y=0`
significa que essa faixa alcança a origem vertical. Isso difere do teste de
normalização que aceita qualquer alpha não zero até y=240: a franja antialias
pode tocar o piso enquanto a parte opaca fica acima. O centro dessa faixa não
identifica pé esquerdo/direito, nem prova apoio ou ausência de deslizamento.
`alpha_change_pixels` mede diferenças de alpha entre elementos consecutivos;
não mede anatomia, cores, suavidade perceptual ou movimento do pé apoiado.

Startup/recovery do relatório são **intervalos AIR com/sem Clsn1**, não frame
data resolvida do estado: triggers de HitDef, hitpause, cancelamento e saídas
antecipadas também determinam o combate. Consulte os contratos exportados.
Valores indefinidos (-1) estão sinalizados e não devem ser somados como duração.

## Problemas remanescentes e desenhos a produzir

| Prioridade / ações | Evidência | Trabalho necessário |
| --- | --- | --- |
| Alta: caminhada 20/21 | Comparações `*-20-frames.png`; quatro desenhos retidos por 12 ticks cada | Produzir contato esquerdo, passagem, contato direito e passagem com pés reconhecíveis, quadril coerente e trajetória de apoio. As poses atuais variam pouco; não certificar alternância real. |
| Alta: pés de Vegeta | `feet.csv`, 20/21: faixa opaca em -5 ou -2; Goku em -2 | Rever solas/âncoras e desenhar apoio coerente. Não deslocar todo o corpo para esconder variação sem avaliar o pé apoiado. |
| Alta: agarrões 800/810/820 | Inventário e TargetBind exportados | Desenhar mãos em contato, levantamento, rotação, soltura e vítima em posições compatíveis com binds; validar ambos os sentidos no motor. Ainda não testado dinamicamente nesta sprint. |
| Alta: salto/queda/recuperação | `*-40*`, `*-47*`, `*-5100*`, `*-5120*` e famílias no inventário | Novas passagens para decolagem, ápice, descida, compressão de aterrissagem e apoio para levantar. Reuso de famílias não garante trajetória corporal. |
| Alta: normais/ataques herdados | `*-200*`, `*-210*`, `*-230*`, `*-240*` e contratos | Revisar antecipação, punho/pé no alcance da Clsn1 e recuperação; produzir poses específicas para palma, giro e parry em vez de reusar uppercut/soco forte. |
| Média: identidade | Contact sheets e comparações de ambas as fontes | Limpar cabelo, rosto, mãos/luvas, volumes e espessura de contorno, usando um model sheet por personagem. Sem correção artística alegada nesta sprint. |
| Média: especiais 7100 | Comparação de corpo e vídeos runtime | Refinar antecipação e recuperação próprias de Kamehameha/Galick Gun; a família interna chamada `kamehameha` atende ambos. Funcionamento do projétil não aprova pose/efeito artístico. |
| Alta: bordas | Margem 40 já existente; comparações de poses largas | Conferir queda, agarrão e ataques extensos nos extremos em partida humana. Caixa local e preview não certificam câmera nem recorte na viewport; não ampliar margem global sem avaliar espaço de luta. |

## Revisão do combate

Normais continuam com hitstun/knockback/guarda herdados. Exemplo verificável:
soco leve 200 inicia Clsn1 após 3 ticks AIR; HitDef em AnimElem=3,
23 de dano, ground.hittime=11, ground.velocity=-4, guarda MA. O inventário
preserva as expressões dos demais ataques para revisão de balanceamento.

Kamehameha: startup de estado 20, recovery configurado 24, velocidade 7,
dano 150. Galick Gun: 22/26, velocidade 6, dano 160. Ambos pagam 1.000 Ki uma
vez, limite 3.000, um projétil por usuário, chip zero, hitstun terrestre 24,
blockstun 14, knockback -6, guarda -3. Projéteis têm limite de vida de 90 ticks.
Cancelamento DBZ segue terrestre, estados 200–429 com movecontact, ou ctrl;
não foi ampliado. Agarrão preserva prioridade 1/Miss, p1stateno=810,
p2stateno=820 e binds KFM. Defesa alta/baixa, parry, cancelamentos, agarrões e
balanceamento completo precisam de sessão humana; não foram declarados aprovados.

A sprint entrega polimento de cadência e inspeção técnica. O aceite artístico,
partida equilibrada 2–1, frame time/FPS, contatos de todos os normais, áudio
perceptual e sessão com duas pessoas continuam pendentes.

## Inspeção das capturas reais finais

O frame em `runtime/reversed-gameplay-frame.png` (8 s do vídeo) mostra Vegeta
à esquerda e Goku defendendo à direita, piso visível e medidores de Ki nas
cores correspondentes. O pé de Goku fica muito próximo da borda direita:
esta imagem não demonstra recorte nessa pose, mas reforça a necessidade de
verificar poses mais largas e agarrões nos extremos. Há um efeito de guarda
branco em losango e retratos ainda provisórios; não foram redesenhados.
A captura não comprova todos os contatos nem substitui assistir às sequências
e jogar. Esses aspectos permanecem explicitamente abertos para revisão humana.
