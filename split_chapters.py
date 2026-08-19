from pathlib import Path
import re


# -----------------------------
# Files and folders
# -----------------------------

INPUT_FILE = Path("Netzwerk B1 Neu_clean.txt")
OUTPUT_DIR = Path("chapters")

OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Kapitel starting pages
# -----------------------------

chapter_starts = {
    1: 9,
    2: 19,
    3: 29,
    4: 45,
    5: 55,
    6: 65,
    7: 81,
    8: 91,
    9: 101,
    10: 117,
    11: 127,
    12: 137,
}


# -----------------------------
# Read OCR
# -----------------------------

text = INPUT_FILE.read_text(encoding="utf-8")


# -----------------------------
# Split into individual pages
# -----------------------------

page_pattern = re.compile(
    r"={60}\nPAGE (\d+)\n={60}\n"
)

matches = list(page_pattern.finditer(text))

pages = {}

for i, match in enumerate(matches):

    page_number = int(match.group(1))

    start = match.end()

    if i + 1 < len(matches):
        end = matches[i + 1].start()
    else:
        end = len(text)

    pages[page_number] = text[start:end].strip()


print(f"Found {len(pages)} pages.")
print()


# -----------------------------
# Create chapter ranges
# -----------------------------

chapter_numbers = list(chapter_starts.keys())

for index, chapter_number in enumerate(chapter_numbers):

    start_page = chapter_starts[chapter_number]

    # Next chapter determines the end
    if index + 1 < len(chapter_numbers):
        next_start = chapter_starts[chapter_numbers[index + 1]]
        end_page = next_start - 1
    else:
        # Main textbook content ends at page 175
        end_page = 175

    output_file = OUTPUT_DIR / f"Kapitel_{chapter_number:02d}.txt"

    with output_file.open("w", encoding="utf-8") as output:

        output.write(
            f"Kapitel {chapter_number}\n"
            f"PDF pages {start_page}-{end_page}\n"
            f"{'=' * 60}\n\n"
        )

        for page_number in range(start_page, end_page + 1):

            if page_number not in pages:
                print(
                    f"WARNING: Page {page_number} "
                    f"not found in OCR file."
                )
                continue

            output.write(
                f"\n\n{'=' * 60}\n"
                f"PAGE {page_number}\n"
                f"{'=' * 60}\n\n"
            )

            output.write(pages[page_number])
            output.write("\n")

    print(
        f"Kapitel {chapter_number:02d}: "
        f"pages {start_page}-{end_page} → "
        f"{output_file}"
    )


print()
print("Chapter splitting complete!")