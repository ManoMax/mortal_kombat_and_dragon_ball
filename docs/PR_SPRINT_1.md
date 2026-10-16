# Sprint 1: estabilizar geometria dos sprites e validar melhor de três

Base: `main`. Branch: `feat/sprint-1-stabilization`.
Abrir como **draft** até concluir as verificações manuais de TESTING.md.

## Problema e comportamento resultante

A geração por grupo reutilizava a mesma pose em frames com caixas AIR distintas,
causando divergências em agachamentos, saltos, ataques e quedas. O gerador agora
acrescenta 604 variantes por personagem, compensando offsets/flips e desenhando
a união das hurtboxes e o alcance das hitboxes. Preserva as 242 entradas antigas
para referências comuns/retratos. Os personagens resultam em 846 sprites e 655
frames AIR cada. A arte fica geométrica e provisória; a mudança prioriza a
correspondência de colisão e requer revisão visual no motor.

As caixas, tempos, estados, comandos, controles personalizados e recursos KFM
de origem permanecem preservados. SFF é reconstruído pelo script, com RLE PCX
por scanline para comprimir o canvas de 320×320. O executável IKEMEN GO v1.0.0
permanece idêntico ao de main; a validação passa a conferir seu SHA256 fixado.
Nenhuma mecânica DBZ foi introduzida.

## Verificações e evidências

- `python3 tests/validate.py` e `python3 -O tests/validate.py`: PASS. Decodificação
  PCX, cadeia SFF, referências AIR, comparação das caixas/tempos com a origem,
  cobertura integral da silhueta e hash do motor.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`: 6 testes PASS,
  incluindo rejeição de SFF/PCX corrompido, origem deslocada, resultados de
  partida inconsistentes e declarações de colisão incompletas.
- Reconstrução do gerador: SHA256 dos 16 arquivos dos personagens inalterados.
- `python3 tests/match_smoke.py`: PASS, dois KOs consecutivos, placar 0–2,
  encerramento com código 0 em 30,65 s; `tests/rounds-nosound.log`.
- `python3 tests/match_smoke.py --audio`: PASS, mesmo cenário, 32,17 s;
  `tests/rounds-audio.log`. `-nosound` silencia o volume, não necessariamente
  desativa o backend de áudio; a qualidade audível permanece sem avaliação.
- `python3 tests/keyboard_smoke.py`: PASS, ambos AILevel 0, vida final 711/811
  a partir de 900/1000; `tests/keyboard-match.log` e `tests/gameplay.png`.
- `git diff --check`: PASS. Workflow novo repete validação estática,
  reconstrução/diff e regressões; GitHub Actions ainda não executado.

Cada teste de partida cria um log temporário novo e exige saída 0 antes de
validar. O teste de rounds confere sequência, soma das vitórias, vencedor,
KOs/vida e encerramento na segunda vitória. Não reutiliza logs históricos como
aprovação. O teste de teclado também deixa de depender de asserts desativáveis
por `python -O` e captura o DISPLAY corrente.

## Investigação e decisões

`-rounds 2` configura duas vitórias, não dois rounds totais. Um primeiro cenário
com vida inicial assimétrica empatou após restauração no próximo round; o teste
rejeitou esse resultado. O cenário corrigido usa vida máxima 1 em P1 sem IA e
P2 IA 8, permitindo repetir KOs. A execução original de 55 s com áudio não foi
reproduzida, e a causa permanece inconclusiva. Nenhuma correção especulativa no
backend foi aplicada.

`docs/COMMANDS.md` registra comandos a manter e candidatos a remoção/substituição
futura. Nesta sprint nenhum controle é removido: especiais e supers KFM ainda
participam de cancelamentos/IA. ROADMAP.md distingue implementação, evidência
automatizada e aceite pendente; TESTING.md contém ambiente e reprodução.

## Limitações e aceite pendente

- Nenhum teste manual concluído. Confirmar todas as poses/caixas, ambos os
  sentidos, escalas, agarrões, guarda, hitstun e recuperação no motor.
- Dois KOs automatizados comprovam o cenário 2–0, sem comprovar partida humana
  equilibrada, 2–1, reset de todos os recursos, empates ou navegação nos menus.
- Avaliar áudio, latência e teclas simultâneas com duas pessoas.
- Silhuetas preenchidas são mais geométricas; arte final está fora desta sprint.
- Parser AIR é compartilhado entre gerador e validador; fixtures independentes
  de offsets/flips e controles negativos mitigam, sem eliminar, esse limite.

## Publicação pendente

Os commits estão locais na branch solicitada. O terminal não dispõe de
credencial HTTPS para push; a API GitHub conectada retornou HTTP 403
`Resource not accessible by integration` em `create_blob`. Nenhuma branch ou
Pull Request remoto foi criado por esta execução.

Em terminal autenticado, executar na raiz do repositório:

```bash
git push -u origin feat/sprint-1-stabilization
```

Depois abrir a comparação no GitHub e criar um draft PR para main usando o
conteúdo técnico acima:
https://github.com/ManoMax/mortal_kombat_and_dragon_ball/compare/main...feat/sprint-1-stabilization
