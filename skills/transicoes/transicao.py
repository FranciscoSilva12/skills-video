#!/usr/bin/env python3
"""Junta clipes com transições (ffmpeg xfade + acrossfade).
uso: transicao.py SAIDA.mp4 clip1 [TRANSICAO[:SEG]] clip2 [TRANSICAO[:SEG]] clip3 ... [--previa] [--res 1920x1080] [--fps 30]
ex.: transicao.py final.mp4 a.mp4 fade:0.8 b.mp4 zoomin:0.5 c.mp4 corte d.mp4
TRANSICAO = nome do xfade (fade, dissolve, slideleft, zoomin, fadewhite...) ou 'corte'. Padrão: fade:0.5"""
import json, subprocess, sys

def probe(f):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
                                   "-of", "json", f], capture_output=True, text=True, check=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    return float(j["format"]["duration"]), v, any(s["codec_type"] == "audio" for s in j["streams"])

args = sys.argv[1:]
previa = "--previa" in args; args = [a for a in args if a != "--previa"]
opt = {}
for k in ("--res", "--fps"):
    if k in args: i = args.index(k); opt[k] = args[i + 1]; del args[i:i + 2]
out, items = args[0], args[1:]
clips, trans = [], []
for it in items:
    if it.lower().endswith((".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi")):
        if len(trans) < len(clips): trans.append(("fade", 0.5))
        clips.append(it)
    else:
        n, _, s = it.partition(":"); trans.append((n, float(s) if s else (0 if n == "corte" else 0.5)))
if len(clips) < 2 or len(trans) != len(clips) - 1: sys.exit(__doc__)

info = [probe(c) for c in clips]
w, h = (int(x) for x in opt.get("--res", f'{info[0][1]["width"]}x{info[0][1]["height"]}').split("x"))
fps = opt.get("--fps", info[0][1]["r_frame_rate"])
if previa: w, h = w // 2 // 2 * 2, h // 2 // 2 * 2

cmd, fc = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-stats", "-y"], []
for i, (c, (dur, _, has_a)) in enumerate(zip(clips, info)):
    cmd += ["-i", c]
    fc.append(f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},format=yuv420p,settb=AVTB[v{i}]")
    fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,asetpts=PTS-STARTPTS[a{i}]" if has_a else
              f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.3f}[a{i}]")
vl, al, acc = "v0", "a0", info[0][0]
for i, (name, d) in enumerate(trans, 1):
    d = min(d, info[i - 1][0] / 2, info[i][0] / 2)
    if name == "corte" or d <= 0:
        fc.append(f"[{vl}][v{i}]concat=n=2:v=1:a=0[vx{i}]"); fc.append(f"[{al}][a{i}]concat=n=2:v=0:a=1[ax{i}]")
    else:
        fc.append(f"[{vl}][v{i}]xfade=transition={name}:duration={d:.3f}:offset={acc - d:.3f}[vx{i}]")
        fc.append(f"[{al}][a{i}]acrossfade=d={d:.3f}[ax{i}]"); acc -= d
    acc += info[i][0]; vl, al = f"vx{i}", f"ax{i}"
q = ["-preset", "veryfast", "-crf", "23"] if previa else ["-preset", "slow", "-crf", "18"]
cmd += ["-filter_complex", ";".join(fc), "-map", f"[{vl}]", "-map", f"[{al}]", "-c:v", "libx264", *q,
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print(f"ok: {out} ({acc:.2f}s, {w}x{h}, {'prévia' if previa else 'qualidade máxima'})")
