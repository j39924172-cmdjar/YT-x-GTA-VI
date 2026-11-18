"""Rol: Publicador. Sube el vídeo a YouTube con metadatos, miniatura y declaración de contenido sintético."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..config import Settings
from ..models import SeoPackage

log = logging.getLogger(__name__)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]


def youtube_client(settings: Settings):
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    cid, secret, refresh = (settings.env(k) for k in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"))
    if not (cid and secret and refresh):
        raise RuntimeError("Faltan credenciales de YouTube. Ejecuta: python -m gta6_studio auth-youtube --client-secret client_secret.json")
    creds = Credentials(None, refresh_token=refresh, client_id=cid, client_secret=secret,
                        token_uri="https://oauth2.googleapis.com/token", scopes=SCOPES)
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def authorize(client_secret_file: str) -> None:
    """Flujo OAuth único para obtener el refresh token de tu canal."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)
    print("\nAñade esto a tu .env (y a los secretos de GitHub si usas el workflow):\n")
    print(f"YOUTUBE_CLIENT_ID={creds.client_id}")
    print(f"YOUTUBE_CLIENT_SECRET={creds.client_secret}")
    print(f"YOUTUBE_REFRESH_TOKEN={creds.refresh_token}")


def build_body(settings: Settings, seo: SeoPackage, synthetic: bool, privacy: str | None = None) -> dict:
    cfg = settings["publishing"]
    privacy = privacy or ("private" if cfg.get("require_approval", True) else cfg["privacy"])
    description = seo.description
    if seo.chapters and seo.chapters[0].startswith("0:00"):
        description += "\n\n" + "\n".join(seo.chapters)
    if seo.hashtags:
        description += "\n\n" + " ".join(seo.hashtags)
    status = {
        "privacyStatus": privacy,
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": bool(synthetic or cfg.get("contains_synthetic_media", True)),
    }
    hours = cfg.get("schedule_hours_ahead", 0)
    if hours and privacy == "private" and not cfg.get("require_approval", True):
        status["publishAt"] = (datetime.now(timezone.utc) + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {
        "snippet": {
            "title": seo.title[:100],
            "description": description[:5000],
            "tags": seo.tags[:30],
            "categoryId": cfg.get("category_id", "20"),
            "defaultLanguage": settings["channel"]["language"],
            "defaultAudioLanguage": settings["channel"]["language"],
        },
        "status": status,
    }


def upload(settings: Settings, video: Path, thumbnail: Path, body: dict) -> str:
    from googleapiclient.http import MediaFileUpload

    yt = youtube_client(settings)
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(video), chunksize=-1, resumable=True))
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            log.info("Subida %d%%", int(status.progress() * 100))
    video_id = response["id"]
    try:
        yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(thumbnail))).execute()
    except Exception as e:  # la miniatura personalizada requiere canal verificado
        log.warning("No se pudo poner la miniatura (¿canal verificado?): %s", e)
    return video_id


def make_public(settings: Settings, video_id: str, privacy: str = "public") -> None:
    yt = youtube_client(settings)
    yt.videos().update(part="status", body={"id": video_id, "status": {"privacyStatus": privacy}}).execute()
