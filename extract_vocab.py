from pathlib import Path
import re
import sys

# --------------------------------------------------
# Chapter selection
# --------------------------------------------------

if len(sys.argv) != 2:
    print("Usage: python extract_vocab.py <chapter_number>")
    print("Example: python extract_vocab.py 2")
    sys.exit(1)

chapter = int(sys.argv[1])

if not 1 <= chapter <= 12:
    print("Chapter number must be between 1 and 12.")
    sys.exit(1)

chapter_name = f"Kapitel_{chapter:02d}"

INPUT_FILE = Path("chapters") / f"{chapter_name}.txt"
OUTPUT_FILE = Path(f"{chapter_name}_vocab_candidates.txt")

# --------------------------------------------------
# Basic German words we don't need in the glossary
# --------------------------------------------------

STOPWORDS = {
    # Pronouns
    "ich", "du", "er", "sie", "es", "wir", "ihr", "Sie",
    "mich", "dich", "sich", "uns", "euch",
    "mein", "meine", "meinen", "meiner", "meinem", "meines",
    "dein", "deine", "deinen", "deiner", "deinem", "deines",
    "sein", "seine", "seinen", "seiner", "seinem", "seines",
    "ihr", "ihre", "ihren", "ihrer", "ihrem", "ihres",

    # Articles
    "der", "die", "das", "den", "dem", "des",
    "ein", "eine", "einen", "einem", "einer", "eines",

    # Common verbs / forms
    "ist", "sind", "bin", "bist", "seid",
    "haben", "hat", "habe", "hast", "habt",
    "werden", "wird", "wurde", "wurden",

    # Common conjunctions
    "und", "oder", "aber", "denn", "sondern",
    "weil", "dass", "wenn", "als", "ob",
    "obwohl", "damit", "also",

    # Common prepositions
    "an", "auf", "aus", "bei", "durch", "für",
    "gegen", "in", "mit", "nach", "ohne",
    "über", "um", "unter", "von", "vor", "zu",

    # Common adverbs
    "auch", "noch", "schon", "nur", "sehr",
    "so", "hier", "dort", "da", "dann",
    "jetzt", "heute", "wieder", "mehr",
    "immer", "oft", "manchmal", "nicht",

    # Question words
    "wer", "was", "wo", "wohin", "woher",
    "wann", "warum", "wie", "welche",
    "welcher", "welches", "welchen",

    # Miscellaneous
    "ja", "nein", "mal", "doch",
}

# --------------------------------------------------
# Words that are clearly not vocabulary
# --------------------------------------------------

IGNORE_EXACT = {
    "page",
    "pdf",
    "kapitel",
    "seite",
}

# --------------------------------------------------
# Check input
# --------------------------------------------------

if not INPUT_FILE.exists():
    print(f"ERROR: Input file not found: {INPUT_FILE}")
    sys.exit(1)

# --------------------------------------------------
# Read chapter
# --------------------------------------------------

text = INPUT_FILE.read_text(encoding="utf-8")

# --------------------------------------------------
# Remove page headers
# --------------------------------------------------

text = re.sub(
    r"=+\s*\*PAGE\*\s*\d+\s*=+",
    " ",
    text,
    flags=re.IGNORECASE,
)

# --------------------------------------------------
# Extract German-looking words
# Supports:
# ä ö ü Ä Ö Ü ß
# hyphenated words
# --------------------------------------------------

words = re.findall(
    r"\b[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*\b",
    text,
)

# --------------------------------------------------
# Normalize
# --------------------------------------------------

cleaned = set()

for word in words:
    word = word.strip("-")

    if not word:
        continue

    if len(word) < 3:
        continue

    normalized = word.lower()

    if normalized in STOPWORDS:
        continue

    if normalized in IGNORE_EXACT:
        continue

    if not re.search(r"[a-zäöüß]", normalized):
        continue

    cleaned.add(normalized)

# --------------------------------------------------
# Sort alphabetically
# --------------------------------------------------

vocabulary = sorted(cleaned, key=str.lower)

# --------------------------------------------------
# Write result
# --------------------------------------------------

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    for word in vocabulary:
        f.write(word + "\n")

print(f"Chapter: {chapter}")
print(f"Found {len(vocabulary)} candidate words.")
print(f"Saved to: {OUTPUT_FILE}")