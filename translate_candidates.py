from pathlib import Path
from deep_translator import GoogleTranslator
import time

INPUT_FILE = Path("Kapitel_01_vocab_candidates.txt")
OUTPUT_FILE = Path("Kapitel_01_translated.txt")

translator = GoogleTranslator(source="de", target="en")

words = [
    line.strip()
    for line in INPUT_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

print(f"Candidates: {len(words)}")
print("Starting translation...\n")

with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    for i, word in enumerate(words, start=1):
        try:
            translation = translator.translate(word).strip()

            print(f"[{i}/{len(words)}] {word} -> {translation}")

            # Keep only words that actually received a different translation.
            if translation.lower() != word.lower():
                out.write(f"{word} — {translation}\n")

        except Exception as e:
            print(f"[{i}/{len(words)}] {word} -> ERROR: {e}")

        # Small delay to avoid sending requests too quickly.
        time.sleep(0.15)

print()
print(f"Saved to: {OUTPUT_FILE}")