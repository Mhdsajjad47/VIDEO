"""Script generation agent powered by Hugging Face GPT-2."""

from __future__ import annotations

from pathlib import Path

from transformers import pipeline


class ScriptAgent:
    """Generate educational short-form scripts with GPT-2."""

    def __init__(self, output_dir: str | Path = "outputs/scripts") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generator = pipeline("text-generation", model="gpt2")

    def generate_script(self, topic: str, max_new_tokens: int = 220) -> str:
        """Generate a ~45 second script for a topic."""
        prompt = (
            f"Create a 45-second educational video script about: {topic}. "
            "Use simple language, include 1 hook line, 3 practical points, and a closing call-to-action. "
            "Tone: encouraging, clear, and student friendly.\n\nScript:\n"
        )
        output = self.generator(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            num_return_sequences=1,
            pad_token_id=50256,
        )
        raw_text = output[0]["generated_text"]
        script = raw_text.replace(prompt, "").strip()
        return script

    def save_script(self, script_text: str, index: int, topic: str) -> Path:
        """Persist script text to outputs/scripts."""
        safe_topic = "".join(char if char.isalnum() else "_" for char in topic).strip("_").lower()
        file_path = self.output_dir / f"{index:02d}_{safe_topic}.txt"
        file_path.write_text(script_text, encoding="utf-8")
        return file_path
