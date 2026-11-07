# skills-video

Skills de edição de vídeo para o Claude Code, criadas sob medida.

| Skill | O que faz |
|---|---|
| `color-grading` | Color grading com ffmpeg: 6 looks prontos, correções, LUTs .cube, HDR para SDR, antes/depois |
| `font-pairing` | Combinações de fontes grátis (Google Fonts) para vídeo, incluindo o estilo Old Money |
| `transicoes` | Junta clipes com ~55 transições (xfade), crossfade de áudio e ajuste de resolução/fps |

`preferencias.md` são as preferências gerais (caveman lite, ffmpeg silencioso, vídeo final em qualidade máxima).

O setup script do ambiente na nuvem copia `skills/` para `~/.claude/skills/` e `preferencias.md` para `~/.claude/CLAUDE.md` no início de cada sessão.
Para usar no seu computador: copie as pastas de `skills/` para `~/.claude/skills/`.
