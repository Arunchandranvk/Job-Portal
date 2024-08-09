from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
import time
from django.http import JsonResponse
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import pandas as pd
from .forms import *
from django.core.cache import cache
import pandas as pd
import requests
from django.core.files.base import ContentFile
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from datetime import datetime
# Create your views here.

def extract_job_title(soup):
    return [title.text for title in soup.find_all('span', {'title': True})]

def extract_company_name(soup):
    return [company.text for company in soup.find_all('span', {'data-testid': 'company-name'})]

def extract_job_location(soup):
    return [loc.text for loc in soup.find_all('div', {'data-testid': 'text-location'})]

def extract_salaries(soup):
    return [sal.text if sal.text else "Not specified" for sal in soup.find_all('div', class_='metadata salary-snippet-container')]

def extract_job_links(soup):
    return [a['href'] for a in soup.find_all('a', {'class': 'jcs-JobTitle'}, href=True)]

def extract_job_type(soup):
    job_type_element = soup.find('div', class_='css-1p3gyjy e1xnxm2i0')
    return job_type_element.text if job_type_element else "Not specified"

def scrape_indeed_jobs(job_name, location,num_days):
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={UserAgent().random}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    chrome_service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    base_url = f'https://in.indeed.com/jobs?q={job_name.replace(" ", "+")}&l={location.replace(" ", "+")}&fromage={num_days}&start='

    try:
        start = 0
        while True:
            url = f'{base_url}{start}'
            print(f"Scraping page {url}")
            driver.get(url)
            time.sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            job_titles = extract_job_title(soup)
            company_names = extract_company_name(soup)
            job_locations = extract_job_location(soup)
            # salaries = extract_salaries(soup)
            job_links = extract_job_links(soup)
            # job_types = [extract_job_type(soup) for _ in range(len(job_titles))]

            for i in range(len(job_titles)):
                job_data = {
                    "job_title": job_titles[i] if i < len(job_titles) else None,
                    "company_name": company_names[i] if i < len(company_names) else None,
                    "job_location": job_locations[i] if i < len(job_locations) else None,
                    # "salary": salaries[i] if i < len(salaries) else "Not specified",
                    # "job_type": job_types[i] if i < len(job_types) else "Not specified",
                    "job_url": f'https://in.indeed.com{job_links[i]}' if i < len(job_links) else None,
                }
                # def normalize_url(url):
                #     # Normalize the URL, e.g., by hashing it
                #     return hashlib.md5(url.encode('utf-8')).hexdigest()


                # normalized_url = normalize_url(job_data["job_url"])


                if not IndeedJobs.objects.filter(job_title=job_data["job_title"],company_name=job_data["company_name"]).exists():
                    
                    IndeedJobs.objects.create(**job_data)
                    print("New Job Added")
                else:
                    print("Already Exists!!!!")
            next_page_button = soup.find('a',{'data-testid': 'pagination-page-next'})
            if not next_page_button:
                print("No more pages. Exiting loop.")
                break

            start += 10

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

class HomeView(TemplateView):
    template_name = 'index.html'
    # def get(self, request, *args, **kwargs):
    #     cache_key = 'last_scrape_time'
    #     expiration_time = 24 * 60 * 60  # Cache expiration time in seconds (24 hours)
    #     last_scrape_time = cache.get(cache_key)      
    #     if not last_scrape_time or timezone.now() - last_scrape_time > timedelta(days=1):
    #         scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support,webdeveloper,ai', location='Ernakulam',num_days=7)  # Fetch jobs from the past 7 days         
    #         scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support,webdeveloper,ai', location='Kozhikode',num_days=7)  # Fetch jobs from the past 7 days         
    #         scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support,webdeveloper,ai', location='Thiruvananthapuram',num_days=7)  # Fetch jobs from the past 7 days         
    #         scrape_indeed_jobs(job_name='developer , software engineer, frontend developer ,backend developer ,restapi', location='Kerala',num_days=7)  # Fetch jobs from the past 7 days         
    #         cache.set(cache_key, timezone.now(), timeout=expiration_time)
    #     return super().get(request, *args, **kwargs)
    

class CyberparkCompaniesView(TemplateView):
    template_name = 'cyberpark_companies.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()

        # Modify URLs to ensure they start with 'http://'
        for company in companies:
            if not company.website.startswith(('http://', 'https://')):
                company.website = 'http://' + company.website

        context['companies'] = companies
        return context
 
def indeed_job_search_view(request):
    jobs = IndeedJobs.objects.all().order_by('-datetime')
    
    if request.method == 'POST':
        form = JobSearchForm(request.POST)
        if form.is_valid():
            job_name = form.cleaned_data['job_name']
            location = form.cleaned_data['location']

            if job_name:
                jobs = jobs.filter(job_title__icontains=job_name)
            if location:
                jobs = jobs.filter(job_location__icontains=location)
            return render(request, 'indeed.html', {'form': form, 'jobs': jobs})
        else:
            jobs = IndeedJobs.objects.none()
    else:
        form = JobSearchForm()
        jobs = IndeedJobs.objects.all().order_by('-datetime')
        return render(request, 'indeed.html', { 'form': form,'jobs': jobs})
    
    

