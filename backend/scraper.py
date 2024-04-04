from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pandas import DataFrame
import os

def scrape_to_csv(url, csv_file_name):
    print('Starting scrape...')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the modal to appear and attempt to close it
    try:
        print('entering try block')
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "esparto-NoButtonElement--zHewpDFp6nnE0cvW6id0"))
        ).click()
        print("Modal found and closed.")
    except (TimeoutException, NoSuchElementException):
        print("Timed out waiting for the modal or no modal found.")

    # Scroll to the bottom of the page to load all the data
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Scrape the locked columns
    locked_table = driver.find_element(By.CSS_SELECTOR, 'div.k-grid-content-locked table')
    locked_rows = locked_table.find_elements(By.TAG_NAME, 'tr')
    locked_data = []
    for row in locked_rows:
        locked_cells = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
        if locked_cells:
            locked_data.append(locked_cells)

    # Scrape the scrollable columns
    scrollable_table = driver.find_element(By.CSS_SELECTOR, 'div.k-grid-content table')
    scrollable_rows = scrollable_table.find_elements(By.TAG_NAME, 'tr')
    scrollable_data = []
    for row in scrollable_rows:
        scrollable_cells = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
        if scrollable_cells:
            scrollable_data.append(scrollable_cells)

    # Combine locked and scrollable data
    combined_data = [locked + scrollable for locked, scrollable in zip(locked_data, scrollable_data)]

    # Extract the column headers
    headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, 'th[role="columnheader"]')]

    driver.quit()

    # Create a DataFrame and save as CSV
    df = DataFrame(combined_data, columns=headers)
    df.to_csv(csv_file_name, index=False)
    print('CSV file saved:', csv_file_name)

# Usage

def run_scraper(start_year, end_year):
    current_season = start_year

    while current_season <= end_year:
        print('Scraping season:', current_season)

        year_folder = f'data/{current_season}'
        os.makedirs(year_folder, exist_ok=True)

        # Scrape offensive passing stats
        scrape_to_csv(f"https://fantasydata.com/nfl/team-stats?season={current_season}&seasontype=1&teamaspect=1&stattype=3", os.path.join(year_folder, f"offense_passing_{current_season}.csv"))

        # Scrape offensive rushing stats
        scrape_to_csv(f"https://fantasydata.com/nfl/team-stats?season={current_season}&seasontype=1&teamaspect=1&stattype=4", os.path.join(year_folder, f"offense_rushing_{current_season}.csv"))

        # Scrape defensive passing stats
        scrape_to_csv(f"https://fantasydata.com/nfl/team-stats?season={current_season}&seasontype=1&teamaspect=2&stattype=3", os.path.join(year_folder, f"defense_passing_{current_season}.csv"))

        # Scrape defensive rushing stats
        scrape_to_csv(f"https://fantasydata.com/nfl/team-stats?season={current_season}&seasontype=1&teamaspect=2&stattype=4", os.path.join(year_folder, f"defense_rushing_{current_season}.csv"))

        current_season += 1

run_scraper(2002, 2021)