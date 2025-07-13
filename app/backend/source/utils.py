from collections import defaultdict
import re

def group_transcripts_by_speaker(raw_text: str) -> dict:
    speaker_map = defaultdict(list)
    pattern = re.compile(r"(?P<speaker>[\w\s]+): (?P<line>.+)")

    for line in raw_text.splitlines():
        match = pattern.match(line.strip())
        if match:
            speaker = match.group("speaker").strip()
            text = match.group("line").strip()
            speaker_map[speaker].append(text)

    return {k: "\n".join(v) for k, v in speaker_map.items()}


import os
TRANSCRIPT_FOLDER = os.path.join("app", "backend", "static", "transcripts")
def load_all_transcripts():
    transcripts = {}
    for filename in os.listdir(TRANSCRIPT_FOLDER):
        if filename.endswith(".txt"):  # or .vtt if using VTT
            path = os.path.join(TRANSCRIPT_FOLDER, filename)
            with open(path, "r", encoding="utf-8") as f:
                transcripts[filename] = f.read()
    return transcripts