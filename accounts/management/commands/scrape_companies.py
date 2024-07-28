import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from django.core.management.base import BaseCommand
from accounts.models import Company

class Command(BaseCommand):
    help = 'Scrape companies from Technopark'

    def handle(self, *args, **kwargs):
        # Set up the Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        base_url = 'https://www.cyberparkkerala.org/companies-at-park'
        data_list = []

        try:
            # Open the A-Z listing page
            driver.get(base_url)

            # Scroll to the bottom of the page to load more companies
            actions = ActionChains(driver)
            for _ in range(2):  # Adjust the range as needed
                actions.send_keys(Keys.END).perform()
                time.sleep(2)  # Adjust the sleep time as needed

            # Get the HTML content after scrolling
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract company links
            company_links = [a['href'] for a in soup.select('.flt_rigt a[href^="https://www.cyberparkkerala.org/listings/"]')]

            # Visit each company page and scrape details
            for company_link in company_links:
                # Open the company page in a new window
                driver.execute_script("window.open('', '_blank');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(company_link)
                time.sleep(2)  # Adjust the sleep time as needed

                # Get the HTML content of the company page
                company_page_source = driver.page_source
                company_soup = BeautifulSoup(company_page_source, 'html.parser')

                # Extract relevant company details
                company_info_elements = company_soup.select('.profile_area .list-sx li')
                company_data = {}
                for info_element in company_info_elements:
                    title_element = info_element.find('div', class_='tit')
                    if title_element:
                        title = title_element.text.strip().lower()
                        value_element = info_element.find_all(text=True, recursive=False)
                        value = ''.join(value_element).strip()
                        company_data[title] = value

                # Extract specific details: company name, email, website, and phone
                company_name = company_data.get('company name', None)

                email_element = company_soup.find('div', class_='tit', string='email')
                email = email_element.find_next('a').text.strip() if email_element else None

                website_element = company_soup.find('div', class_='tit', string='website')
                website = website_element.find_next('a').text.strip() if website_element else None

                phone = company_data.get('phone', None)

                if company_name:
                    data = {
                        "name": company_name,
                        "email": email,
                        "website": website,
                        "phone": phone,
                        "tab_url": driver.current_url
                    }
                    data_list.append(data)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            self.stdout.write(f"An error occurred: {e}")

        finally:
            driver.quit()

        # Save data to the database
        for data in data_list:
            Company.objects.update_or_create(
                name=data["name"],
                defaults={
                    "email": data["email"],
                    "website": data["website"],
                    "phone": data["phone"],
                    "tab_url": data["tab_url"]
                }
            )

        self.stdout.write('Finished scraping companies.')

