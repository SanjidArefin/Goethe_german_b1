from pathlib import Path
import sqlite3
import sys

# --------------------------------------------------
# Chapter selection
# --------------------------------------------------

if len(sys.argv) != 2:
    print("Usage: python flag_suspicious.py <chapter_number>")
    sys.exit(1)

chapter = int(sys.argv[1])

if not 1 <= chapter <= 12:
    print("Chapter number must be between 1 and 12.")
    sys.exit(1)

chapter_name = f"Kapitel_{chapter:02d}"

INPUT_FILE = Path(f"{chapter_name}_vocab_cleaned.txt")
OUTPUT_FILE = Path(f"{chapter_name}_vocab_suspicious.txt")
DB_FILE = Path("dictionary-de.db")

if not INPUT_FILE.exists():
    print(f"ERROR: Missing {INPUT_FILE}")
    sys.exit(1)

if not DB_FILE.exists():
    print(f"ERROR: Missing {DB_FILE}")
    sys.exit(1)

# --------------------------------------------------
# Load vocabulary
# --------------------------------------------------

words = {
    line.strip().lower()
    for line in INPUT_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip()
}

# --------------------------------------------------
# Connect to dictionary
# --------------------------------------------------

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# --------------------------------------------------
# Load dictionary headwords
# --------------------------------------------------

entry_words = {
    row[0].lower()
    for row in cursor.execute(
        "SELECT word FROM entries"
    )
    if row[0]
}

# --------------------------------------------------
# Load inflected forms
# --------------------------------------------------

inflected_words = {
    row[0].lower()
    for row in cursor.execute(
        "SELECT inflected_form FROM inflections"
    )
    if row[0]
}

# --------------------------------------------------
# Check words
# --------------------------------------------------

known = words & (entry_words | inflected_words)
suspicious = sorted(words - known)

# --------------------------------------------------
# Save suspicious words
# --------------------------------------------------

OUTPUT_FILE.write_text(
    "\n".join(suspicious) + ("\n" if suspicious else ""),
    encoding="utf-8"
)

conn.close()

# --------------------------------------------------
# Report
# --------------------------------------------------

print(f"Chapter:     {chapter}")
print(f"Input:       {len(words)}")
print(f"Recognized:  {len(known)}")
print(f"Suspicious:  {len(suspicious)}")
print(f"Saved:       {OUTPUT_FILE}")