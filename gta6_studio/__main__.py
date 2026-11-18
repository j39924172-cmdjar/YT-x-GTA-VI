"""CLI del equipo: python -m gta6_studio <comando>"""

from __future__ import annotations

import argparse
import logging
import sys

from .config import load_settings
from .llm import LLMError
from .orchestrator import RENDER_STEPS, Producer


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gta6_studio", description="Equipo automatizado de YouTube sobre GTA 6")
    p.add_argument("--config", help="Ruta a config.yaml")
    p.add_argument("--dry-run", action="store_true", help="Sin APIs: datos de ejemplo, voz muda, no publica")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Producción completa: idea → vídeo → (publicación)")
    r.add_argument("--format", choices=["short", "long"], default="short")
    r.add_argument("--topic", help="Forzar un tema concreto")
    r.add_argument("--stop-after", choices=["script", "compliance"],
                   help="Pausar tras el guion (para generar clips IA) o antes de publicar")

    rs = sub.add_parser("resume", help="Continuar una producción pausada")
    rs.add_argument("run_id")

    rd = sub.add_parser("render", help="Rehacer montaje (p.ej. tras añadir clips IA o gameplay)")
    rd.add_argument("run_id")

    ap = sub.add_parser("approve", help="Hacer público un vídeo subido en privado")
    ap.add_argument("run_id")
    ap.add_argument("--privacy", default="public", choices=["public", "unlisted"])

    sub.add_parser("stats", help="Actualizar estadísticas de los vídeos publicados")
    au = sub.add_parser("auth-youtube", help="Autorizar el canal de YouTube (una vez)")
    au.add_argument("--client-secret", required=True)

    a = p.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if a.verbose else logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")
    settings = load_settings(a.config, dry_run=a.dry_run)
    producer = Producer(settings)

    try:
        if a.cmd == "run":
            state = producer.new_run(a.format)
            producer.produce(state, topic=a.topic, stop_after=a.stop_after)
            print(f"\nProducción: {state.dir}")
        elif a.cmd == "resume":
            producer.produce(producer.open_run(a.run_id))
        elif a.cmd == "render":
            producer.produce(producer.open_run(a.run_id), redo=RENDER_STEPS)
        elif a.cmd == "approve":
            from .agents.publisher import make_public
            state = producer.open_run(a.run_id)
            pub = state.get("publish") or {}
            if not pub.get("video_id"):
                print("Esta producción no se ha subido todavía.")
                return 1
            make_public(settings, pub["video_id"], a.privacy)
            state.save("publish", {**pub, "privacy": a.privacy})
            print(f"Publicado como {a.privacy}: {pub['url']}")
        elif a.cmd == "stats":
            from .agents import analytics
            analytics.refresh_stats(settings)
            print(analytics.summary(settings))
        elif a.cmd == "auth-youtube":
            from .agents.publisher import authorize
            authorize(a.client_secret)
    except (LLMError, RuntimeError, FileNotFoundError) as e:
        logging.error("%s", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
