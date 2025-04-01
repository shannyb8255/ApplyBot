import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import smtplib
from email.message import EmailMessage
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Settings
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RESUME_DIR = "."
CSV_FILE = "serpapi_jobs.csv"
COVER_LETTER_TEMPLATE = "base_cover_letter.txt"
LOG_EXCEL = "job_applications.xlsx"

# Get the latest resume file
def get_latest_resume():
    pdfs = [f for f in os.listdir(RESUME_DIR) if f.lower().endswith(".pdf") and "resume" in f.lower()]
    versioned = sorted(pdfs, key=lambda f: os.path.getmtime(os.path.join(RESUME_DIR, f)), reverse=True)
    return versioned[0] if versioned else None

# Personalize cover letter
def personalize_letter(job_title, company):
    with open(COVER_LETTER_TEMPLATE, "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("[Job Title]", job_title).replace("[Company]", company)

# Send email
def send_email(to_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(attachment_path))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# Log application
def log_application(company, job_title, location, recipient, resume_used):
    log_data = {
        "Job Title": job_title,
        "Company": company,
        "Location": location,
        "Link": "N/A",
        "Resume Used": resume_used,
        "Cover Letter": f"{company} - {job_title}.pdf",
        "Date Applied": datetime.today().strftime("%Y-%m-%d"),
        "Recipient": recipient,
        "Status": "Pending"
    }

    df = pd.DataFrame([log_data])
    if os.path.exists(LOG_EXCEL):
        existing = pd.read_excel(LOG_EXCEL)
        combined = pd.concat([existing, df], ignore_index=True)
    else:
        combined = df

    combined.to_excel(LOG_EXCEL, index=False)

# Load job list and filter out already applied jobs
jobs_df = pd.read_csv(CSV_FILE)
if os.path.exists(LOG_EXCEL):
    applied_log = pd.read_excel(LOG_EXCEL)
    applied_pairs = set(zip(applied_log["Company"], applied_log["Job Title"]))
    jobs_df = jobs_df[~jobs_df.apply(lambda row: (row["Company"], row["Job Title"]) in applied_pairs, axis=1)].reset_index(drop=True)

job_index = 0

# UI Setup
root = tk.Tk()
root.title("ApplyBot ✉️")
root.geometry("850x720")
root.configure(bg="#f1f3f4")

font_title = ("Helvetica", 16, "bold")
font_label = ("Helvetica", 11)
font_entry = ("Helvetica", 11)
font_button = ("Helvetica", 11, "bold")

job_label = tk.Label(root, text="", font=font_title, bg="#f1f3f4", wraplength=750, justify="center")
job_label.pack(pady=10)

cover_letter_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=95, height=20, font=font_entry, bg="white", borderwidth=1, relief="solid")
cover_letter_box.pack(padx=20, pady=10)

resume_label = tk.Label(root, text="", font=("Helvetica", 10), fg="gray", bg="#f1f3f4")
resume_label.pack()

email_frame = tk.Frame(root, bg="#f1f3f4")
email_label = tk.Label(email_frame, text="Recipient Email:", font=font_label, bg="#f1f3f4")
email_label.pack(side=tk.LEFT, padx=(0, 10))
email_entry = tk.Entry(email_frame, width=60, font=font_entry)
email_entry.pack(side=tk.LEFT)
email_frame.pack(pady=5)

def update_ui():
    if job_index >= len(jobs_df):
        messagebox.showinfo("Done", "✅ All jobs processed!")
        root.quit()
        return

    job = jobs_df.iloc[job_index]
    job_title = job["Job Title"]
    company = job["Company"]
    location = job["Location"]

    job_label.config(text=f"📌 {job_title} at {company} ({location})")
    letter = personalize_letter(job_title, company)
    cover_letter_box.delete("1.0", tk.END)
    cover_letter_box.insert(tk.END, letter)
    email_entry.delete(0, tk.END)

    resume_file = get_latest_resume()
    resume_label.config(text=f"📎 Using resume: {resume_file}" if resume_file else "❌ No resume found")

def submit():
    global job_index

    job = jobs_df.iloc[job_index]
    job_title = job["Job Title"]
    company = job["Company"]
    location = job["Location"]
    recipient_email = email_entry.get().strip()
    letter = cover_letter_box.get("1.0", tk.END).strip()

    resume_file = get_latest_resume()
    if not resume_file:
        messagebox.showerror("Error", "❌ No resume PDF found!")
        return

    if recipient_email:
        try:
            send_email(recipient_email, f"Application for {job_title} at {company}", letter, resume_file)
            messagebox.showinfo("Success", f"📨 Email sent to {recipient_email}")
        except Exception as e:
            messagebox.showerror("Failed", f"❌ Failed to send email:\n{e}")
            return

    log_application(company, job_title, location, recipient_email or "N/A", resume_file)
    job_index += 1
    update_ui()

button_frame = tk.Frame(root, bg="#f1f3f4")
submit_btn = tk.Button(button_frame, text="📤 Send + Log", command=submit, bg="#1a73e8", fg="white", font=font_button, padx=20, pady=6)
submit_btn.pack(side=tk.LEFT, padx=15)
skip_btn = tk.Button(button_frame, text="➡️ Skip", command=lambda: (globals().__setitem__('job_index', job_index + 1), update_ui()), bg="#e8eaed", font=font_button)
skip_btn.pack(side=tk.LEFT)
button_frame.pack(pady=20)

update_ui()
root.mainloop()