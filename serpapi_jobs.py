from serpapi import GoogleSearch
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key securely
API_KEY = os.getenv("SERPAPI_KEY")

def search_jobs(query, location, num_results=20):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "jobs_results" not in results:
        print(f"⚠️ No results found for '{query}' in '{location}'")
        return []

    jobs = []
    for job in results["jobs_results"][:num_results]:
        jobs.append({
            "Job Title": job.get("title", "N/A"),
            "Company": job.get("company_name", "N/A"),
            "Location": job.get("location", "N/A"),
            "Posted": job.get("detected_extensions", {}).get("posted_at", "N/A"),
            "Description": job.get("description", "N/A"),
            "Link": job.get("apply_options", [{}])[0].get("link", job.get("related_links", [{}])[0].get("link", "N/A"))
        })

    return jobs

if __name__ == "__main__":
    job_titles = [
        "data scientist", "data analyst", "machine learning engineer", "quantitative analyst", "actuary",
        "financial analyst", "investment analyst", "risk analyst", "accountant", "financial advisor",
        "software engineer", "data engineer", "business intelligence analyst", "statistical analyst",
        "operations research analyst", "economist", "machine learning researcher", "data science",
        "research scientist", "mathematical modeler", "AI engineer", "algorithm engineer",
        "quantitative researcher", "technical consultant", "bioinformatics analyst", "cryptographer"
    ]

    locations = [
        "New Hampshire", "Remote", "Durham, NH", "Warner, NH", "Hudson, NH", "Concord, NH", 
        "Portsmouth, NH", "New London, NH", "Merrimack, NH", "Boston, MA", "Londonderry, NH", 
        "Hampton, NH", "Nashua, NH", "Tilton, NH", "Rochester, NH", "Exeter, NH", "Belmont, NH", 
        "Salem, NH", "Ossipee, NH", "Dover, NH", "Lee, NH", "Henniker, NH", "Hopkinton, NH", 
        "Hillsborough, NH", "Weare, NH", "Franklin, NH", "Northfield, NH", "Newport, NH", 
        "Pembroke, NH", "Goffstown, NH", "Hooksett, NH", "New Boston, NH", "Laconia, NH", 
        "Gilford, NH", "Salisbury, NH", "Contoocook, NH", "Sunapee, NH", "Andover, NH", 
        "Bradford, NH", "Sutton, NH"
    ]

    all_jobs = []
    for title in job_titles:
        for loc in locations:
            print(f"🔍 Searching '{title}' in '{loc}'...")
            jobs = search_jobs(title, loc)
            all_jobs.extend(jobs)

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        df.to_csv("serpapi_jobs.csv", index=False)
        print(f"\n✅ Saved {len(all_jobs)} jobs to 'serpapi_jobs.csv'")
    else:
        print("❌ No jobs found.")
