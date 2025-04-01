import pandas as pd
import os
import re
from fpdf import FPDF

# Locations to keep
target_locations = [
    "new hampshire", "remote", "warner", "concord", "durham", "portsmouth"
]

# Load base template
with open("base_cover_letter.txt", "r", encoding="utf-8") as f:
    base_template = f.read()

# Ensure output folder exists
os.makedirs("cover_letters", exist_ok=True)

df = pd.read_csv("serpapi_jobs.csv")

filtered = 0
skipped = 0

def save_as_pdf(text, filepath):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filepath)

for _, row in df.iterrows():
    location = str(row["Location"]).lower()
    if not any(loc in location for loc in target_locations):
        continue

    job_title = row["Job Title"]
    company = row["Company"]
    loc = row["Location"]

    # Fill in the template
    personalized_letter = base_template.replace("[JOB_TITLE]", job_title)\
                                       .replace("[COMPANY_NAME]", company)\
                                       .replace("[LOCATION]", loc)

    # Clean and prepare filenames
    clean_filename = re.sub(r"[\\/:*?\"<>|]", "", f"{company} - {job_title}")
    txt_path = os.path.join("cover_letters", clean_filename + ".txt")
    pdf_path = os.path.join("cover_letters", clean_filename + ".pdf")

    if os.path.exists(txt_path) and os.path.exists(pdf_path):
        print(f"⏩ Skipped existing: {clean_filename}")
        skipped += 1
        continue

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(personalized_letter)
    save_as_pdf(personalized_letter, pdf_path)
    print(f"✅ Created: {clean_filename}")
    filtered += 1

print(f"\n✅ Generated {filtered} new letters.")
print(f"🗃️ Skipped {skipped} existing ones.")
