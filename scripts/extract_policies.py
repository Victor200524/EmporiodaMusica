# Extract the text of the store policies PDF into a Markdown file.
# Run once from the project root: python scripts/extract_policies.py

from pypdf import PdfReader

PDF_PATH = "data/store_policies.pdf"
OUTPUT_PATH = "data/policies.md"

reader = PdfReader(PDF_PATH)

# "layout" mode keeps the tables and lines like in the PDF
lines = ["# Store policies (extracted from store_policies.pdf)", ""]
for page in reader.pages:
    text = page.extract_text(extraction_mode="layout")
    for line in text.split("\n"):
        line = line.rstrip()
        # Skip repeated empty lines
        if line == "" and lines[-1] == "":
            continue
        lines.append(line)

with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
    file.write("\n".join(lines) + "\n")

print("Saved", len(reader.pages), "pages to", OUTPUT_PATH)
