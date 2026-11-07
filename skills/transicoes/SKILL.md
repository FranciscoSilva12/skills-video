---
name: transicoes
description: >
  Transições entre clipes de vídeo com ffmpeg (xfade, ~55 efeitos: fade, dissolve, slide, wipe, zoom, flash branco, blur, pixelate...)
  com crossfade de áudio e ajuste automático de resolução/fps. Use quando pedirem transição, juntar clipes com efeito, fade entre cenas.
---
# Transições (ffmpeg xfade)
Script: `python3 -I ~/.claude/skills/transicoes/transicao.py SAIDA.mp4 clip1 [EFEITO[:SEG]] clip2 [EFEITO[:SEG]] clip3 ... [--previa] [--res 1080x1920] [--fps 30]`
- Entre clipes: nome do efeito com duração opcional (`fade:0.8`), ou `corte` (corte seco). Sem nada = `fade:0.5`.
- Resolução/fps vêm do 1º clipe (ou `--res`/`--fps`); clipes diferentes são ajustados com barras pretas. Clipe sem áudio recebe silêncio.
- `--previa`: meia resolução, rápido. Sem ele: qualidade máxima (`-preset slow -crf 18`). Testado (vídeos 16:9, 9:16, 25/30 fps).
## Fluxo
1. Sugerir efeitos conforme o clima; mostrar prévia (`--previa`) ou frames no meio da transição; ajustar; render final sem `--previa`.
2. Duração: 0,3-0,5 s (dinâmico, Reels) · 0,8-1,2 s (calmo, cinematográfico). Máx. metade do clipe mais curto (o script limita).
## Efeitos por clima
| Clima | Efeitos |
|---|---|
| Clássico, discreto | `fade`, `dissolve`, `fadeblack` (passagem de tempo), `fadegrays` |
| Energia, Reels | `zoomin` (amplia o centro do clipe que sai), `fadewhite` (flash), `hblur`, `slideleft`, `smoothleft` |
| Elegante, Old Money | `fade` 1 s, `fadeblack`, `circleopen`, `smoothup` |
| Moderno, tech | `wipeleft`, `coverleft`, `revealleft`, `squeezeh`, `pixelize`, `hlslice` |
| Divertido | `radial`, `circlecrop`, `diagtl`, `hlwind`, `vertopen` |
Direções: trocar `left` por `right/up/down` (wipe, slide, smooth, cover, reveal); `diagtl/tr/bl/br`; `wipetl/tr/bl/br`.
Todos: fade wipeleft/right/up/down slideleft/right/up/down circlecrop rectcrop distance fadeblack fadewhite radial smoothleft/right/up/down
circleopen circleclose vertopen vertclose horzopen horzclose dissolve pixelize diagtl/tr/bl/br hlslice hrslice vuslice vdslice hblur fadegrays
wipetl/tr/bl/br squeezeh squeezev zoomin fadefast fadeslow hlwind hrwind vuwind vdwind coverleft/right/up/down revealleft/right/up/down
## Regras
- Usar no máx. 1-2 tipos de transição por vídeo; corte seco é a melhor transição na maioria das vezes.
- Transição no ritmo da música: alinhar o início ao beat (ajustar duração dos clipes antes).
- Remotion: usar `@remotion/transitions` (fade, slide, wipe, flip, clockWipe) dentro do projeto.
