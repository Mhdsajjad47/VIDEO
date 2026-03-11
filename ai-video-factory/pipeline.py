"""End-to-end local AI video generation pipeline."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tqdm import tqdm

from agents.avatar_agent import AvatarAgent
from agents.script_agent import ScriptAgent
from agents.topic_agent import get_topics
from agents.voice_agent import VoiceAgent


ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "outputs" / "scripts"
AUDIO_DIR = ROOT / "outputs" / "audio"
VIDEOS_DIR = ROOT / "outputs" / "videos"


def seconds_to_timestamp(value: float) -> str:
    total_ms = int(value * 1000)
    ms = total_ms % 1000
    total_sec = total_ms // 1000
    sec = total_sec % 60
    total_min = total_sec // 60
    minute = total_min % 60
    hour = total_min // 60
    return f"{hour:02d}:{minute:02d}:{sec:02d},{ms:03d}"


def write_subtitle_file(script_text: str, subtitle_path: Path, estimated_duration: float = 45.0) -> Path:
    """Create a simple SRT subtitle file from script text."""
    words = script_text.split()
    lines = []
    words_per_line = 8
    for i in range(0, len(words), words_per_line):
        lines.append(" ".join(words[i : i + words_per_line]))

    chunk_duration = max(1.0, estimated_duration / max(1, len(lines)))
    cursor = 0.0

    with subtitle_path.open("w", encoding="utf-8") as srt:
        for idx, line in enumerate(lines, start=1):
            start = seconds_to_timestamp(cursor)
            end = seconds_to_timestamp(cursor + chunk_duration)
            srt.write(f"{idx}\n{start} --> {end}\n{line}\n\n")
            cursor += chunk_duration

    return subtitle_path


def combine_video_with_subtitles(
    avatar_video: Path,
    audio_file: Path,
    subtitle_file: Path,
    output_file: Path,
) -> None:
    """Render vertical 9:16 final short with subtitles."""
    subtitle_filter_path = subtitle_file.as_posix().replace("'", "\\'")
    vf = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"subtitles='{subtitle_filter_path}':force_style='Fontsize=14,PrimaryColour=&HFFFFFF&,"
        "OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=80'"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(avatar_video),
        "-i",
        str(audio_file),
        "-vf",
        vf,
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-shortest",
        str(output_file),
    ]
    subprocess.run(command, check=True)


def run_pipeline() -> None:
    topics = get_topics()
    target_count = min(len(topics), 30)

    print(f"Found {len(topics)} topics. Generating {target_count} videos...")

    script_agent = ScriptAgent(output_dir=SCRIPTS_DIR)
    voice_agent = VoiceAgent(output_dir=AUDIO_DIR)
    avatar_agent = AvatarAgent(output_dir=VIDEOS_DIR, avatar_dir=ROOT / "assets" / "avatars")

    failures = 0

    for idx, topic in enumerate(tqdm(topics[:target_count], desc="Video generation"), start=1):
        print(f"\n[{idx}/{target_count}] Topic: {topic}")
        try:
            print("  - Generating script...")
            script_text = script_agent.generate_script(topic)
            script_path = script_agent.save_script(script_text, idx, topic)

            print("  - Generating voice...")
            audio_path = voice_agent.text_to_speech(script_text, idx, topic)

            print("  - Animating avatar with SadTalker...")
            avatar_video_path = avatar_agent.generate_avatar_video(audio_path, idx, topic)

            print("  - Writing subtitles...")
            subtitle_path = VIDEOS_DIR / f"{idx:02d}_subtitles.srt"
            write_subtitle_file(script_text, subtitle_path, estimated_duration=45.0)

            print("  - Rendering final vertical short...")
            safe_topic = "".join(char if char.isalnum() else "_" for char in topic).strip("_").lower()
            final_path = VIDEOS_DIR / f"{idx:02d}_{safe_topic}_final_9x16.mp4"
            combine_video_with_subtitles(avatar_video_path, audio_path, subtitle_path, final_path)

            print(f"  ✓ Done: {final_path}")

        except Exception as exc:  # intentionally broad to keep the batch running
            failures += 1
            print(f"  ✗ Failed for '{topic}': {exc}")
            continue

    successes = target_count - failures
    print(f"\nPipeline completed. Success: {successes}, Failed: {failures}")


if __name__ == "__main__":
    run_pipeline()
