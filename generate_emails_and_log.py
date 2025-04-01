import pandas as pd
import os
import re
import datetime

# Path setup
cover_letter_folder = "cover_letters"
resume_folder = "."  # main folder
log_file = "job_applications.xlsx"
csv_file = "serpapi_jobs.csv"

# Find the latest resume file
def get_latest_resume():
    version_pattern = r"Resume V (\d+\.\d+)\.pdf"
    highest_version = (0, 0)
    latest_resume = None

    for file in os.listdir(resume_folder):
        match = re.match(version_pattern, file)
        if match:
            major, minor = map(int, match.group(1).split("."))
            if (major, minor) > highest_version:
                highest_version = (major, minor)
                latest_resume = file
    return latest_resume

# Load cover letters and job list
df = pd.read_csv(csv_file)
applied_rows = []

latest_resume = get_latest_resume()
if not latest_resume:
    print("❌ No resume file found!")
    exit()

print(f"📎 Using resume: {latest_resume}")

for _, row in df.iterrows():
    job_title = row["Job Title"]
    company = row["Company"]
    location = row["Location"]
    link = row.get("Link", "N/A")

    # Format file name
    filename = re.sub(r"[\\/:*?\"<>|]", "", f"{company} - {job_title}") + ".pdf"
    cover_path = os.path.join(cover_letter_folder, filename)

    if not os.path.exists(cover_path):
        print(f"⚠️ Skipping {job_title} at {company} — cover letter not found.")
        continue

    # Email draft output
    print("\n" + "="*60)
    print(f"📨 Subject: Application for {job_title} at {company}")
    print("📎 Attachments:")
    print(f"   - {latest_resume}")
    print(f"   - {filename}")
    print("\n📄 Email Body:\n")

    with open(os.path.join(cover_letter_folder, filename.replace(".pdf", ".txt")), "r", encoding="utf-8") as f:
        print(f.read())

    print("="*60 + "\n")

    # Add to log
    applied_rows.append({
        "Job Title": job_title,
        "Company": company,
        "Location": location,
        "Link": link,
        "Resume Used": latest_resume,
        "Cover Letter": filename,
        "Date Applied": datetime.date.today().strftime("%Y-%m-%d"),
        "Recipient": "N/A",
        "Status": "Pending"
    })

# Save to Excel with correct columns
if applied_rows:
    log_df = pd.DataFrame(applied_rows, columns=[
        "Job Title", "Company", "Location", "Link",
        "Resume Used", "Cover Letter", "Date Applied",
        "Recipient", "Status"
    ])

    if os.path.exists(log_file):
        existing_log = pd.read_excel(log_file)
        combined = pd.concat([existing_log, log_df], ignore_index=True)
    else:
        combined = log_df

    combined.to_excel(log_file, index=False)
    print(f"✅ Logged {len(applied_rows)} applications to '{log_file}'")
else:
    print("⚠️ No applications were logged.")
