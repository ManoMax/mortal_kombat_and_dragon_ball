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
