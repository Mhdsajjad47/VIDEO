"""Voice generation agent using Coqui TTS."""

from __future__ import annotations

from pathlib import Path

from TTS.api import TTS


class VoiceAgent:
    """Convert scripts into WAV narration."""

    def __init__(self, output_dir: str | Path = "outputs/audio") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

    def text_to_speech(self, text: str, index: int, topic: str) -> Path:
        """Generate speech WAV file from text."""
        safe_topic = "".join(char if char.isalnum() else "_" for char in topic).strip("_").lower()
        output_path = self.output_dir / f"{index:02d}_{safe_topic}.wav"
        self.tts.tts_to_file(text=text, file_path=str(output_path))
        return output_path
