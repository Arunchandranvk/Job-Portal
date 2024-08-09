def extract_job_links(soup):
    job_links = []
    for a_tag in soup.find_all('a', href=True):
        if '/job/' in a_tag['href']:
            job_links.append(a_tag['href'])
    return job_links

def extract_job_title(soup):
    job_titles = []
    for position in soup.find_all('div', class_='position'):
        title = position.find('h3')
        if title:
            job_titles.append(title.get_text(strip=True))
        else:
            job_titles.append("Not specified")
    return job_titles

def extract_company_name(soup):
    company_names = []
    for company in soup.find_all('div', class_='company'):
        name = company.find('strong')
        if name:
            company_names.append(name.get_text(strip=True))
        else:
            company_names.append("Not specified")
    return company_names

def extract_posted_date(soup):
    posted_dates = []
    for date_tag in soup.find_all('li', class_='date'):
        time_tag = date_tag.find('time')
        if time_tag:
            posted_dates.append(time_tag.get_text(strip=True))
        else:
            posted_dates.append("Not specified")
    return posted_dates

