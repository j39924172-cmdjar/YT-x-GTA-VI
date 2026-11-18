"""Productor ejecutivo: coordina al equipo de principio a fin y guarda el estado de cada paso."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from .agents import (analytics, compliance, editor, publisher, scriptwriter, seo, strategist,
                     thumbnail, trend_scout, visuals, voice)
from .config import Settings
from .llm import Brain
from .models import ComplianceReport, Script, SeoPackage, TrendReport, VideoIdea
from .state import RunState

log = logging.getLogger(__name__)

STEPS = ["trends", "idea", "script", "voice", "visuals", "edit", "seo", "thumbnail", "compliance", "publish"]
RENDER_STEPS = ["visuals", "edit", "seo", "thumbnail", "compliance", "publish"]


class Producer:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.brain = Brain(settings)

    def new_run(self, fmt: str) -> RunState:
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{fmt}"
        state = RunState(self.settings.runs_dir / run_id)
        state.set_meta(format=fmt, dry_run=self.settings.dry_run)
        return state

    def open_run(self, run_id: str) -> RunState:
        path = self.settings.runs_dir / run_id
        if not (path / "state.json").exists():
            raise FileNotFoundError(f"No existe la producción {run_id}")
        return RunState(path)

    # ------------------------------------------------------------------
    def produce(self, state: RunState, topic: str | None = None, stop_after: str | None = None,
                redo: list[str] | None = None) -> RunState:
        s, fmt = self.settings, state.data["format"]
        for step in redo or []:
            state.data["steps"].pop(step, None)
        history = analytics.summary(s)

        def step(name: str, fn):
            if state.done(name):
                log.info("✓ %s (en caché)", name)
                return state.get(name)
            log.info("▶ %s", name)
            value = fn()
            state.save(name, value)
            return value

        def stop(name: str) -> bool:
            if stop_after == name:
                log.info("Pausa tras '%s'. Continúa con: python -m gta6_studio resume %s", name, state.run_id)
                return True
            return False

        trends = TrendReport.model_validate(step("trends", lambda: trend_scout.run(s, self.brain, history).model_dump()))
        idea = VideoIdea.model_validate(step("idea", lambda: strategist.run(s, self.brain, trends, fmt, history, topic).model_dump()))
        script = Script.model_validate(step("script", lambda: scriptwriter.run(s, self.brain, idea, fmt).model_dump()))
        visuals.export_ai_prompts(s, script, fmt, state.run_id, state.dir / "ai_prompts.json")
        (state.dir / "guion.md").write_text(_script_md(script), encoding="utf-8")
        if stop("script"):
            return state

        voice_out = step("voice", lambda: voice.run(s, script, state.dir / "audio"))
        plan = step("visuals", lambda: visuals.run(s, script, fmt, state.run_id, state.dir / "visuals"))
        edit = step("edit", lambda: editor.run(s, script, fmt, voice_out, plan, state.dir))
        seo_pkg = SeoPackage.model_validate(
            step("seo", lambda: seo.run(s, self.brain, script, fmt, edit["scene_starts"]).model_dump()))
        thumb = step("thumbnail", lambda: str(thumbnail.run(
            seo_pkg.thumbnail, plan, state.dir, ai_bg=s.path(s["visuals"]["ai_clips_dir"]) / state.run_id / "thumbnail.png")))
        sources = {p["index"]: p["kind"] for p in plan}
        report = ComplianceReport.model_validate(
            step("compliance", lambda: compliance.run(s, self.brain, script, seo_pkg, sources).model_dump()))
        (state.dir / "metadata.md").write_text(_metadata_md(seo_pkg, report), encoding="utf-8")
        if stop("compliance"):
            return state

        if not report.approved:
            log.warning("⛔ Cumplimiento ha bloqueado la publicación. Revisa %s", state.dir / "metadata.md")
            return state
        uses_ai = report.synthetic_media_disclosure_needed or "ai_clip" in sources.values()
        body = publisher.build_body(s, seo_pkg, synthetic=uses_ai)
        if not s["publishing"]["enabled"] or s.dry_run:
            log.info("Publicación desactivada. Vídeo listo en %s", edit["video"])
            state.save("publish", {"skipped": True, "body": body})
            return state

        def _publish():
            vid = publisher.upload(s, Path(edit["video"]), Path(thumb), body)
            analytics.record(s, {"run_id": state.run_id, "video_id": vid, "title": seo_pkg.title,
                                 "format": fmt, "pillar": idea.pillar})
            return {"video_id": vid, "url": f"https://youtu.be/{vid}", "privacy": body["status"]["privacyStatus"]}

        result = step("publish", _publish)
        log.info("✅ Subido: %s (%s)", result.get("url"), result.get("privacy"))
        return state


def _script_md(script: Script) -> str:
    out = [f"# {script.title}\n", f"**Gancho:** {script.hook}\n"]
    for sc in script.scenes:
        out.append(f"## Escena {sc.index} — {sc.on_screen_text}\n\n{sc.narration}\n\n"
                   f"- Visual: {sc.visual_description}\n- Cámara: {sc.camera}\n- Prompt IA: `{sc.ai_video_prompt}`\n")
    out.append(f"**CTA:** {script.call_to_action}\n\n**Fuentes:** {script.sources_note}\n")
    return "\n".join(out)


def _metadata_md(seo_pkg: SeoPackage, report: ComplianceReport) -> str:
    issues = "\n".join(f"- [{i.severity}] {i.area}: {i.detail} → {i.fix}" for i in report.issues) or "- Ninguno"
    return (f"# {seo_pkg.title}\n\n## Descripción\n\n{seo_pkg.description}\n\n## Etiquetas\n\n{', '.join(seo_pkg.tags)}\n\n"
            f"## Hashtags\n\n{' '.join(seo_pkg.hashtags)}\n\n## Capítulos\n\n" + "\n".join(seo_pkg.chapters) +
            f"\n\n## Miniatura\n\n- Texto: {seo_pkg.thumbnail.headline}\n- Prompt fondo: `{seo_pkg.thumbnail.image_prompt}`\n\n"
            f"## Cumplimiento\n\nAprobado: {'sí' if report.approved else 'NO'}\n"
            f"Declarar contenido sintético: {'sí' if report.synthetic_media_disclosure_needed else 'no'}\n\n{issues}\n")
