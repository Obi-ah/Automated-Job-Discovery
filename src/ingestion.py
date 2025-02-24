import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

from src import config


class JobScraper:
    BASE_URL = config.BASE_URL
    PATH = "/jobs/search?q={query}&w={location}&f={days_since_posted}&page={page}"
    SEARCH_URL = BASE_URL + PATH
    print("search URL: ", SEARCH_URL)
    USER_AGENTS = config.USER_AGENTS

    def __init__(self, query, location, days_since_posted=3, max_pages=3):
        self.query = query
        self.location = location
        self.days_since_posted = days_since_posted
        self.max_pages = max_pages
        self.jobs = []

    def get_headers(self):
        return {"User-Agent": random.choice(self.USER_AGENTS)}

    def get_with_retry(self, url, max_retries=5):
        retry_delay = 2
        headers = self.get_headers()

        for attempt in range(max_retries):
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.text

            elif response.status_code == 429:
                print(f"Rate limited! Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2

            else:
                print(f"Request failed with status {response.status_code}")
                break
        return None

    def parse_job(self, job):
        title = job.find("a", class_="text-base")
        company = job.find("div", class_="ui-company")
        location = job.find("div", class_="ui-location")
        salary = job.find("div", class_="ui-salary")
        job_link_tag = job.find("a", attrs={"data-js": "jobLink"})

        salary_text = salary.text.strip() if salary else "N/A"
        salary_match = re.search(r'£[\d,]+(?:\s*-\s*£[\d,]+)?', salary_text)
        salary_clean = salary_match.group() if salary_match else "N/A"

        job_link = job_link_tag["href"] if job_link_tag else "N/A"
        if job_link.startswith("/"):
            job_link = self.BASE_URL + job_link

        return {
            "Title": title.text.strip() if title else "N/A",
            "Company": company.get_text(strip=True, separator="/").split('/')[0] if company else "N/A",
            "Location": location.text.strip().split(',')[0] if location else "N/A",
            "Salary": salary_clean,
            "Job Link": job_link
        }

    def scrape(self):
        for page in range(1, self.max_pages + 1):
            url = self.SEARCH_URL.format(
                query=self.query.replace(" ", "+"),
                location=self.location.replace(" ", "+"),
                days_since_posted=self.days_since_posted,
                page=page
            )

            html = self.get_with_retry(url)
            if not html:
                break

            # # For testing with local HTML file
            # with open("output.txt", "r") as file:
            #     html = file.read()

            soup = BeautifulSoup(html, "lxml")
            job_listings = soup.find_all("article", class_="a")

            if not job_listings:
                print("No jobs found on this page. Stopping.")
                break

            for job in job_listings:
                job_data = self.parse_job(job)
                self.jobs.append(job_data)

            print(f"Scraped page {page} successfully.")
            time.sleep(random.uniform(3, 7))  # Randomized sleep

        return self.jobs

    def save_to_excel(self, filename="scraped_jobs.xlsx"):
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"Scraped jobs saved to {filename}")


if __name__ == "__main__":
    scraper = JobScraper(query=config.JOB_TITLE, location=config.JOB_LOCATION, days_since_posted=config.JOB_DAYS_SINCE_POSTED)
    jobs = scraper.scrape()
    scraper.save_to_excel()
