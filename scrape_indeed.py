import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_indeed_jobs(job_keywords, desired_locations, max_results=10):
    base_url = "https://www.indeed.com/jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    all_jobs = []

    for keyword in job_keywords:
        for search_location in desired_locations:
            print(f"\n🔍 Searching for jobs with '{keyword}' in '{search_location}'...")
            params = {
                "q": keyword,
                "l": search_location,
                "limit": max_results
            }

            response = requests.get(base_url, params=params, headers=headers)
            print(f"🌐 Response status code: {response.status_code}")
            print(f"📄 Page length: {len(response.text)} characters")

            soup = BeautifulSoup(response.text, "html.parser")

            job_cards = soup.find_all("div", class_="job_seen_beacon")

            if not job_cards:
                print("⚠️  No job cards found on this page.")

            for card in job_cards:
                title_elem = card.find("h2", class_="jobTitle")
                company_elem = card.find("span", class_="companyName")
                location_elem = card.find("div", class_="companyLocation")
                link_elem = card.find("a", href=True)

                job_title = title_elem.text.strip() if title_elem else "N/A"
                company = company_elem.text.strip() if company_elem else "N/A"
                location_text = location_elem.text.strip() if location_elem else "N/A"
                link = "https://www.indeed.com" + link_elem['href'] if link_elem else "N/A"

                # Lowercase for matching
                job_title_lower = job_title.lower()
                location_lower = location_text.lower()

                # Matching logic
                title_matches = any(kw.lower() in job_title_lower for kw in job_keywords)
                location_matches = any(loc.lower() in location_lower for loc in desired_locations)

                print(f"🔎 Found: {job_title} at {company} | {location_text}")
                if title_matches and location_matches:
                    all_jobs.append({
                        "Job Title": job_title,
                        "Company": company,
                        "Location": location_text,
                        "Link": link
                    })

    df = pd.DataFrame(all_jobs)
    df.to_csv("indeed_jobs.csv", index=False)
    print(f"\n✅ Saved {len(all_jobs)} filtered jobs to 'indeed_jobs.csv'")

if __name__ == "__main__":
    job_keywords = [
        "data scientist",
    "data analyst",
    "machine learning engineer",
    "quantitative analyst",
    "actuary",
    "financial analyst",
    "investment analyst",
    "risk analyst",
    "accountant",
    "financial advisor",
    "software engineer",
    "data engineer",
    "business intelligence analyst",
    "statistical analyst",
    "operations research analyst",
    "economist",
    "machine learning researcher",
    "data science",
    "research scientist",
    "mathematical modeler",
    "AI engineer",
    "algorithm engineer",
    "quantitative researcher",
    "technical consultant",
    "bioinformatics analyst",
    "cryptographer"
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

    search_indeed_jobs(job_keywords, locations, max_results=15)
