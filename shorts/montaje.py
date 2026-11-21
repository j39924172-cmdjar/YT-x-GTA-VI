"""Plantilla de montaje de Shorts de VICECITY DAYS TV (sección 4 del documento maestro).

Uso:  python shorts/montaje.py shorts/03-jason-lucia/plan.json

El plan describe las escenas (capturas con barrido Ken Burns, etiquetas y flechas rojas) y las capas
(titular del gancho, "FACT n/3", ruta animada, pastillas, CTA). La plantilla añade sola: degradados,
subtítulos palabra a palabra, destello en cada corte, marca "VICECITY DAYS TV", fuente en pantalla
y audio (voz + ritmo electrónico propio con sidechain, normalizado a −14 LUFS).
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FUENTES = Path(__file__).parent / "fuentes"
W, H, FPS = 1080, 1920, 30
COL = {  # paleta del documento maestro
    "fondo": (8, 8, 16), "morado": (139, 53, 255), "lila": (199, 125, 255), "blanco": (244, 241, 255),
    "rosa": (255, 46, 140), "amarillo": (255, 206, 40), "rojo": (255, 45, 45), "verde": (46, 204, 113), "negro": (0, 0, 0),
}
# Zonas seguras de Shorts: arriba ~160 px de controles; abajo ~420 px de título y botones; derecha ~130 px.
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT = 170, 1500, 950


@lru_cache(None)
def font(nombre: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FUENTES / nombre), size)


def ease(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def ease_back(t: float) -> float:  # pequeño rebote al aparecer
    t = min(max(t, 0.0), 1.0)
    c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


# ------------------------------------------------------------------ piezas gráficas (se cachean)
@lru_cache(None)
def texto_img(txt: str, fname: str, size: int, color: str, stroke: int = 0, stroke_col: str = "negro", shadow: bool = True) -> Image.Image:
    f = font(fname, size)
    l, t, r, b = f.getbbox(txt, stroke_width=stroke)
    pad = 24
    im = Image.new("RGBA", (r - l + pad * 2, b - t + pad * 2), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + 4, pad - t + 6), txt, font=f, fill=(0, 0, 0, 170), stroke_width=stroke, stroke_fill=(0, 0, 0, 170))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text((pad - l, pad - t), txt, font=f, fill=COL[color] + (255,), stroke_width=stroke, stroke_fill=COL[stroke_col] + (255,))
    return im


@lru_cache(None)
def pastilla(txt: str, fondo: str, color: str = "negro", size: int = 54, icono: str = "") -> Image.Image:
    f = font("Montserrat-Black.ttf", size)
    l, t, r, b = f.getbbox(txt)
    tw, th = r - l, b - t
    ico = int(size * 1.05) if icono else 0
    gap = int(size * 0.35) if icono else 0
    px, py = int(size * 0.55), int(size * 0.38)
    w, h = tw + px * 2 + ico + gap, th + py * 2
    im = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((8, 12, w + 8, h + 12), radius=h // 2, fill=(0, 0, 0, 150))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((8, 8, w + 8, h + 8), radius=h // 2, fill=COL[fondo] + (255,))
    d.text((8 + px - l, 8 + py - t), txt, font=f, fill=COL[color] + (255,))
    if icono:
        cx, cy, rr = 8 + px + tw + gap + ico // 2, 8 + h // 2, ico // 2
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=COL["verde" if icono == "ok" else "rojo"] + (255,), outline=COL["blanco"] + (255,), width=4)
        lw = max(5, ico // 8)
        if icono == "ok":
            d.line([(cx - rr * 0.45, cy + rr * 0.02), (cx - rr * 0.1, cy + rr * 0.38), (cx + rr * 0.5, cy - rr * 0.35)], fill=COL["blanco"] + (255,), width=lw, joint="curve")
        else:
            k = rr * 0.38
            d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=COL["blanco"] + (255,), width=lw)
            d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=COL["blanco"] + (255,), width=lw)
    return im


@lru_cache(None)
def degradados() -> Image.Image:
    g = np.zeros((H, W, 4), np.uint8)
    y = np.arange(H)[:, None]
    top = np.clip(1 - y / 520, 0, 1) ** 1.6 * 200
    bot = np.clip((y - (H - 760)) / 760, 0, 1) ** 1.4 * 235
    g[..., 3] = np.maximum(top, bot).astype(np.uint8)
    g[..., :3] = COL["fondo"]
    return Image.fromarray(g, "RGBA")


def pegar(base: Image.Image, im: Image.Image, cx: float, cy: float, alpha: float = 1.0, escala: float = 1.0) -> None:
    if alpha <= 0.01 or escala <= 0.01:
        return
    if abs(escala - 1) > 0.01:
        im = im.resize((max(1, int(im.width * escala)), max(1, int(im.height * escala))), Image.BILINEAR)
    if alpha < 0.99:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda a: int(a * alpha)))
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def flecha(d: ImageDraw.ImageDraw, x0, y0, x1, y1, grosor=22):
    """Flecha roja con borde blanco de (x0,y0) a la punta (x1,y1)."""
    ang = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    head = grosor * 2.6

    def pts(g, hd):
        bx, by = x1 - math.cos(ang) * hd, y1 - math.sin(ang) * hd
        nx, ny = -math.sin(ang), math.cos(ang)
        return [(x0 + nx * g / 2, y0 + ny * g / 2), (bx + nx * g / 2, by + ny * g / 2), (bx + nx * hd * 0.62, by + ny * hd * 0.62),
                (x1, y1), (bx - nx * hd * 0.62, by - ny * hd * 0.62), (bx - nx * g / 2, by - ny * g / 2), (x0 - nx * g / 2, y0 - ny * g / 2)]
    if L < head:
        return
    d.polygon(pts(grosor + 12, head + 10), fill=COL["blanco"] + (255,))
    d.polygon(pts(grosor, head), fill=COL["rojo"] + (255,))


# ------------------------------------------------------------------ fondo con Ken Burns
class Escena:
    def __init__(self, cfg: dict, base: Path):
        self.cfg = cfg
        im = Image.open(base / cfg["img"]).convert("RGB")
        if im.height > 2160:
            im = im.resize((int(im.width * 2160 / im.height), 2160), Image.LANCZOS)
        self.im = im
        self.t0, self.t1 = cfg["desde"], cfg["hasta"]
        self.f0 = cfg.get("foco", [0.5, 0.5])
        self.f1 = cfg.get("foco_fin", self.f0)
        self.z0, self.z1 = cfg.get("zoom", [1.0, 1.12])

    def ventana(self, t: float):
        k = ease((t - self.t0) / max(self.t1 - self.t0, 0.01)) * 0.85 + ((t - self.t0) / max(self.t1 - self.t0, 0.01)) * 0.15
        z = self.z0 + (self.z1 - self.z0) * k
        fx = self.f0[0] + (self.f1[0] - self.f0[0]) * k
        fy = self.f0[1] + (self.f1[1] - self.f0[1]) * k
        ch = self.im.height / z
        cw = ch * W / H
        if cw > self.im.width:
            cw = self.im.width
            ch = cw * H / W
        x = min(max(fx * self.im.width - cw / 2, 0), self.im.width - cw)
        y = min(max(fy * self.im.height - ch / 2, 0), self.im.height - ch)
        return x, y, cw, ch

    def render(self, t: float) -> Image.Image:
        x, y, cw, ch = self.ventana(t)
        return self.im.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch)).convert("RGBA")

    def a_pantalla(self, t: float, px: float, py: float):
        x, y, cw, ch = self.ventana(t)
        return (px * self.im.width - x) * W / cw, (py * self.im.height - y) * H / ch


class EscenaVideo:
    """Escena con un plano de un vídeo oficial: {"video": ruta, "inicio": s, "foco": [x, y], "zoom": [a, b]}.
    Recorta en vertical 9:16 alrededor del foco y hace un empuje suave (zoom de a a b). Lee los fotogramas en orden."""

    def __init__(self, cfg: dict, base: Path):
        self.cfg, self.t0, self.t1 = cfg, cfg["desde"], cfg["hasta"]
        self.ruta = (base / cfg["video"]).resolve()
        self.f0 = cfg.get("foco", [0.5, 0.5])
        self.f1 = cfg.get("foco_fin", self.f0)
        self.z0, self.z1 = cfg.get("zoom", [1.0, 1.06])
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                               "-of", "csv=p=0", str(self.ruta)], capture_output=True, text=True).stdout.strip().split(",")
        self.vw, self.vh = int(info[0]), int(info[1])
        self.proc, self.idx, self.ultimo = None, -1, None
        self.alto = 1920   # el vídeo se decodifica a 1920 de alto y se recorta aquí

    def _abrir(self):
        dur = self.t1 - self.t0 + 1.0
        self.sw = int(self.vw * self.alto / self.vh) // 2 * 2
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{self.cfg.get('inicio', 0):.3f}", "-i", str(self.ruta), "-t", f"{dur:.3f}",
                                      "-vf", f"scale={self.sw}:{self.alto},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                     stdout=subprocess.PIPE)

    def ventana(self, t: float):
        k = min(max((t - self.t0) / max(self.t1 - self.t0, 0.01), 0), 1)
        z = self.z0 + (self.z1 - self.z0) * k
        fx = self.f0[0] + (self.f1[0] - self.f0[0]) * k
        fy = self.f0[1] + (self.f1[1] - self.f0[1]) * k
        sw = int(self.vw * self.alto / self.vh)
        ch = self.alto / z
        cw = ch * W / H
        x = min(max(fx * sw - cw / 2, 0), sw - cw)
        y = min(max(fy * self.alto - ch / 2, 0), self.alto - ch)
        return x, y, cw, ch, sw

    def render(self, t: float) -> Image.Image:
        if self.proc is None:
            self._abrir()
        objetivo = int((t - self.t0) * FPS)
        tam = self.sw * self.alto * 3
        while self.idx < objetivo:
            buf = self.proc.stdout.read(tam)
            if len(buf) < tam:
                break
            self.ultimo = Image.frombytes("RGB", (self.sw, self.alto), buf)
            self.idx += 1
        if self.ultimo is None:
            self.ultimo = Image.new("RGB", (self.sw, self.alto), "black")
        x, y, cw, ch, _ = self.ventana(t)
        return self.ultimo.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch)).convert("RGBA")

    def a_pantalla(self, t: float, px: float, py: float):
        x, y, cw, ch, sw = self.ventana(t)
        return (px * sw - x) * W / cw, (py * self.alto - y) * H / ch

    def cerrar(self):
        if self.proc:
            self.proc.kill()


def nueva_escena(cfg: dict, base: Path):
    return EscenaVideo(cfg, base) if "video" in cfg else Escena(cfg, base)


# ------------------------------------------------------------------ capas
def capa_titulo(fr, c, t):
    k = ease_back((t - c["desde"]) / 0.35)
    y = SAFE_TOP + 120
    for i, (txt, color) in enumerate(c["lineas"]):
        im = texto_img(txt, "Anton-Regular.ttf", c.get("size", 150), color, stroke=8)
        ki = ease_back((t - c["desde"] - i * 0.12) / 0.35)
        pegar(fr, im, W / 2, y + im.height / 2 - 20, alpha=min(1, ki * 1.5), escala=0.6 + 0.4 * ki)
        y += im.height - 40
    if c.get("pastilla"):
        p = pastilla(c["pastilla"], "rosa", "blanco", 50)
        ki = ease_back((t - c["desde"] - 0.3) / 0.35)
        pegar(fr, p, W / 2, y + 40, alpha=min(1, ki * 1.5), escala=0.6 + 0.4 * ki)
    return k


def capa_fact(fr, c, t):
    k = ease((t - c["desde"]) / 0.3)
    x_off = (1 - k) * -500
    p = pastilla(f"{c.get('etiqueta', 'FACT')} {c['n']}/{c['total']}", "rosa", "blanco", 46)
    pegar(fr, p, 60 + p.width / 2 + x_off, SAFE_TOP + 70)
    nombre = texto_img(c["titulo"], "Anton-Regular.ttf", 120, "amarillo", stroke=7)
    pegar(fr, nombre, 54 + nombre.width / 2 + x_off * 1.2, SAFE_TOP + 70 + 110)
    # contador con barra: 3 segmentos, el actual se llena con el tiempo
    d = ImageDraw.Draw(fr)
    seg_w, gap, y0 = 250, 14, SAFE_TOP + 70 + 205
    prog = min(max((t - c["desde"]) / (c["hasta"] - c["desde"]), 0), 1)
    for i in range(c["total"]):
        x0 = 60 + i * (seg_w + gap) + x_off
        d.rounded_rectangle((x0, y0, x0 + seg_w, y0 + 14), radius=7, fill=(255, 255, 255, 70))
        fill = 1 if i < c["n"] - 1 else prog if i == c["n"] - 1 else 0
        if fill > 0:
            d.rounded_rectangle((x0, y0, x0 + seg_w * fill, y0 + 14), radius=7, fill=COL["amarillo"] + (255,))


def capa_ruta(fr, c, t):
    """Tarjeta animada: origen → destino con línea discontinua que se dibuja."""
    k = ease((t - c["desde"]) / 0.35)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cx, top, bottom = W / 2, 640, 1060
    d.rounded_rectangle((90, top - 110, W - 90, bottom + 110), radius=48, fill=(8, 8, 16, int(215 * k)), outline=COL["morado"] + (int(255 * k),), width=6)
    prog = ease((t - c["desde"] - 0.3) / 1.4)
    n = 26
    for i in range(int(n * prog)):
        y = top + 70 + (bottom - top - 140) * i / n
        d.ellipse((cx - 9, y - 9, cx + 9, y + 9), fill=COL["lila"] + (255,))
    for (txt, y, color, delay) in [(c["origen"], top, "blanco", 0.1), (c["destino"], bottom, "amarillo", 1.5)]:
        kk = ease_back((t - c["desde"] - delay) / 0.35)
        if kk <= 0:
            continue
        pr = 34 * kk
        d.ellipse((cx - pr, y - pr, cx + pr, y + pr), fill=COL["rosa"] + (255,), outline=COL["blanco"] + (255,), width=6)
        im = texto_img(txt, "Anton-Regular.ttf", 96, color, stroke=6)
        ov.alpha_composite(im, (int(cx - im.width / 2), int(y + (-150 if y == top else 40))))
    fr.alpha_composite(ov)
    if c.get("nota") and t >= c["nota"]["desde"]:
        kk = ease_back((t - c["nota"]["desde"]) / 0.3)
        p = pastilla(c["nota"]["texto"], "amarillo", "negro", 56, icono=c["nota"].get("icono", ""))
        pegar(fr, p, cx, (top + bottom) / 2, escala=0.5 + 0.5 * kk, alpha=min(1, kk * 2))


def capa_pastillas(fr, c, t):
    for i, it in enumerate(c["items"]):
        if t < it["desde"]:
            continue
        kk = ease_back((t - it["desde"]) / 0.3)
        p = pastilla(it["texto"], it.get("fondo", "amarillo"), it.get("color", "negro"), it.get("size", 72), icono=it.get("icono", ""))
        pegar(fr, p, W / 2, it.get("y", 560 + i * 170), escala=0.5 + 0.5 * kk, alpha=min(1, kk * 2))


def capa_cta(fr, c, t):
    k = ease_back((t - c["desde"]) / 0.4)
    pulse = 1 + 0.04 * math.sin((t - c["desde"]) * 8)
    big = texto_img(c["lineas"][0], "Anton-Regular.ttf", 190, "amarillo", stroke=9)
    pegar(fr, big, W / 2, 700, alpha=min(1, k * 1.5), escala=(0.6 + 0.4 * k) * pulse)
    p = pastilla(c["lineas"][1], "rosa", "blanco", 52)
    pegar(fr, p, W / 2, 880, alpha=min(1, k * 1.5), escala=0.6 + 0.4 * k)


def capa_tarjeta(fr, c, t):
    """Tarjeta de dato: caja oscura con líneas que van apareciendo; una línea puede tener contador ("contar": 345).
    La caja se calcula con todas las líneas desde el principio para que no cambie de tamaño."""
    k = ease_back((t - c["desde"]) / 0.35)
    if k <= 0:
        return

    def pieza(ln, txt):
        if ln.get("pastilla"):
            return pastilla(txt, ln.get("fondo", "amarillo"), ln.get("color", "negro"), ln.get("size", 54), icono=ln.get("icono", ""))
        return texto_img(txt, ln.get("fuente", "Anton-Regular.ttf"), ln.get("size", 90), ln.get("color", "blanco"), stroke=ln.get("stroke", 6))

    finales = [pieza(ln, ln["texto"].replace("{n}", f"{ln['contar']:,}") if "contar" in ln else ln["texto"]) for ln in c["lineas"]]
    ancho = min(W - 120, max(p.width for p in finales) + 80)
    escalas = [min(1.0, (ancho - 40) / p.width) for p in finales]
    alto = sum((p.height - 18) * e for p, e in zip(finales, escalas)) + 60
    cy = c.get("y", 820)
    caja = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(caja).rounded_rectangle((W / 2 - ancho / 2, cy - alto / 2, W / 2 + ancho / 2, cy + alto / 2), radius=40,
                                          fill=(8, 8, 16, int(215 * min(1, k))), outline=COL[c.get("borde", "morado")] + (int(255 * min(1, k)),), width=6)
    fr.alpha_composite(caja)
    y = cy - alto / 2 + 30
    for ln, fin, esc in zip(c["lineas"], finales, escalas):
        t0 = c["desde"] + ln.get("retraso", 0)
        if t >= t0:
            txt = ln["texto"]
            if "contar" in ln:
                txt = txt.replace("{n}", f"{int(round(ln['contar'] * ease((t - t0) / ln.get('dur', 1.0)))):,}")
            im = pieza(ln, txt)
            kk = ease_back((t - t0) / 0.25)
            pegar(fr, im, W / 2, y + fin.height * esc / 2 - 9, escala=esc * (0.7 + 0.3 * kk), alpha=min(1, kk * 2))
        y += (fin.height - 18) * esc


def capa_comparativa(fr, c, t):
    """Pantalla partida: el fondo (juego) arriba y una foto real abajo, con etiquetas IN GAME / REAL LIFE."""
    k = ease((t - c["desde"]) / 0.3)
    real = c["_escena"]
    abajo = real.render(t).crop((0, (H - H // 2) // 2, W, (H - H // 2) // 2 + H // 2))
    y0 = int(H / 2 + (1 - k) * H / 2)
    fr.alpha_composite(abajo, (0, y0))
    ImageDraw.Draw(fr).rectangle((0, y0 - 5, W, y0 + 5), fill=COL["amarillo"] + (255,))
    pa = pastilla(c.get("arriba", "IN GAME"), "rosa", "blanco", 40)
    pb = pastilla(c.get("abajo", "REAL LIFE"), "amarillo", "negro", 40, icono="ok")
    pegar(fr, pa, 50 + pa.width / 2, y0 - 62, alpha=k)
    pegar(fr, pb, 50 + pb.width / 2, y0 + 66, alpha=k)
    if c.get("credito"):
        cr = texto_img(c["credito"], "Montserrat-ExtraBold.ttf", 24, "blanco")
        pegar(fr, cr, W - 60 - cr.width / 2, y0 + H // 2 - 40, alpha=0.8 * k)


CAPAS = {"titulo": capa_titulo, "fact": capa_fact, "ruta": capa_ruta, "pastillas": capa_pastillas, "cta": capa_cta,
         "tarjeta": capa_tarjeta, "comparativa": capa_comparativa}


def etiqueta_escena(fr, esc: Escena, t):
    et = esc.cfg.get("etiqueta")
    if not et:
        return
    t0 = esc.t0 + et.get("desde", 0.25)
    if t < t0:
        return
    kk = ease_back((t - t0) / 0.3)
    p = pastilla(et["texto"], et.get("fondo", "amarillo"), et.get("color", "negro"), et.get("size", 58), icono=et.get("icono", ""))
    lx, ly = et.get("pos", [W / 2, 1060])
    pegar(fr, p, lx, ly, escala=0.5 + 0.5 * kk, alpha=min(1, kk * 2))
    if et.get("flecha"):
        tx, ty = esc.a_pantalla(t, *et["flecha"])
        bob = 10 * math.sin((t - t0) * 9)
        ang = math.atan2(ty - ly, tx - lx)
        sx, sy = lx + math.cos(ang) * (p.height * 0.7), ly + math.sin(ang) * (p.height * 0.7)
        ex, ey = tx - math.cos(ang) * (30 + bob), ty - math.sin(ang) * (30 + bob)
        grow = ease((t - t0 - 0.1) / 0.3)
        ex, ey = sx + (ex - sx) * grow, sy + (ey - sy) * grow
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        flecha(ImageDraw.Draw(ov), sx, sy, ex, ey)
        fr.alpha_composite(ov)
        pegar(fr, p, lx, ly, escala=0.5 + 0.5 * kk, alpha=min(1, kk * 2))   # la pastilla queda por encima


def subtitulos(fr, palabras, t, clave):
    """1-2 palabras grandes, centradas, con contorno negro; la palabra clave en color."""
    grupos, g = [], []
    for w in palabras:
        g.append(w)
        if len(g) == 2 or w["w"][-1] in ".,?!" or len(w["w"]) > 9:
            grupos.append(g); g = []
    if g:
        grupos.append(g)
    for g in grupos:
        if g[0]["s"] - 0.05 <= t < g[-1]["e"] + 0.12:
            x_total, piezas = 0, []
            for w in g:
                limpio = w["w"].strip(".,?!\"“”").upper()
                es_clave = any(limpio.startswith(k.upper()) for k in clave)
                im = texto_img(limpio, "Montserrat-Black.ttf", 128 if es_clave else 112, "amarillo" if es_clave else "blanco", stroke=11 if es_clave else 10)
                piezas.append(im); x_total += im.width - 30
            k = ease_back((t - g[0]["s"] + 0.05) / 0.16)
            ajuste = min(1.0, 940 / max(x_total, 1))          # si no cabe a lo ancho, se encoge
            x = W / 2 - x_total * ajuste / 2
            for im in piezas:
                pegar(fr, im, x + im.width * ajuste / 2, 1300, escala=(0.82 + 0.18 * k) * ajuste)
                x += (im.width - 30) * ajuste
            return


def marca(fr, txt, fuente):
    im = texto_img(txt, "Montserrat-Black.ttf", 34, "blanco", stroke=0)
    glow = texto_img(txt, "Montserrat-Black.ttf", 34, "morado", stroke=6, stroke_col="morado", shadow=False).filter(ImageFilter.GaussianBlur(6))
    pegar(fr, glow, SAFE_RIGHT - im.width / 2 + 10, SAFE_TOP - 50, alpha=0.9)
    pegar(fr, im, SAFE_RIGHT - im.width / 2 + 10, SAFE_TOP - 50)
    if fuente:   # por defecto NO se pinta (decisión de Adam, 19/11/2026): las fuentes y el crédito van en la descripción
        s = texto_img(fuente, "Montserrat-ExtraBold.ttf", 30, "blanco", shadow=True)
        pegar(fr, s, 60 + s.width / 2, SAFE_BOTTOM - 10, alpha=0.85)


# ------------------------------------------------------------------ música propia (sin derechos de terceros)
def ritmo(segundos: float, bpm: int, salida: Path, sr: int = 44100) -> None:
    n = int(segundos * sr)
    t = np.arange(n) / sr
    beat = 60 / bpm
    out = np.zeros(n)
    rng = np.random.default_rng(7)
    for b in np.arange(0, segundos, beat):          # bombo a negras
        i = int(b * sr); L = int(0.35 * sr); tt = np.arange(min(L, n - i)) / sr
        out[i:i + len(tt)] += np.sin(2 * np.pi * (48 + 110 * np.exp(-tt * 28)) * tt) * np.exp(-tt * 9) * 0.9
    for b in np.arange(beat / 2, segundos, beat):   # charles a contratiempo
        i = int(b * sr); L = int(0.06 * sr); seg = rng.standard_normal(min(L, n - i))
        out[i:i + len(seg)] += np.diff(np.concatenate([[0], seg])) * np.exp(-np.arange(len(seg)) / sr * 60) * 0.18
    for b in np.arange(beat, segundos, beat * 2):   # palmada en 2 y 4
        i = int(b * sr); L = int(0.18 * sr); seg = rng.standard_normal(min(L, n - i))
        out[i:i + len(seg)] += seg * np.exp(-np.arange(len(seg)) / sr * 22) * 0.22
    notas = [45, 45, 48, 43]                         # bajo sincopado (La menor)
    for j, b in enumerate(np.arange(0, segundos, beat / 2)):
        if j % 4 == 1:
            continue
        f = 440 * 2 ** ((notas[(j // 8) % 4] - 69) / 12)
        i = int(b * sr); L = int(beat / 2 * sr * 0.9); tt = np.arange(min(L, n - i)) / sr
        saw = 2 * ((tt * f) % 1) - 1
        out[i:i + len(tt)] += np.tanh(saw * 2.5) * np.exp(-tt * 6) * 0.22
    pad = sum(np.sin(2 * np.pi * 440 * 2 ** ((m - 69) / 12) * t) for m in (57, 60, 64)) * 0.03 * (0.6 + 0.4 * np.sin(2 * np.pi * t / (beat * 8)))
    out += pad
    out /= np.max(np.abs(out)) * 1.05
    estereo = np.stack([out, out], 1)
    estereo = (estereo * 32767).astype(np.int16)
    import wave
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(estereo.tobytes())


# ------------------------------------------------------------------ modo show: efectos de sonido propios (sin derechos de terceros)
def _env(L, sr, ataque=0.01):
    t = np.arange(L) / sr
    return t, np.minimum(1, t / max(ataque, 1e-4))


def _lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same") if k > 1 else x


def sfx_whoosh(sr):
    L = int(0.38 * sr); t, _ = _env(L, sr)
    rng = np.random.default_rng(1)
    ruido = _lp(rng.standard_normal(L), 6) - _lp(rng.standard_normal(L), 60) * 0.5
    env = np.sin(np.pi * np.clip(t / 0.38, 0, 1)) ** 2
    return ruido * env * 0.55


def sfx_golpe(sr):
    L = int(0.7 * sr); t, a = _env(L, sr, 0.003)
    bombo = np.sin(2 * np.pi * (40 + 120 * np.exp(-t * 18)) * t) * np.exp(-t * 5.5)
    rng = np.random.default_rng(2)
    chas = _lp(rng.standard_normal(L), 3) * np.exp(-t * 30) * 0.5
    return np.tanh((bombo + chas) * 1.6) * a * 0.9


def sfx_pop(sr):
    L = int(0.08 * sr); t, a = _env(L, sr, 0.002)
    f = 950 - 5000 * t
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 45) * a * 0.45


def sfx_ding(sr):
    L = int(0.5 * sr); t, a = _env(L, sr, 0.002)
    return (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2352 * t)) * np.exp(-t * 9) * a * 0.32


def sfx_subida(sr, dur=0.9):
    L = int(dur * sr); t, _ = _env(L, sr)
    rng = np.random.default_rng(3)
    ruido = _lp(rng.standard_normal(L), 4)
    tono = np.sin(2 * np.pi * np.cumsum(300 + 900 * (t / dur) ** 2) / sr)
    return (ruido * 0.35 + tono * 0.25) * (t / dur) ** 2


def pista_sfx(dur, eventos, salida, sr=44100):
    """eventos: lista de (segundo, tipo). Escribe un wav estéreo con todos los efectos."""
    n = int((dur + 1) * sr)
    out = np.zeros(n)
    banco = {"whoosh": sfx_whoosh(sr), "golpe": sfx_golpe(sr), "pop": sfx_pop(sr), "ding": sfx_ding(sr), "subida": sfx_subida(sr)}
    for seg, tipo in eventos:
        x = banco[tipo]
        i = int(max(0, seg) * sr)
        if tipo == "subida":
            i = int(max(0, seg - len(x) / sr) * sr)   # la subida TERMINA en el momento indicado
        j = min(n, i + len(x))
        out[i:j] += x[: j - i]
    out = np.tanh(out * 1.2) / 1.2
    est = (np.stack([out, out], 1) * 32767 * 0.9).astype(np.int16)
    import wave
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(est.tobytes())


def pausa_dramatica(wav: Path, t_reveal: float, sr=44100, hueco=0.45):
    """Silencia la música justo antes del dato fuerte (la voz sigue) para que el golpe se note."""
    import wave
    with wave.open(str(wav), "rb") as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float64)
    i0, i1 = int(max(0, t_reveal - hueco) * sr), int(t_reveal * sr)
    data[i0:i1] = 0
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data.astype(np.int16).tobytes())


def eventos_show(plan, palabras, cortes):
    """Qué sonido va en cada momento y dónde dar golpes de cámara."""
    clave = [k.upper() for k in plan.get("palabras_clave", [])]
    ev, golpes, zooms = [], [], []
    for c in cortes:
        ev.append((c - 0.12, "whoosh"))
    for c in plan.get("capas", []):
        if c["tipo"] in ("titulo", "fact", "cta", "tarjeta", "comparativa"):
            ev.append((c["desde"], "golpe")); golpes.append(c["desde"])
        if c["tipo"] == "pastillas":
            for it in c.get("items", []):
                ev.append((it.get("desde", c["desde"]), "ding"))
    facts = [c for c in plan.get("capas", []) if c["tipo"] == "fact"]
    if facts:
        ev.append((facts[-1]["desde"], "subida"))       # tensión antes del último dato
    vistos = 0
    for w in palabras:
        limpio = w["w"].strip(".,?!\"“”:").upper()
        if any(limpio.startswith(k) for k in clave) and w["s"] - vistos > 0.6:
            ev.append((w["s"], "pop")); zooms.append(w["s"]); vistos = w["s"]
    return ev, golpes, zooms, (facts[-1]["desde"] if facts else None)


def efecto_camara(fr: Image.Image, t: float, golpes, zooms) -> Image.Image:
    """Zoom de golpe en las palabras clave y sacudida al revelar cada dato."""
    p, dx, dy = 0.0, 0.0, 0.0
    for z in zooms:
        a = (t - z) / 0.28
        if 0 <= a < 1:
            p = max(p, 0.07 * (1 - a) ** 2)
    for g in golpes:
        a = (t - g) / 0.32
        if 0 <= a < 1:
            k = (1 - a) ** 2
            rng = np.random.default_rng(int(t * 1000))
            dx += rng.uniform(-1, 1) * 22 * k; dy += rng.uniform(-1, 1) * 22 * k
            p = max(p, 0.05 * k)
    if p == 0 and dx == 0 and dy == 0:
        return fr
    s = 1 + p + (abs(dx) + abs(dy)) / W
    nw, nh = int(W * s), int(H * s)
    big = fr.resize((nw, nh), Image.BILINEAR)
    x0 = int((nw - W) / 2 + dx); y0 = int((nh - H) / 2 + dy)
    x0 = min(max(0, x0), nw - W); y0 = min(max(0, y0), nh - H)
    return big.crop((x0, y0, x0 + W, y0 + H))


# ------------------------------------------------------------------ render
def montar(plan_path: str) -> Path:
    plan_path = Path(plan_path)
    base = plan_path.parent
    plan = json.loads(plan_path.read_text())
    palabras = json.loads((base / plan["palabras"]).read_text())
    voz = base / plan["voz"]
    dur_voz = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(voz)], capture_output=True, text=True).stdout)
    dur = plan.get("duracion") or round(dur_voz + 0.8, 2)
    if plan.get("show", True) and plan.get("microcortes", True):   # ritmo: ninguna foto fija más de ~2 s sin cambio de plano
        nuevas = []
        for e in plan["escenas"]:
            largo = e["hasta"] - e["desde"]
            if "img" in e and 2.0 < largo and e["hasta"] < 90:
                m = round(e["desde"] + largo / 2, 2)
                z = e.get("zoom", [1.05, 1.15]); f = e.get("foco_fin", e.get("foco", [0.5, 0.5]))
                a1 = dict(e, hasta=m)
                a2 = dict(e, desde=m, foco=f, foco_fin=f, zoom=[z[-1] + 0.12, z[-1] + 0.2])
                a2.pop("etiqueta", None)
                nuevas += [a1, a2]
            else:
                nuevas.append(e)
        plan["escenas"] = nuevas
    escenas = [nueva_escena(e, base) for e in plan["escenas"]]
    for c in plan.get("capas", []):           # la comparativa lleva su propia foto con Ken Burns
        if c["tipo"] == "comparativa":
            c["_escena"] = Escena({"img": c["img"], "desde": c["desde"], "hasta": c["hasta"], "foco": c.get("foco", [0.5, 0.5]),
                                   "foco_fin": c.get("foco_fin", c.get("foco", [0.5, 0.5])), "zoom": c.get("zoom", [1.0, 1.1])}, base)
    escenas[-1].t1 = max(escenas[-1].t1, dur)
    cortes = [e.t0 for e in escenas[1:]]
    show = plan.get("show", True)           # modo show (Adam, 21/11/2026): efectos de sonido, zooms de golpe y sacudidas
    eventos, golpes, zooms, t_reveal = eventos_show(plan, palabras, cortes) if show else ([], [], [], None)
    salida_mudo = base / "render_mudo.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(salida_mudo)], stdin=subprocess.PIPE)
    total = int(dur * FPS)
    for fi in range(total):
        t = fi / FPS
        esc = next((e for e in escenas if e.t0 <= t < e.t1), escenas[-1])
        fr = esc.render(t)
        if show:
            fr = efecto_camara(fr, t, golpes, zooms)
        fr.alpha_composite(degradados())
        for c in plan.get("capas", []):
            if c["desde"] <= t < c["hasta"]:
                CAPAS[c["tipo"]](fr, c, t)
        etiqueta_escena(fr, esc, t)
        subtitulos(fr, palabras, t, plan.get("palabras_clave", []))
        marca(fr, plan.get("marca", "VICECITY DAYS TV"), plan.get("fuente") if plan.get("mostrar_fuente") else None)
        for c0 in cortes:                     # destello blanco en cada corte
            if 0 <= t - c0 < 0.14:
                a = 1 - (t - c0) / 0.14
                fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(170 * a))))
        ff.stdin.write(fr.convert("RGB").tobytes())
        if fi % 90 == 0:
            print(f"  fotograma {fi}/{total}", flush=True)
    ff.stdin.close(); ff.wait()
    for e in escenas:
        if hasattr(e, "cerrar"):
            e.cerrar()

    musica = base / "ritmo.wav"
    ritmo(dur, plan.get("musica", {}).get("bpm", 128), musica)
    vol = plan.get("musica", {}).get("volumen", 0.32)
    final = base / plan.get("salida", "final.mp4")
    sfx = base / "sfx.wav"
    if show and t_reveal:
        pausa_dramatica(musica, t_reveal)
    pista_sfx(dur, eventos, sfx)
    vsfx = plan.get("efectos", {}).get("volumen", 0.35) if show else 0
    filtro = (f"[1:a]aresample=44100,aformat=channel_layouts=stereo,asplit=2[v1][v2];"
              f"[2:a]volume={vol}[m];[m][v1]sidechaincompress=threshold=0.04:ratio=9:attack=8:release=300[mc];"
              f"[3:a]volume={vsfx}[fx];"
              f"[v2][mc][fx]amix=inputs=3:duration=longest:normalize=0,apad,atrim=0:{dur},loudnorm=I=-14:TP=-1.0:LRA=9[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(salida_mudo), "-i", str(voz), "-i", str(musica), "-i", str(sfx), "-filter_complex", filtro,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(final)], check=True)
    salida_mudo.unlink()
    print("Listo:", final)
    return final


if __name__ == "__main__":
    montar(sys.argv[1])
