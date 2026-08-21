from pathlib import Path
import sqlite3
import sys
import re

# --------------------------------------------------
# Chapter selection
# --------------------------------------------------

if len(sys.argv) != 2:
    print("Usage: python classify_vocab.py <chapter_number>")
    sys.exit(1)

chapter = int(sys.argv[1])

if not 1 <= chapter <= 12:
    print("Chapter number must be between 1 and 12.")
    sys.exit(1)

name = f"Kapitel_{chapter:02d}"

INPUT = Path(f"{name}_vocab_cleaned.txt")
OUTPUT = Path(f"{name}_vocab_classified.txt")
DB = Path("dictionary-de.db")

# --------------------------------------------------
# Load dictionary
# --------------------------------------------------

conn = sqlite3.connect(DB)
cur = conn.cursor()

entries = {
    row[0].lower()
    for row in cur.execute("SELECT word FROM entries")
    if row[0]
}

inflections = {
    row[0].lower()
    for row in cur.execute("SELECT inflected_form FROM inflections")
    if row[0]
}

conn.close()

dictionary = entries | inflections

# --------------------------------------------------
# Known non-OCR patterns
# --------------------------------------------------

def looks_like_valid_compound(word):
    """
    Don't flag words that look like normal German compounds.
    """

    # Hyphenated words
    if "-" in word:
        return True

    # Long German words are often compounds.
    if len(word) >= 12:
        return True

    # Common compound endings
    endings = (
        "urlaub",
        "wohnung",
        "planung",
        "ziele",
        "reise",
        "band",
        "raum",
        "nummer",
        "promenade",
        "geschichte",
        "planung",
        "typ",
        "ferien",
        "hotel",
        "arbeit",
        "mitarbeiter",
        "partner",
        "plätze",
        "platz",
    )

    if any(word.endswith(x) for x in endings):
        return True

    return False


# --------------------------------------------------
# OCR suspicion
# --------------------------------------------------

def likely_ocr(word):
    # Obvious repeated character
    if re.search(r"(.)\1\1", word):
        return True

    # Extremely strange vowel pattern
    vowels = sum(c in "aeiouyäöü" for c in word)

    if len(word) >= 6 and vowels == 0:
        return True

    # Obvious OCR-looking fragments
    suspicious_fragments = (
        "chml",
        "mwelch",
        "iich",
        "wöär",
        "vergesscn",
    )

    if any(x in word for x in suspicious_fragments):
        return True

    return False


# --------------------------------------------------
# Classify
# --------------------------------------------------

words = sorted(
    set(
        line.strip().lower()
        for line in INPUT.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
)

known = []
review = []
ocr = []

for word in words:

    if word in dictionary:
        known.append(word)

    elif likely_ocr(word):
        ocr.append(word)

    elif looks_like_valid_compound(word):
        review.append(word)

    else:
        review.append(word)

# --------------------------------------------------
# Output
# --------------------------------------------------

with OUTPUT.open("w", encoding="utf-8") as f:

    f.write("===== KNOWN / DICTIONARY =====\n")
    for word in known:
        f.write(word + "\n")

    f.write("\n===== REVIEW / POSSIBLY VALID =====\n")
    for word in review:
        f.write(word + "\n")

    f.write("\n===== LIKELY OCR =====\n")
    for word in ocr:
        f.write(word + "\n")

print(f"Chapter: {chapter}")
print(f"Total:   {len(words)}")
print(f"Known:   {len(known)}")
print(f"Review:  {len(review)}")
print(f"OCR:     {len(ocr)}")
print(f"Saved:   {OUTPUT}")