from pathlib import Path
import re
import sys

# --------------------------------------------------
# Chapter selection
# --------------------------------------------------

if len(sys.argv) != 2:
    print("Usage: python clean_candidates.py <chapter_number>")
    print("Example: python clean_candidates.py 3")
    sys.exit(1)

chapter = int(sys.argv[1])

if not 1 <= chapter <= 12:
    print("Chapter number must be between 1 and 12.")
    sys.exit(1)

chapter_name = f"Kapitel_{chapter:02d}"

INPUT_FILE = Path(f"{chapter_name}_vocab_candidates.txt")
OUTPUT_FILE = Path(f"{chapter_name}_vocab_cleaned.txt")

if not INPUT_FILE.exists():
    print(f"ERROR: File not found: {INPUT_FILE}")
    sys.exit(1)

# --------------------------------------------------
# Obvious OCR / extraction garbage
# --------------------------------------------------

IGNORE_EXACT = {
    "page", "pages", "pdf", "kapitel", "seite",
}

# --------------------------------------------------
# Read candidates
# --------------------------------------------------

words = INPUT_FILE.read_text(encoding="utf-8").splitlines()

cleaned = set()
removed = []

for word in words:
    word = word.strip().lower()

    if not word:
        continue

    # Only German-looking words
    if not re.fullmatch(
        r"[a-zäöüß]+(?:-[a-zäöüß]+)*",
        word
    ):
        removed.append(word)
        continue

    # Obvious non-vocabulary items
    if word in IGNORE_EXACT:
        removed.append(word)
        continue

    # Reject suspicious strings with no vowels.
    # This catches many OCR artifacts such as:
    # "zzzzos", "sietmn", "ljlaqzla"
    if not re.search(r"[aeiouyäöü]", word):
        removed.append(word)
        continue

    # Extremely long words are allowed in German,
    # but absurd OCR strings are usually suspicious.
    if len(word) > 35:
        removed.append(word)
        continue

    cleaned.add(word)

# --------------------------------------------------
# Sort
# --------------------------------------------------

cleaned = sorted(cleaned)

# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_FILE.write_text(
    "\n".join(cleaned) + "\n",
    encoding="utf-8"
)

print(f"Chapter: {chapter}")
print(f"Input:   {len(words)}")
print(f"Cleaned: {len(cleaned)}")
print(f"Removed: {len(words) - len(cleaned)}")
print(f"Saved:   {OUTPUT_FILE}")