# Function to fetch job data from a specific page
def fetch_jobs(page):
    url = f"https://technopark.org/api/paginated-jobs?page={page}&search=&type="
    response = requests.get(url)
    return response.json()

# Function to process and save job data
def save_job_data(data):
   for job in data['data']:
    # print(job)
    company_data = job['company']
    company_name = company_data['company']
    logo_url = f"https://technopark.org{company_data['logo']}"
    
    # Download the logo image
    response = requests.get(logo_url)
    if response.status_code == 200:
        logo_content = ContentFile(response.content)
        try:
            closing_date = datetime.strptime(job['closing_date'], '%Y-%m-%d')  # Adjust format as needed
            # Make the naive datetime aware
            closing_date = timezone.make_aware(closing_date, timezone.get_current_timezone())
            print(closing_date)
        except ValueError:
            print(f"Invalid date format for job: {job['closing_date']}")
            continue
        if not closing_date < timezone.now():
            job_instance, created = TechnoparkJobs.objects.update_or_create(
                job_id=job['id'],
                defaults={
                    'job_listing_id': job['job_listing_id'],
                    'title': job['job_title'],
                    'posted_date': job['posted_date'],
                    'closing_date': job['closing_date'],
                    'company': company_name,
                }
            )

            # Save the logo file
            job_instance.logo.save(f"{company_name}_logo.jpg", logo_content, save=True)
        else:
            print("Job Expired")

# Main function to scrape and save jobs from all pages
def scrape_and_save_jobs_technopark():
    initial_data = fetch_jobs(1)
    total_pages = initial_data['last_page']

    # Fetch and process jobs from all pages
    for page in range(1, total_pages + 1):
        print(f"Fetching page {page} of {total_pages}")
        data = fetch_jobs(page)
        save_job_data(data)



def Technopark_job_search_view(request):
    jobs = TechnoparkJobs.objects.all().order_by('-datetime')
    
    if request.method == 'POST':
        form = JobSearchparkForm(request.POST)
        if form.is_valid():
            job_name = form.cleaned_data['job_name']
            company = form.cleaned_data['company']

            if job_name:
                jobs = jobs.filter(title__icontains=job_name)
            if company:
                jobs = jobs.filter(company__icontains=company)
            return render(request, 'technoparkjobs.html', {'form': form, 'jobs': jobs})
        else:
            jobs = TechnoparkJobs.objects.none()
    else:
        form = JobSearchparkForm()
        jobs = TechnoparkJobs.objects.all().order_by('-datetime')
        return render(request, 'technoparkjobs.html', { 'form': form,'jobs': jobs})
    
    
    
def extract_job_links_cyberpark(soup):
    job_links = []
    for a_tag in soup.find_all('a', href=True):
        if '/job/' in a_tag['href']:
            job_links.append(a_tag['href'])
    return job_links

def extract_job_title_cyberpark(soup):
    job_titles = []
    for position in soup.find_all('div', class_='position'):
        title = position.find('h3')
        if title:
            job_titles.append(title.get_text(strip=True))
        else:
            job_titles.append("Not specified")
    return job_titles

def extract_company_name_cyberpark(soup):
    company_names = []
    for company in soup.find_all('div', class_='company'):
        name = company.find('strong')
        if name:
            company_names.append(name.get_text(strip=True))
        else:
            company_names.append("Not specified")
    return company_names

def extract_posted_date_cyberpark(soup):
    posted_dates = []
    for date_tag in soup.find_all('li', class_='date'):
        time_tag = date_tag.find('time')
        if time_tag:
            posted_dates.append(time_tag.get_text(strip=True))
        else:
            posted_dates.append("Not specified")
    return posted_dates


def extract_images_cyberpark(soup):
    images = []
    for img_tag in soup.find_all('img', class_='company_logo'):
        src = img_tag.get('src', 'Not specified')
        images.append(src)
    return images

    

