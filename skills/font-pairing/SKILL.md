---
name: font-pairing
description: >
  Combinações de fontes (título + legenda) para vídeo, Reels, TikTok, YouTube e motion graphics, com fontes grátis do Google Fonts.
  Baixa, mostra prévia e aplica (ffmpeg, Remotion, moviepy). Use quando pedirem fonte, tipografia ou combinação de fontes.
---
# Combinações de fontes para vídeo
## Fluxo
1. Perguntar o clima (se não foi dito) e sugerir 2-3 pares. 2. Baixar (`baixar_fonte`), gerar prévia com título e legenda, mostrar (SendUserFile).
3. Aplicar: ffmpeg `drawtext=fontfile=...`, moviepy `TextClip(font=...)`, Remotion `@remotion/google-fonts`.
## Pares testados (título / texto) - todos Google Fonts, licença OFL
| Clima | Título (peso) | Texto/legenda (peso) |
|---|---|---|
| Impacto, Reels, esporte | Bebas Neue (400) | Montserrat (600) |
| Moderno, tech, negócios | Poppins (800) | Inter (500) |
| Cinematográfico, elegante | Playfair Display (700) | Source Sans 3 (400) |
| Documentário, editorial | DM Serif Display (400) | DM Sans (500) |
| Divertido, lifestyle | Fredoka (600) | Nunito (600) |
| Luxo, moda, minimal | Cormorant Garamond (600) | Montserrat (300) |
| Retrô, vintage | Abril Fatface (400) | Work Sans (400) |
| Futurista, games | Orbitron (800) | Exo 2 (500) |
| Pessoal, vlog, escrito à mão | Caveat (700) | Poppins (500) |
| Notícia, urgente | Oswald (700) | Roboto (400) |
## Estilo Old Money / elegante (fundo creme, tinta preta, cursiva sobreposta ao título) - testados
- Playfair Display 400 + Pinyon Script (sobreposta) · Bodoni Moda 500 + Bodoni Moda 500 i + Montserrat 500 CAIXA ALTA espaçada
- Bodoni Moda 500 i + Didact Gothic CAIXA ALTA · Pinyon Script + Montserrat 700 CAIXA ALTA (sobrepostas)
- Playfair Display SC + Libre Baskerville 400 i · Tinos 700 + Tinos 700 i + Source Sans 3 CAIXA ALTA
- Allura + Sanchez CAIXA ALTA · Bodoni Moda 400 CAIXA ALTA + Mrs Saint Delafield sobreposta · Italiana CAIXA ALTA + Josefin Sans 600
- Equivalentes grátis (Canva/pagas): The Seasons≈Bodoni Moda, Sloop/Burgues Script≈Pinyon/Mrs Saint Delafield, Symphony≈Allura, Safira March≈Italiana
- Layout: legenda pequena em CAIXA ALTA com tracking; cursiva maior e sobreposta. Tracking/sobreposição: Pillow ou Remotion (drawtext não tem tracking).
## Baixar fonte (estática, peso exato)
```bash
baixar_fonte() { # baixar_fonte "Bodoni Moda" 500 [i] -> caminho do .ttf (i = itálico). Peso inexistente: usar 400
  local d=~/.fonts/google f; mkdir -p $d; f="$d/$(echo "$1" | tr -d ' ')-$2${3:+i}.ttf"
  [ -s "$f" ] || curl -fsSL -o "$f" "$(curl -fsSL -A 'Mozilla/4.0' "https://fonts.googleapis.com/css2?family=${1// /+}:${3:+ital,}wght@${3:+1,}$2" \
    | grep -o 'https://[^)]*\.ttf' | head -1)" && echo "$f"; }
```
## Regras para vídeo
- Legenda: sem serifa, peso 500-700, contorno (`borderw=3:bordercolor=black`) ou caixa semitransparente.
- Legenda mín. ~4,5% da altura (1080p ~48 px; 1920 ~80 px). Vertical 9:16: texto fora dos 15% de cima e 20% de baixo.
- Máximo 2 famílias; contraste numa coisa, harmonia no resto. Finas (300) e cursivas só em títulos grandes. Outros sites: ver licença.
