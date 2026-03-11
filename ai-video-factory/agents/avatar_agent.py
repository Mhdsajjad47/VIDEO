"""Avatar animation agent using SadTalker."""

from __future__ import annotations

import os
from pathlib import Path


class AvatarAgent:
    """Generate talking avatar clips from an image and audio file."""

    def __init__(
        self,
        output_dir: str | Path = "outputs/videos",
        avatar_dir: str | Path = "assets/avatars",
        sadtalker_dir: str | Path = "SadTalker",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.avatar_dir = Path(avatar_dir)
        self.sadtalker_dir = Path(sadtalker_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _choose_avatar_image(self) -> Path:
        avatars = sorted(self.avatar_dir.glob("*.png")) + sorted(self.avatar_dir.glob("*.jpg")) + sorted(
            self.avatar_dir.glob("*.jpeg")
        )
        if not avatars:
            raise FileNotFoundError(
                f"No avatar image found in {self.avatar_dir}. Add at least one .png/.jpg/.jpeg image."
            )
        return avatars[0]

    def generate_avatar_video(self, audio_path: str | Path, index: int, topic: str) -> Path:
        """Call SadTalker inference.py through os.system as requested."""
        safe_topic = "".join(char if char.isalnum() else "_" for char in topic).strip("_").lower()
        target_name = f"{index:02d}_{safe_topic}_avatar.mp4"
        final_output = self.output_dir / target_name

        source_image = self._choose_avatar_image()
        temp_output = self.output_dir / f"sadtalker_run_{index:02d}"
        temp_output.mkdir(parents=True, exist_ok=True)

        command = (
            f"python {self.sadtalker_dir / 'inference.py'} "
            f"--driven_audio \"{audio_path}\" "
            f"--source_image \"{source_image}\" "
            f"--result_dir \"{temp_output}\" "
            "--enhancer gfpgan"
        )
        exit_code = os.system(command)
        if exit_code != 0:
            raise RuntimeError(f"SadTalker failed for topic '{topic}' with exit code {exit_code}")

        mp4_files = sorted(temp_output.rglob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not mp4_files:
            raise FileNotFoundError("SadTalker did not produce an mp4 file.")

        produced_video = mp4_files[0]
        produced_video.replace(final_output)
        return final_output
