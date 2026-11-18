"""Prueba de extremo a extremo en modo dry-run (sin APIs, requiere ffmpeg)."""

import shutil
import subprocess
from pathlib import Path

import pytest

from gta6_studio.agents.publisher import build_body
from gta6_studio.config import load_settings
from gta6_studio.media import duration
from gta6_studio.models import Script, SeoPackage
from gta6_studio.orchestrator import Producer

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg no instalado")


@pytest.fixture
def settings(tmp_path):
    s = load_settings(dry_run=True)
    s.root = tmp_path
    for d in ("assets/footage", "assets/music", "assets/ai_clips"):
        (tmp_path / d).mkdir(parents=True)
    return s


def test_short_end_to_end_with_gameplay(settings, tmp_path):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=30",
                    "-t", "20", str(tmp_path / "assets/footage/vice_city_drone.mp4")], check=True)
    producer = Producer(settings)
    state = producer.produce(producer.new_run("short"))

    final = Path(state.get("edit")["video"])
    assert final.exists() and duration(final) > 10
    assert Path(state.get("thumbnail")).exists()
    assert {p["kind"] for p in state.get("visuals")} == {"own_gameplay"}
    assert state.get("publish")["skipped"] is True
    assert (state.dir / "ai_prompts.json").exists()
    assert (state.dir / "guion.md").exists()


def test_ai_clips_take_priority_and_render_resumes(settings, tmp_path):
    producer = Producer(settings)
    state = producer.produce(producer.new_run("short"), stop_after="script")
    assert not state.done("voice")

    clip_dir = tmp_path / "assets/ai_clips" / state.run_id
    clip_dir.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc=size=720x1280:rate=30",
                    "-t", "5", str(clip_dir / "scene_00.mp4")], check=True)
    producer.produce(producer.open_run(state.run_id))
    kinds = [p["kind"] for p in producer.open_run(state.run_id).get("visuals")]
    assert kinds[0] == "ai_clip" and kinds[1] == "title_card"


def test_upload_body_declares_synthetic_media(settings):
    from gta6_studio.agents.seo import _mock
    from gta6_studio.agents.scriptwriter import _mock as script_mock
    from gta6_studio.agents.strategist import _mock as idea_mock

    script: Script = script_mock(idea_mock("short").ideas[0], 3)
    seo: SeoPackage = _mock(script)
    body = build_body(settings, seo, synthetic=True)
    assert body["status"]["containsSyntheticMedia"] is True
    assert body["status"]["privacyStatus"] == "private"  # require_approval por defecto
    assert body["snippet"]["categoryId"] == "20"
