"""Montaje de VÍDEOS LARGOS (horizontal 1920×1080, 30 fps) de VICECITY DAYS TV.

Uso:  python shorts/montaje_largo.py largos/01-secretos-semana/plan.json [procesos=3]

Estilo (largos/01-secretos-semana/fase1-estilo.md): imagen a pantalla completa con Ken Burns lento o clip oficial,
contador redondo propio arriba a la izquierda (el anillo se llena mientras dura cada secreto), pastilla con el
nombre del secreto, tarjetas de capítulo, tarjetas gráficas propias para datos sin imagen, marca arriba a la
derecha y crédito "Footage: Rockstar Games". Sin subtítulos quemados: se genera un .srt para subir a YouTube.
Audio: voz + base electrónica suave con sidechain + efectos propios, normalizado a −14 LUFS.

plan.json:
  voz, palabras, salida, duracion
  escenas:   [{img | video+inicio, desde, hasta, foco, foco_fin, zoom}]
  secretos:  [{n, titulo, desde, hasta, color}]
  capitulos: [{num, titulo, desde}]
  tarjetas:  [{tipo: "lista", titulo, lineas, desde, hasta} | {tipo: "pastilla", texto, fondo, desde, hasta}]
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import montaje as M  # noqa: E402  (fuentes, paleta, efectos de sonido y base musical)

W, H, FPS = 1920, 1080, 30
COL = M.COL
font = M.font


def ease(t):
    return M.ease(t)


# ------------------------------------------------------------------ fondo de cada escena
class Imagen:
    def __init__(self, c, base):
        self.c = c
        z1 = max(c.get("zoom", [1.0, 1.08]))
        im = Image.open(base / c["img"]).convert("RGB")
        # cubrir 16:9 y dejar margen para el zoom
        esc = max(W * z1 / im.width, H * z1 / im.height) * 1.02
        self.im = im.resize((int(im.width * esc), int(im.height * esc)), Image.LANCZOS)

    def frame(self, t):
        c = self.c
        d = max(c["hasta"] - c["desde"], 0.01)
        p = ease((t - c["desde"]) / d) * 0.85 + ((t - c["desde"]) / d) * 0.15
        z0, z1 = c.get("zoom", [1.0, 1.08])
        z = z0 + (z1 - z0) * p
        f0 = c.get("foco", [0.5, 0.5]); f1 = c.get("foco_fin", f0)
        fx = f0[0] + (f1[0] - f0[0]) * p; fy = f0[1] + (f1[1] - f0[1]) * p
        # ventana visible en píxeles de la imagen escalada
        cw = W * (max(self.im.width / W, self.im.height / H)) / z
        ch = cw * H / W
        cw, ch = min(cw, self.im.width), min(ch, self.im.height)
        x = min(max(fx * self.im.width - cw / 2, 0), self.im.width - cw)
        y = min(max(fy * self.im.height - ch / 2, 0), self.im.height - ch)
        return self.im.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))


class Clip:
    def __init__(self, c, base):
        self.c = c
        self.ruta = (base / c["video"]).resolve()
        self.p = None
        self.t_leido = None
        self.ult = None

    def _abrir(self, t):
        self.cerrar()
        ini = self.c.get("inicio", 0) + (t - self.c["desde"])
        z = self.c.get("zoom", [1.0, 1.0])[0]
        vf = f"fps={FPS},scale={int(W * z)}:{int(H * z)}:force_original_aspect_ratio=increase,crop={W}:{H}"
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{max(ini, 0):.3f}", "-i", str(self.ruta), "-an", "-vf", vf,
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.t_leido = t - 1 / FPS

    def frame(self, t):
        if self.p is None or t < self.t_leido or t - self.t_leido > 0.5:
            self._abrir(t)
        while self.t_leido < t - 1e-6:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            self.ult = Image.frombuffer("RGB", (W, H), buf, "raw", "RGB", 0, 1).copy()
            self.t_leido += 1 / FPS
        return self.ult if self.ult is not None else Image.new("RGB", (W, H), COL["fondo"])

    def cerrar(self):
        if self.p:
            self.p.stdout.close(); self.p.kill(); self.p.wait(); self.p = None


# ------------------------------------------------------------------ capas propias
@lru_cache(None)
def viñeta():
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    a = np.clip((d - 0.75) / 0.7, 0, 1) ** 1.6 * 150
    arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = COL["fondo"]; arr[..., 3] = a.astype(np.uint8)
    # degradado inferior para que se lean las pastillas
    g = np.clip((y - H * 0.72) / (H * 0.28), 0, 1) * 120
    arr[..., 3] = np.maximum(arr[..., 3], g.astype(np.uint8))
    return Image.fromarray(arr, "RGBA")


def contador(fr, s, t):
    """Círculo oscuro con el número y un anillo que se llena durante el secreto."""
    cx, cy, r = 118, 118, 66
    d = ImageDraw.Draw(fr, "RGBA")
    k = (t - s["desde"]) * FPS
    esc = 1 + 0.25 * math.exp(-k / 4) * math.cos(k / 2.2) if k < 18 else 1.0   # golpe al cambiar de número
    rr = r * esc
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(8, 8, 16, 225))
    d.ellipse([cx - rr + 6, cy - rr + 6, cx + rr - 6, cy + rr - 6], outline=(255, 255, 255, 40), width=9)
    prog = min(max((t - s["desde"]) / max(s["hasta"] - s["desde"], 0.1), 0), 1)
    col = COL[s.get("color", "rosa")]
    if prog > 0:
        d.arc([cx - rr + 6, cy - rr + 6, cx + rr - 6, cy + rr - 6], -90, -90 + 360 * prog, fill=col + (255,), width=9)
    num = M.texto_img(str(s["n"]), "Anton-Regular.ttf", int(70 * esc), "blanco", 0, "negro", False)
    fr.alpha_composite(num, (int(cx - num.width / 2), int(cy - num.height / 2) - 4))


def pastilla(fr, texto, fondo, t, desde, hasta, x=60, y=H - 150, size=46):
    a = min(ease((t - desde) / 0.35), ease((hasta - t) / 0.3))
    if a <= 0:
        return
    p = M.pastilla(texto, fondo, "negro" if fondo in ("amarillo", "blanco") else "blanco", size)
    dx = int((1 - a) * -80)
    capa = p.copy(); capa.putalpha(capa.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(capa, (x + dx, y))


def tarjeta_capitulo(fr, c, t):
    dur = 2.6
    k = t - c["desde"]
    if not 0 <= k <= dur:
        return
    a = min(ease(k / 0.35), ease((dur - k) / 0.4))
    capa = Image.new("RGBA", (W, H), (8, 8, 16, int(170 * a)))
    fr.alpha_composite(capa)
    d = ImageDraw.Draw(fr)
    barra = int(W * 0.42 * ease(k / 0.6))
    d.rectangle([W / 2 - barra / 2, H / 2 + 70, W / 2 + barra / 2, H / 2 + 78], fill=COL["rosa"] + (int(255 * a),))
    t1 = M.texto_img(f"PART {c['num']}", "Montserrat-Black.ttf", 44, "amarillo", 0, "negro", True)
    t2 = M.texto_img(c["titulo"].upper(), "Anton-Regular.ttf", 120, "blanco", 0, "negro", True)
    for im, y in ((t1, H / 2 - 150), (t2, H / 2 - 95)):
        im2 = im.copy(); im2.putalpha(im2.getchannel("A").point(lambda v: int(v * a)))
        fr.alpha_composite(im2, (int(W / 2 - im.width / 2), int(y + (1 - a) * 30)))


def tarjeta_lista(fr, c, t):
    k = t - c["desde"]
    dur = c["hasta"] - c["desde"]
    if not 0 <= k <= dur:
        return
    a = min(ease(k / 0.3), ease((dur - k) / 0.3))
    n = len(c["lineas"])
    alto = 110 + n * 78
    ancho = 1180
    x0, y0 = int(W / 2 - ancho / 2), int(H / 2 - alto / 2)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rounded_rectangle([x0, y0, x0 + ancho, y0 + alto], 26, fill=(8, 8, 16, 228), outline=COL["morado"] + (255,), width=4)
    d.rectangle([x0, y0 + 92, x0 + ancho, y0 + 96], fill=COL["rosa"] + (255,))
    capa.alpha_composite(M.texto_img(c["titulo"].upper(), "Anton-Regular.ttf", 58, "amarillo", 0, "negro", False), (x0 + 36, y0 + 14))
    paso = max((dur - 0.8) / max(n, 1), 0.25)
    for i, ln in enumerate(c["lineas"]):
        b = ease((k - 0.4 - i * min(paso, 1.4)) / 0.3)
        if b <= 0:
            continue
        im = M.texto_img(ln, "Montserrat-ExtraBold.ttf", 40, "blanco", 0, "negro", False).copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * b)))
        capa.alpha_composite(im, (x0 + 50 + int((1 - b) * 40), y0 + 120 + i * 78))
    capa.putalpha(capa.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(capa)


def texto_grande(fr, c, t):
    """Texto enorme del gancho que entra de golpe (escala 1.5 → 1 con rebote)."""
    k = t - c["desde"]
    if not 0 <= k <= c["hasta"] - c["desde"]:
        return
    a = min(1.0, M.ease((c["hasta"] - t) / 0.2))
    esc = 1 + 0.3 * (1 - M.ease_back(k / 0.22))
    im = M.texto_img(c["texto"], "Anton-Regular.ttf", c.get("size", 120), c.get("color", "blanco"), 8, "negro", True)
    if esc != 1:
        im = im.resize((max(1, int(im.width * esc)), max(1, int(im.height * esc))), Image.BILINEAR)
    if a < 1:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    y = c.get("y", H * 0.74)
    fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(y - im.height / 2)))


def titulo_golpe(fr, c, t):
    k = t - c["desde"]
    if not 0 <= k <= c["hasta"] - c["desde"]:
        return
    fr.alpha_composite(Image.new("RGBA", (W, H), (8, 8, 16, 120)))
    esc = 1 + 1.2 * (1 - M.ease(k / 0.18))
    t1 = M.texto_img(c["texto"], "Anton-Regular.ttf", 270, "amarillo", 10, "negro", True)
    t1 = t1.resize((int(t1.width * esc), int(t1.height * esc)), Image.BILINEAR) if esc != 1 else t1
    fr.alpha_composite(t1, (int(W / 2 - t1.width / 2), int(H * 0.44 - t1.height / 2)))
    b = M.ease((k - 0.25) / 0.25)
    if b > 0:
        t2 = M.texto_img(c["sub"], "Montserrat-Black.ttf", 58, "blanco", 4, "negro", True).copy()
        t2.putalpha(t2.getchannel("A").point(lambda v: int(v * b)))
        fr.alpha_composite(t2, (int(W / 2 - t2.width / 2), int(H * 0.66 + (1 - b) * 30)))


@lru_cache(None)
def marca_img():
    return M.texto_img("VICECITY DAYS TV", "Montserrat-Black.ttf", 30, "blanco", 0, "negro", True)


@lru_cache(None)
def credito_img():
    return M.texto_img("Footage: Rockstar Games · Unofficial fan channel", "Montserrat-ExtraBold.ttf", 20, "blanco", 0, "negro", True)


def componer(plan, fondo, t):
    fr = fondo.convert("RGBA")
    fr.alpha_composite(viñeta())
    for s in plan["secretos"]:
        if s["desde"] <= t < s["hasta"]:
            contador(fr, s, t)
            pastilla(fr, s["titulo"], s.get("color", "rosa"), t, s["desde"] + 0.3, min(s["desde"] + 4.5, s["hasta"]))
    for c in plan.get("tarjetas", []):
        if c["tipo"] == "lista":
            tarjeta_lista(fr, c, t)
        elif c["tipo"] == "grande":
            texto_grande(fr, c, t)
        elif c["tipo"] == "titulo":
            titulo_golpe(fr, c, t)
        elif c["tipo"] == "pastilla":
            pastilla(fr, c["texto"], c.get("fondo", "amarillo"), t, c["desde"], c["hasta"], x=c.get("x", 60), y=c.get("y", H - 240), size=c.get("size", 40))
    for c in plan.get("capitulos", []):
        tarjeta_capitulo(fr, c, t)
    m = marca_img(); fr.alpha_composite(m, (W - m.width - 40, 34))
    cr = credito_img(); fr.alpha_composite(cr, (W - cr.width - 40, H - cr.height - 26))
    return fr.convert("RGB")


# ------------------------------------------------------------------ render por trozos en paralelo
def render_trozo(args):
    plan_path, i0, i1, salida = args
    plan = json.loads(Path(plan_path).read_text())
    base = Path(plan_path).parent
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-threads", "2", salida],
                           stdin=subprocess.PIPE)
    escenas = plan["escenas"]
    act, obj = None, None
    for i in range(i0, i1):
        t = i / FPS
        e = next((e for e in escenas if e["desde"] <= t < e["hasta"]), escenas[-1])
        if e is not act:
            if isinstance(obj, Clip):
                obj.cerrar()
            act = e
            obj = Clip(e, base) if "video" in e else Imagen(e, base)
        base_fr = obj.frame(t)
        k = (t - e["desde"]) * FPS
        if e.get("golpe") and k < 7:          # golpe de zoom al entrar
            z = 1 + 0.14 * (1 - k / 7) ** 2
            cw, ch = W / z, H / z
            base_fr = base_fr.resize((W, H), Image.BILINEAR, box=((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2))
        fr = componer(plan, base_fr, t)
        if e.get("flash") and k < 5:          # destello blanco en el corte
            fr = Image.blend(fr, Image.new("RGB", (W, H), (255, 255, 255)), 0.75 * (1 - k / 5))
        enc.stdin.write(fr.tobytes())
    if isinstance(obj, Clip):
        obj.cerrar()
    enc.stdin.close(); enc.wait()
    return salida


def audio(plan, base, dur):
    voz = base / plan["voz"]
    ritmo = base / "_ritmo.wav"
    M.ritmo(dur + 1, plan.get("bpm", 100), ritmo)
    eventos = [(s["desde"], "pop") for s in plan["secretos"]] + [(c["desde"], "whoosh") for c in plan.get("capitulos", [])]
    eventos += [(c["desde"] + 0.4, "ding") for c in plan.get("tarjetas", []) if c["tipo"] == "lista"]
    eventos += [tuple(x) for x in plan.get("sfx", [])]
    sfx = base / "_sfx.wav"
    M.pista_sfx(dur, eventos, sfx)
    mezcla = base / "_mezcla.wav"
    vol = plan.get("musica", 0.10)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voz), "-i", str(ritmo), "-i", str(sfx), "-filter_complex",
                    f"[0:a]aformat=channel_layouts=stereo,asplit[v][vs];[1:a]volume='if(lt(t,{plan.get('gancho_hasta', 0)}),{plan.get('musica_gancho', vol)},{vol})':eval=frame[m];"
                    f"[m][vs]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=400[md];"
                    f"[2:a]volume=0.30[fx];[v][md][fx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "48000", str(mezcla)], check=True)
    return mezcla


def srt(palabras, salida):
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    lineas, cur = [], []
    for w in palabras:
        cur.append(w)
        if len(cur) >= 8 or w["w"].endswith((".", "?", "!")):
            lineas.append(cur); cur = []
    if cur:
        lineas.append(cur)
    out = [f"{i}\n{ts(l[0]['s'])} --> {ts(l[-1]['e'])}\n{' '.join(x['w'] for x in l)}\n" for i, l in enumerate(lineas, 1)]
    Path(salida).write_text("\n".join(out))


def montar(plan_path, procesos="3"):
    plan_path = str(Path(plan_path).resolve())
    plan = json.loads(Path(plan_path).read_text())
    base = Path(plan_path).parent
    dur = plan["duracion"]
    n = int(dur * FPS)
    k = int(procesos)
    cortes = [n * j // k for j in range(k + 1)]
    trozos = [(plan_path, cortes[j], cortes[j + 1], str(base / f"_trozo{j}.mp4")) for j in range(k)]
    with Pool(k) as p:
        partes = p.map(render_trozo, trozos)
    lista = base / "_lista.txt"
    lista.write_text("".join(f"file '{Path(x).name}'\n" for x in partes))
    mezcla = audio(plan, base, dur)
    salida = base / plan["salida"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-i", str(mezcla),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(salida)], check=True)
    if plan.get("palabras"):
        srt(json.loads((base / plan["palabras"]).read_text()), base / "subtitulos.srt")
    for x in partes + [str(lista), str(base / "_ritmo.wav"), str(base / "_sfx.wav"), str(mezcla)]:
        Path(x).unlink(missing_ok=True)
    print(salida)
    return salida


if __name__ == "__main__":
    montar(*sys.argv[1:])
