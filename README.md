# 📬 ApplyBot: Automated Job Application Assistant

ApplyBot is a Python-based desktop application that automates job applications by:

✅ Scraping jobs based on your preferences  
✅ Auto-generating customized cover letters  
✅ Attaching your latest resume  
✅ Emailing recruiters directly  
✅ Logging every application you send

All from one modern, Gmail-style user interface built with `tkinter`.

---

## 🧠 Features

- 🔍 Scrapes jobs using [SerpAPI](https://serpapi.com/) and filters by title/location
- ✍️ Automatically fills in a base cover letter template with the job title and company name
- 📎 Always attaches your latest resume version (e.g., `Resume V 1.15.pdf`)
- 📤 Sends emails directly via Gmail using app password authentication
- 📓 Logs all applications to `job_applications.xlsx` to avoid duplicates

---

## 💻 Tech Stack

- Python 3
- Tkinter (for UI)
- Pandas (for CSV/Excel management)
- smtplib + email (for Gmail integration)
- dotenv (for secure credentials)
- SerpAPI (job scraping)

---
📌 Notes
Jobs already sent are automatically skipped in the UI.

Your resume is selected based on the latest Resume V X.XX.pdf in the project folder.

.env and job_applications.xlsx are hidden from GitHub for your privacy.

---
🚀 How to Run
Clone the repository:
git clone https://github.com/shannyb8255/ApplyBot.git
cd ApplyBot

Install the required Python packages:
pip install -r requirements.txt

Create a .env file in the root folder with the following:
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_PASSWORD=your-app-password
SERPAPI_KEY=your-serpapi-key

Download or prepare your latest resume as a PDF Save it in the main folder with a name like:
Resume V 1.15.pdf

Run the app:
python apply_ui.py

---
🧠 Inspiration
This project was created to streamline my own job search. I wanted to save time, stay organized, and personalize every application — with minimal manual effort.

---
📫 Contact
Have questions or want to collaborate?
Reach out to me at: shannonebreault@gmail.com

