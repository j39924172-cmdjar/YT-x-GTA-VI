"""Tiempos palabra a palabra: faster-whisper da los tiempos y el guion da el texto exacto."""
import difflib, json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

def tiempos(audio, guion_txt, salida, prompt=""):
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    segs, _ = m.transcribe(np.frombuffer(pcm, np.float32), word_timestamps=True, language="en", initial_prompt=prompt)
    W = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
    script = open(guion_txt).read().split()
    norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
    sm = difflib.SequenceMatcher(a=[norm(w) for w, _, _ in W], b=[norm(x) for x in script], autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out += [{"w": script[j1 + k], "s": round(W[i1 + k][1], 3), "e": round(W[i1 + k][2], 3)} for k in range(i2 - i1)]
        elif j2 > j1:   # el guion manda en el texto; los tiempos se reparten en el tramo de whisper
            s = W[i1][1] if i1 < len(W) else out[-1]["e"]
            e = W[i2 - 1][2] if i2 > i1 else s + 0.3 * (j2 - j1)
            n = j2 - j1
            out += [{"w": script[j1 + k], "s": round(s + (e - s) * k / n, 3), "e": round(s + (e - s) * (k + 1) / n, 3)} for k in range(n)]
            print("ajuste:", [w for w, _, _ in W[i1:i2]], "→", script[j1:j2])
    json.dump(out, open(salida, "w"), ensure_ascii=False, indent=0)
    print(" ".join(w for w, _, _ in W))
    print(len(out), "palabras; termina en", out[-1]["e"], "s")

if __name__ == "__main__":
    tiempos(*sys.argv[1:4], prompt=sys.argv[4] if len(sys.argv) > 4 else "")
