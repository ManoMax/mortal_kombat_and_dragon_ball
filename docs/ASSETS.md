# Origem e licenças

- Motor e scripts: IKEMEN GO v1.0.0, MIT; avisos em engine/LICENSES.txt.
- Download: https://github.com/ikemen-engine/Ikemen-GO/releases/tag/v1.0.0
- Arquivo Linux: Ikemen_GO-v1.0.0-linux.zip.
- SHA256 verificado contra SHA256SUMS.txt oficial:
  cc533c1a2ab84d63cbf9126d9dcb3f2dcc1a41c6206f2da419b0c91084f193e4.
- Interface, fontes, palco e sons: pacote oficial, licenças individuais em
  engine/LICENSES.txt. Inclui CC BY 3.0 e recursos não comerciais Elecbyte.
- Combate, comandos, animações e sons de Goku/Vegeta: adaptação de Kung Fu Man,
  (c) 2009 Elecbyte, Creative Commons Noncommercial conforme readme incluído.
  O protótipo completo não deve ser tratado como integralmente MIT/comercial.
- Sprites: desenhos geométricos originais gerados por scripts/build_characters.py,
  sem extração de jogos. Código novo do projeto disponibilizado sob MIT;
  isto não relicencia as dependências nem concede direitos sobre marcas/personagens.
- FFmpeg dinâmico: LGPL v2.1, conforme avisos do pacote. Código correspondente:
  https://github.com/ikemen-engine/Ikemen-GO/releases/download/v1.0.0/src_ffmpeg.tar.gz

Nenhum arquivo de Mortal Kombat ou Budokai Tenkaichi 3 foi importado.

## Substituição futura da arte

Criar/licenciar modelo, registrar autor/licença, importar no Blender, usar câmera
ortográfica lateral e iluminação fixa, animar idle/walk/jump/crouch/ataques/
block/hit/fall/win. Renderizar PNG transparente com origem nos pés e escala
compatível com hurtboxes. Converter para SFF, atualizar AIR e ajustar hitboxes
por frame. Validar ambos os lados e golpes no chão/no ar. Blender e pipeline
PNG→SFF não foram instalados/implementados neste incremento.

## Sprint 2

Os efeitos azul/roxo, aura, impacto, medidor e poses de carga/disparo são
originais procedurais em `scripts/dbz_combat.py`. Nenhuma imagem comercial de
Dragon Ball/Mortal Kombat foi importada. O gerador integra tudo ao SFF v1 de
forma reproduzível, preservando os avisos KFM e sua licença não comercial.

## Sprint 3

Obsidian Rift é um cenário procedural original criado por scripts/build_arena.py
(MIT), sem arquivos de jogos comerciais. Os PNGs idle-000 dos personagens são
exportações originais do gerador do projeto, com licença MIT sobre o desenho,
sem conceder direitos sobre os personagens/marcas. São exemplos de importação
com transparência, **não arte final**. Goku mantém laranja/azul e Vegeta azul/
branco; efeitos Kamehameha/Galick Gun continuam azul/roxo.

O motivo base em assets-source/fight-base.def é cópia do fight.def distribuído;
créditos Ohmga Shironeko e licenças em engine/LICENSES.txt continuam aplicáveis.
A personalização progressiva não torna as fontes/sons/sprites herdados originais.

Pipeline PNG→PCX→SFF implementado com Pillow fixado em requirements-assets.txt;
contrato e limitações em assets-source/sprites/README.md. Blender não utilizado.
Ainda exige produção artística: idle, caminhada, agachamento, salto, quatro
normais, defesa, dano, queda, carga, disparos e vitória de ambos. A cobertura
funcional AIR existente não equivale a animações finais desenhadas. Produzir
primeiro idle/walk/ataques, revisar colisões e facing no motor e só então
expandir a sequência. Não há transformações Super Saiyajin nesta entrega.

## Sprint 4

Goku recebeu cinco folhas AI de fan art candidatas, geradas nesta sessão,
sem importação de sprites comerciais. O SFF dos dois personagens agora é
2.0.1 PNG32 e preserva alpha parcial. As referências, prompts, hashes e limites
de licença estão em [ART_PROVENANCE.md](ART_PROVENANCE.md). Não existe licença
oficial de Dragon Ball registrada; não declarar autorização comercial. Avisos
KFM/motor permanecem aplicáveis. Arte restante e Vegeta aguardam produção.
