import csv
import parameters
from parsel import Selector
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

#Write to csv file with the ordered column that you want
writer = csv.writer(open(parameters.file_name, 'w'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'Url'])

#This function is to check field is null or not.
#if null replace with '' to print out.
def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

#Open ChromeDriver
driver = webdriver.Chrome('chromedriver')

driver.get("https://www.linkedin.com")
sleep(0.5)

#Auto Login
#Auto fill username: just put your username in parameters.py file
username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

#Auto fill password: just put your password in parameters.py file
password = driver.find_element_by_id('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

#Auto click login, another way is to use send_keys method with RETURN key.
login_btn = driver.find_element_by_xpath('//*[@type="submit"]')
login_btn.click()
sleep(5)

#Search in google
driver.get('https://www.google.com')
sleep(3)

#Auto fill search query
search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

#Scraping link in google result pages
#I just use selenium only so just scrapy first google result page.
#Can improve by use Scrapy to crawl all the result link then use Selenium.
linkedin_urls = driver.find_elements_by_tag_name('cite')
linkedin_urls = [url.text for url in linkedin_urls if 'linkedin' in url.text]
sleep(0.5)

#For each link, just extract the information you need
for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//h1/text()').extract_first()
    if name:
        name = name.strip()

    job_title = sel.xpath('//h2/text()').extract_first()
    if job_title:
        job_title = job_title.strip()

    school = sel.xpath('//*[contains(@class, "pv-top-card-v2-section__school-name")]/text()').extract_first()
    if school:
        school = school.strip()

    location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
    if location:
        location = location.strip()

    user_url = driver.current_url

    validate_field
    name = validate_field(name)
    job_title = validate_field(job_title)
    school = validate_field(school)
    location = validate_field(location)

    print("\n")
    print("Name: " + name)
    print("Job Title: " + job_title)
    print("School: " + school)
    print("Location: " + location)
    print("Url: " + user_url)
    print("\n")

    #Encode for easily reading
    writer.writerow([name.encode('utf-8'),
                     job_title.encode('utf-8'),
                     school.encode('utf-8'),
                     location.encode('utf-8'),
                     user_url.encode('utf-8'),
                     ])

driver.quit()