def Cyberpark_Jobs():
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={UserAgent().random}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    base_url = 'https://www.cyberparkkerala.org/careers'
    driver.get(base_url)

    actions = ActionChains(driver)

    button_wait_timeout = 15
    button_disappear_timeout = 10
    click_delay = 1.5

    last_visible_time = time.time()

    while True:
        try:
            load_more_button = WebDriverWait(driver, button_wait_timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.load_more_jobs"))
            )

            last_visible_time = time.time()
            load_more_button.click()
            time.sleep(click_delay)

        except TimeoutException:
            if time.time() - last_visible_time > button_disappear_timeout:
                break
            else:
                time.sleep(1)

        except (NoSuchElementException, ElementNotInteractableException) as e:
            break

    actions.send_keys(Keys.END).perform()
    time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    job_links = extract_job_links_cyberpark(soup)
    company_names = extract_company_name_cyberpark(soup)
    job_titles = extract_job_title_cyberpark(soup)
    post_dates = extract_posted_date_cyberpark(soup)
    # logo = extract_images(soup)

    length = len(job_links)
    for i in range(length):     
        company_name = company_names[i] if i < len(company_names) and company_names[i] else "Not specified"
        job_title = job_titles[i] if i < len(job_titles) and job_titles[i] else "Not specified"
        job_link = job_links[i] if i < len(job_links) and job_links[i] else "Not specified"
        post_date = post_dates[i] if i < len(post_dates) and post_dates[i] else "Not specified"
        # logo = logo[i] if i < len(logo) and logo[i] else "Not specified"
        
        if not CyberparkJobs.objects.filter(job_title=job_title,company_name=company_name).exists():
            try:   
                date_str = post_date.replace('Posted on ', '').strip()
                
                # Parse the date string
                date = datetime.strptime(date_str, '%B %d, %Y')
                
                # Make the naive datetime aware
                aware_date = timezone.make_aware(date, timezone.get_current_timezone())
        
            except ValueError:
                print(f"Invalid date format for job: {post_date}")
            if aware_date >= (timezone.now() - timedelta(days=30)):
                CyberparkJobs.objects.create(
                    company_name=company_name,
                    job_title=job_title,
                    job_link=job_link,
                    post_date=post_date
                )
            else:
                print("Outdated")
        else:
            print(f"Skipping duplicate entry: {company_name} - {job_title}")
    driver.quit()
    
    
    
def Cyberpark_job_search_view(request):
    jobs = CyberparkJobs.objects.all().order_by('-datetime')
    
    if request.method == 'POST':
        form = JobSearchparkForm(request.POST)
        if form.is_valid():
            job_name = form.cleaned_data['job_name']
            company = form.cleaned_data['company']

            if job_name:
                jobs = jobs.filter(job_title__icontains=job_name)
            if company:
                jobs = jobs.filter(company_name__icontains=company)
            return render(request, 'cyberpark_jobs.html', {'form': form, 'jobs': jobs})
        else:
            jobs = CyberparkJobs.objects.none()
    else:
        form = JobSearchparkForm()
        jobs = CyberparkJobs.objects.all().order_by('-datetime')
        return render(request, 'cyberpark_jobs.html', { 'form': form,'jobs': jobs})    
    
    
    
def Infopark_jobs():
        chrome_options = Options()
        chrome_options.add_argument(f'user-agent={UserAgent().random}')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled') 

        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # URL to be scraped
        url = 'https://infopark.in/ml/companies/job-search'
        driver.get(url)

        try:
            # Wait for the elements to be present
            wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
            while True:
                try:
                    # Locate job elements
                    job_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.joblist')))
                    
                    if not job_elements:
                        break
                    
                    for job in job_elements:
                        try:
                            title_element = job.find_element(By.CSS_SELECTOR, 'a')
                            title = title_element.text.strip() if title_element else 'N/A'
                            job_url = title_element.get_attribute('href') if title_element else 'N/A'
                            
                            company_element = job.find_element(By.CSS_SELECTOR, '.jobs-comp-name a')
                            company = company_element.text.strip() if company_element else 'N/A'
                            
                            date_element = job.find_element(By.CSS_SELECTOR, '.job-date')
                            posted_date = date_element.text.strip() if date_element else 'N/A'
                            if  not  InfoparkJobs.objects.filter(company=company,job_title=title).exists():
                               InfoparkJobs.objects.create(company=company,job_title=title,job_link=job_url,post_date=posted_date)
                        except Exception as e:
                            print(f"Error processing job listing: {e}")
                    
          
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
                        if next_button:
                            next_button.click()
                            wait.until(EC.staleness_of(job_elements[0]))  # Wait until the page is reloaded
                        else:
                            break
                    except NoSuchElementException:
                        print("No more pages or error finding the next page.")
                        break

                except TimeoutException:
                    print("Error: Timeout while waiting for elements to load.")
                    break

        finally:
            driver.quit()

            

def Infopark_job_search_view(request):
    jobs = InfoparkJobs.objects.all().order_by('-datetime')
    
    if request.method == 'POST':
        form = JobSearchInfoparkparkForm(request.POST)
        if form.is_valid():
            job_name = form.cleaned_data['job_name']
            company = form.cleaned_data['company']

            if job_name:
                jobs = jobs.filter(job_title__icontains=job_name)
            if company:
                jobs = jobs.filter(company__icontains=company)
            return render(request, 'infopark_jobs.html', {'form': form, 'jobs': jobs})
        else:
            jobs = CyberparkJobs.objects.none()
    else:
        form = JobSearchparkForm()
        jobs = InfoparkJobs.objects.all().order_by('-datetime')
        return render(request, 'infopark_jobs.html', { 'form': form,'jobs': jobs})    
    
    
    
    
    
def test(request):
    # Filter jobs where the closing date is less than the current time
    job_qs = TechnoparkJobs.objects.filter(closing_date__lt=timezone.now())
    
    # Serialize the queryset into a list of dictionaries
    job_list = list(job_qs.values())

    # Return the serialized data as a JSON response
    return JsonResponse(job_list, safe=False)


