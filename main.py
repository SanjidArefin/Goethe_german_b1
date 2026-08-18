import fitz

pdf_path = r"D:\coding\german_b1\Goethe_german_b1\Netzwerk B1 Neu.pdf"

pdf = fitz.open(pdf_path)

print("Total pages:", len(pdf))

for page_number, page in enumerate(pdf, start=1):
    text = page.get_text().strip()
    images = page.get_images(full=True)

    print(
        f"Page {page_number}: "
        f"{len(text)} text characters, "
        f"{len(images)} images"
    )

pdf.close()