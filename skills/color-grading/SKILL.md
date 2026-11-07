---
name: color-grading
description: >
  Color grading e correção de cor de vídeo com ffmpeg - looks prontos (cinema teal & orange, quente, frio,
  vintage, P&B, desbotado), exposição, contraste, saturação, balanço de branco, LUT .cube, HDR para SDR
  e antes/depois. Use quando pedirem color grading, correção de cor, look, LUT ou vídeo mais quente/frio/cinematográfico.
---
# Color grading (ffmpeg)
## Fluxo
1. Analisar: `ffprobe -v error -select_streams v -show_entries stream=pix_fmt,color_transfer -of csv=p=0 IN`.
   Se transfer for `smpte2084` ou `arib-std-b67` é HDR: converter para SDR primeiro.
2. Antes/depois: aplicar o filtro num frame do meio e mostrar ao usuário (SendUserFile) antes de processar o vídeo todo. Ajustar até aprovar.
3. Render: `ffmpeg -hide_banner -loglevel error -stats -i IN -vf "FILTRO" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy OUT_grade.mp4`. Nunca sobrescrever o original.
4. Conferir frame do final (sempre qualidade máxima). Prévia rápida: `-preset veryfast -crf 23` + `scale=-2:540`. Grande/vertical: `scale=-2:720,` antes do split.
## Looks (testados)
| Look | Filtro |
|---|---|
| Cinema (teal & orange) | `colorbalance=rs=-0.06:gs=-0.02:bs=0.08:rh=0.08:gh=0.02:bh=-0.08,eq=contrast=1.08:saturation=1.1` |
| Quente | `colortemperature=temperature=4500:pl=1` |
| Frio | `colortemperature=temperature=9000:pl=1` |
| Vintage | `curves=preset=vintage,eq=saturation=0.85` |
| Preto e branco | `hue=s=0,eq=contrast=1.15` |
| Desbotado (faded) | `curves=all='0/0.08 1/0.92',eq=saturation=0.8` |
Intensidade parcial (ex. 50%): `split[a][b];[b]LOOK[g];[a][g]blend=all_mode=normal:all_opacity=0.5` (usar em -filter_complex).
## Correções
- Exposição: `exposure=exposure=0.3` (stops). Contraste/saturação/gama: `eq=contrast=1.1:saturation=1.2:gamma=1.05` (1 = igual)
- Vibrance (protege pele): `vibrance=intensity=0.2`. Branco: `colortemperature=temperature=K:pl=1` (6500 neutro; menor = mais quente)
- Sombras/médios/altas por cor: `colorbalance=rs=..:gm=..:bh=..` (-1 a 1, usar ±0.02-0.1)
- Curvas: `curves=preset=increase_contrast` (ou lighter, darker, strong_contrast). LUT .cube: `lut3d=file='x.cube':interp=tetrahedral` (aceita intensidade parcial)
- Ordem: correção (exposição, branco) primeiro, look depois.
## HDR para SDR
`zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p` (escuro? somar `exposure`)
## Antes/depois (frame)
```
T="x=20:y=20:fontsize=40:fontcolor=white:box=1:boxcolor=black@0.5"
ffmpeg -hide_banner -loglevel error -y -ss TEMPO -i IN -frames:v 1 -q:v 2 -filter_complex \
  "[0]split[a][b];[b]FILTRO[g];[a]drawtext=text=ANTES:$T[a2];[g]drawtext=text=DEPOIS:$T[g2];[a2][g2]hstack" antes_depois.jpg
```
Cuidados: pele: preferir vibrance a saturação. Pretos/brancos estourados: conferir `signalstats` (YMIN/YMAX). Exportar sempre yuv420p.
