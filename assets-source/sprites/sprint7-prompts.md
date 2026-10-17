# Sprint 7 — prompts finais e cadeia de iteração

Ferramenta integrada `image_gen`, alpha solicitado em todas as seis gerações.
Sem CLI, API externa, sprite comercial ou referência oficial. Uma folha de
quatro corpos por chamada. Cada personagem tem `walk-generated.png`,
`walk-v2-generated.png`, `walk-v3-generated.png` preservados. Somente v3 entra
nos novos bindings; as duas anteriores documentam tentativas rejeitadas.

## Brief inicial comum

Use case: illustration-story. Original newly drawn arcade fighting-game WALK
CYCLE sprite sheet. Clean anime cel art, uniform dark thin outlines, 3 flat
tones, upper left light. EXACTLY FOUR separate full body sprites equally spaced
ONE horizontal row, transparent background, no text shadow effects ground.
Orthographic side/three-quarter facing RIGHT in EVERY drawing. Preserve head
size hairstyle proportions palette between all four. TRUE WALK poses, not idle
variants: 1 LEFT leg extended FORWARD heel contact, RIGHT leg behind toe
contact; 2 LEFT supporting leg under pelvis, RIGHT bent knee and visibly LIFTED
boot passing forward, narrow overlapping legs; 3 RIGHT leg extended forward
heel contact, LEFT behind toe contact (swap near/far leg shading and reciprocal
arm swing); 4 RIGHT supporting leg under pelvis, LEFT knee bent and visibly
lifted boot passing forward. Contact silhouettes WIDE, passage silhouettes
NARROW. Slight pelvic rise on passing frames; guarded bent arms counter rotate.
Same planted sole baseline. Whole hair boots inside cells with generous padding.
New original artwork, no copying commercial sprites.

Goku: adult muscular Goku, black pointed hair with lateral spikes, orange gi,
dark blue undershirt belt wristbands boots, red piping and gold boot cords.
Vegeta: adult compact muscular Vegeta, tall black upright pointed hair widow
peak, royal blue bodysuit, white chest armor with gold abdomen and shoulder
straps, white gloves and white boots with gold toes.

## Iteração v2

Ambos: editar a folha inicial, manter identidade/alpha/escala/cores. Trocar
perna próxima/distante no terceiro contato; braço próximo avança quando perna
próxima recua. Baixar a passagem para caminhar em vez de marcha de joelho alto.
A v2 de Goku alterou principalmente os braços; Vegeta passou a levantar a bota
para a frente como um chute. Ambas foram rejeitadas como produto final.

## Prompt exato v3 — Goku (referência: walk-v2-generated.png)

Correct this original Goku walk sheet. Biggest correction: sprites TWO and FOUR
must be ordinary LOW walking passage, NOT HIGH KNEE marching. Lower both raised
knees from waist level to almost the same height as supporting knee. Raised
boots must be beside supporting ankle, toes only 4 cm above floor. Knee flexion
mild, thighs almost vertical under pelvis. In FOURTH sprite swing the VISIBLE
NEAR ARM FORWARD (fist right in front of chest) and hidden far arm back, unlike
second. In FOURTH the near knee passes in FRONT OF the far supporting knee,
visibly occluding it. In SECOND the far knee passes BEHIND near supporting knee.
First and third contact poses and heads unchanged. Preserve clothing anatomy
identity thin outline colors and transparent canvas, four equally spaced whole
bodies in a single horizontal row. No words/effects/shadow. This is walk cycle,
not knee strikes.

## Prompt exato v3 — Vegeta (referência: walk-v2-generated.png)

Edit these four Vegeta sprite drawings. Preserve heads identity armor colors
line style scale transparency. First unchanged. In SECOND: supporting leg
straight beneath pelvis, other leg bent BEHIND supporting knee with raised heel
BEHIND toward LEFT, toes pointing down near ground; NOT extended forward like
a kick. In THIRD: VISIBLE NEAR ARM bent swinging FORWARD to RIGHT (fist in front
of chest), far arm back. Near leg extended BACK LEFT overlapping far leg, far
leg extends forward RIGHT. In FOURTH: visible NEAR ARM bent swinging FORWARD
RIGHT, far arm back; VISIBLE NEAR KNEE bent crossing IN FRONT OF the straight
far supporting knee; near boot lifted next to supporting ANKLE just 4cm above
floor, NOT high knee or forward kick. SECOND and FOURTH must be opposite passing
poses. Contact 1/3 wide silhouettes; passage 2/4 narrow overlapping legs.
Natural low walk. All four full bodies in one row, same baseline, no text floor
effects shadows.

Os briefs v1/v2 acima resumem as instruções; os prompts v3 são integrais.
As imagens preservadas são a fonte de build; geração não é determinística.
