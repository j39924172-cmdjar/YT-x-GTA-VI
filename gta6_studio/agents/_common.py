from __future__ import annotations

from ..config import Settings


def channel_brief(settings: Settings) -> str:
    ch = settings["channel"]
    pillars = "\n".join(f"- {p}" for p in ch["niche_pillars"])
    return (
        f"Canal de YouTube: {ch['name']}\n"
        f"Idioma de todo el contenido: {ch['language']}\n"
        f"Audiencia: {ch['audience']}\n"
        f"Tono: {ch['tone']}\n"
        f"Pilares temáticos:\n{pillars}"
    )


GROUND_RULES = """Reglas de la casa (obligatorias):
- Grand Theft Auto VI es de Rockstar Games. Nunca presentes el canal como oficial ni uses logotipos de Rockstar como propios.
- No inventes datos: si algo es rumor o filtración, dilo explícitamente. Señala qué hechos hay que verificar.
- Nada de clickbait engañoso: el título y la miniatura deben cumplirse en el vídeo.
- No reproduzcas diálogos, música ni tráileres oficiales completos. Comenta, analiza y transforma.
- Contenido apto para la política de anuncios de YouTube (sin violencia gráfica gratuita ni lenguaje extremo)."""
