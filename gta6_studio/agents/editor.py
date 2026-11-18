"""Rol: Editor de vídeo. Monta escenas, voz, textos, subtítulos y música en el vídeo final."""

from __future__ import annotations

import logging
import os
import random
from pathlib import Path

from PIL import Image

from ..config import Settings
from ..media import draw_centered, run_ffmpeg
from ..models import Script

log = logging.getLogger(__name__)
FPS = 30
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".ogg"}


def _fmt_ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(script: Script, voice: list[dict], out: Path, words_per_cue: int = 6) -> list[float]:
    """Crea subtítulos repartiendo cada narración en su escena. Devuelve el inicio de cada escena."""
    cues, starts, t0 = [], [], 0.0
    for scene, v in zip(script.scenes, voice):
        starts.append(t0)
        words = scene.narration.split()
        chunks = [words[i:i + words_per_cue] for i in range(0, len(words), words_per_cue)] or [[""]]
        per_word = v["seconds"] / max(len(words), 1)
        t = t0
        for ch in chunks:
            end = t + per_word * len(ch)
            cues.append((t, end, " ".join(ch)))
            t = end
        t0 += v["seconds"] + 0.25
    out.write_text(
        "\n".join(f"{i}\n{_fmt_ts(a)} --> {_fmt_ts(b)}\n{txt}\n" for i, (a, b, txt) in enumerate(cues, 1)),
        encoding="utf-8",
    )
    return starts


def _overlay_png(text: str, w: int, h: int, out: Path) -> Path:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if text:
        draw_centered(img, text.upper(), size=int(min(w, h) * 0.075), y_center=int(h * 0.14), fill="#FFE600")
    img.save(out)
    return out


def _segment(item: dict, audio: dict, overlay: Path, w: int, h: int, out: Path) -> None:
    dur = audio["seconds"] + 0.25
    cover = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"
    if item["kind"] == "title_card":
        frames = int(dur * FPS)
        vin = ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.2f}", "-i", item["file"]]
        vf = f"{cover},zoompan=z='min(zoom+0.0007,1.15)':d={frames}:s={w}x{h}:fps={FPS}"
    else:
        vin = ["-stream_loop", "-1", "-ss", str(item["start"]), "-t", f"{dur:.2f}", "-i", item["file"]]
        vf = f"{cover},fps={FPS}"
    run_ffmpeg([
        *vin,
        "-i", audio["file"],
        "-i", str(overlay),
        "-filter_complex",
        f"[0:v]{vf}[bg];[bg][2:v]overlay=0:0,format=yuv420p[v];[1:a]apad,aresample=44100[a]",
        "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "192k", "-ac", "2",
        str(out),
    ])


def run(settings: Settings, script: Script, fmt: str, voice: list[dict], plan: list[dict], work: Path) -> dict:
    f = settings["formats"][fmt]
    vcfg = settings["visuals"]
    w, h = f["width"], f["height"]
    seg_dir = work / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    segments = []
    for scene, audio, item in zip(script.scenes, voice, plan):
        overlay = _overlay_png(scene.on_screen_text, w, h, seg_dir / f"text_{scene.index:02d}.png")
        seg = seg_dir / f"seg_{scene.index:02d}.mp4"
        _segment(item, audio, overlay, w, h, seg)
        segments.append(seg)
        log.info("Escena %d montada (%s)", scene.index, item["kind"])

    concat_list = work / "concat.txt"
    concat_list.write_text("".join(f"file '{s.resolve()}'\n" for s in segments), encoding="utf-8")
    joined = work / "joined.mp4"
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(joined)])

    srt = work / "subs.srt"
    starts = build_srt(script, voice, srt, words_per_cue=4 if h > w else 7)

    music_dir = settings.path(vcfg["music_dir"])
    tracks = sorted(p for p in music_dir.glob("*") if p.suffix.lower() in AUDIO_EXT) if music_dir.exists() else []
    final = work / "final.mp4"
    args = ["-i", str(joined.resolve())]
    vf = "null"
    if vcfg.get("burn_subtitles", True):
        size, margin = (12, 70) if h > w else (16, 20)
        vf = (f"subtitles={srt.name}:force_style='FontName=DejaVu Sans,Bold=1,FontSize={size},"
              f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,MarginV={margin}'")
    if tracks:
        track = random.Random(work.name).choice(tracks)
        args += ["-stream_loop", "-1", "-i", str(track.resolve())]
        fc = (f"[0:v]{vf}[v];[1:a]volume={vcfg.get('music_volume', 0.12)}[m];"
              f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=0[a]")
    else:
        fc = f"[0:v]{vf}[v];[0:a]anull[a]"
    # cwd = carpeta de trabajo para que la ruta del .srt no necesite escapes
    cwd = os.getcwd()
    os.chdir(work)
    try:
        run_ffmpeg([*args, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", str(final.resolve())])
    finally:
        os.chdir(cwd)
    return {"video": str(final), "subtitles": str(srt), "scene_starts": starts}
