from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Setup the Browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

job_list = [] # Storage for our final dataset
# We will scrape the first 3 pages as a test (you can increase this to 10 later)
total_pages = 3 

for page in range(1, total_pages + 1):
    # Naukri's URL structure for multiple pages
    url = f"https://www.naukri.com/business-analyst-jobs-in-pune-{page}"
    print(f"Scraping Page {page}...")
    
    driver.get(url)
    time.sleep(5) # Allow JS to load the job cards
    
    # Grab the loaded HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find all job cards on the current page
    job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper')
    
    for job in job_cards:
        try:
            # Extracting specific data points for your analysis
            data = {
                'Title': job.find('a', class_='title').text.strip(),
                'Company': job.find('a', class_='comp-name').text.strip(),
                'Experience': job.find('span', class_='expwdth').text.strip(),
                'Location': job.find('span', class_='locWdth').text.strip(),
                'Posted_Date': job.find('span', class_='job-post-day').text.strip()
            }
            job_list.append(data)
        except AttributeError:
            # Skip if any specific field is missing in a card
            continue

# 2. Save the data to a CSV file
df = pd.DataFrame(job_list)
df.to_csv('naukri_business_analyst_data.csv', index=False)

print(f"\n--- Scraping Complete! ---")
print(f"Total Jobs Captured: {len(job_list)}")
print("File saved as: naukri_business_analyst_data.csv")

# 3. Close the browser
driver.quit()