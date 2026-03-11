# AI Video Factory (Local + Open Source)

This project builds a fully automated AI video generation pipeline using **free and open source tools only**:
- Topic generation (education/careers/admissions)
- Script generation with **GPT-2** (Hugging Face Transformers)
- Voice generation with **Coqui TTS**
- Talking avatar animation with **SadTalker**
- Subtitle burn-in + vertical formatting with **FFmpeg**

## Folder Structure

```text
ai-video-factory/
├── agents/
│   ├── topic_agent.py
│   ├── script_agent.py
│   ├── voice_agent.py
│   └── avatar_agent.py
├── assets/
│   ├── avatars/
│   └── background_videos/
├── outputs/
│   ├── scripts/
│   ├── audio/
│   └── videos/
├── pipeline.py
└── requirements.txt
```

## Prerequisites

1. Python 3.9+
2. FFmpeg installed and available in `PATH`
3. SadTalker cloned locally (default expected path is `ai-video-factory/SadTalker`)
4. At least one avatar image in:
   - `assets/avatars/` (`.png`, `.jpg`, or `.jpeg`)

## Setup

```bash
cd ai-video-factory
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### Install SadTalker

Clone SadTalker inside project root so `pipeline.py` can call `SadTalker/inference.py`:

```bash
git clone https://github.com/OpenTalker/SadTalker.git
```

Then install SadTalker dependencies as described in their repository.

## Run

```bash
cd ai-video-factory
python pipeline.py
```

## What happens during execution

For each topic (30 topics processed in one run):
1. `topic_agent.py` provides education/career topics.
2. `script_agent.py` generates a ~45 second script with GPT-2 and saves to `outputs/scripts/`.
3. `voice_agent.py` converts script into WAV using Coqui TTS and saves to `outputs/audio/`.
4. `avatar_agent.py` calls SadTalker `inference.py` via `os.system()` to create talking avatar video.
5. `pipeline.py` writes `.srt` subtitles and uses FFmpeg to render final **1080x1920 (9:16)** video in `outputs/videos/`.

## Notes

- First run downloads models automatically (GPT-2 + Coqui TTS model).
- The pipeline has `try/except` around each topic so failures do not stop the full batch.
- Adjust topic count by editing `target_count` in `pipeline.py`.
