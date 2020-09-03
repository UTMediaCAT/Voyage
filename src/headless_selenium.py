from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
def get_articles_from_site(driver, web_name, tag_name = "a", attribute = "href"):
    #Regex to separate the website name and its domain
    general_regex = r'://(www\.)?(.*)(\.[a-zA-Z]+)'
    if "https" == web_name[0:5]:
        site_regex = r'https'+general_regex
    else:
        site_regex = r'http'+general_regex
    path_regex = "^/?[^/]+/[^/]+$"
    groups = re.search(site_regex, web_name) 
    page_name = groups.group(2)
    domain = groups.group(3)
    if 'www.' in web_name:
        if 'https' in web_name:
            shortened_web_name = 'https://'+page_name+domain
        elif 'http' in web_name:
            shortened_web_name = 'http://'+page_name+domain
    else:
        shortened_web_name = web_name
    print(page_name, web_name)
    driver.get(web_name)
    time.sleep(20)
    if driver.find_elements_by_css_selector(".mfp-content .popup"):
        driver.find_element_by_css_selector(".mfp-content .popup .link-close-popup > *").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".mfp-content .popup")))
    cells = driver.find_elements_by_css_selector(tag_name)
    article_links = set()
    print(len(cells))
    for cell in cells:
        link = cell.get_attribute(attribute)
        if link:
            if re.match(path_regex, link):
                article_links.add(web_name+link)
            elif link != '' and page_name in link and link != shortened_web_name and link != web_name+"#":
                article_links.add(link)
    print(len(article_links))
    return article_links
options = Options()
# Comment this out if you want the headless mode to be disabled
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
#####################################
driver = webdriver.Chrome(chrome_options=options)
web_name = 'https://www.dpa-international.com/'
dpa_set = get_articles_from_site(driver, web_name, ".cell", "data-link")
dpa_set = dpa_set.union(get_articles_from_site(driver, web_name))
print(dpa_set)
website_list = ['https://www.cbc.ca','https://www.indianexpress.com/','https://www.jadaliyya.com/',
                'https://www.bbc.com/','https://www.alarabiya.net']
for web_name in website_list:
    article_set = get_articles_from_site(driver, web_name)
    print(article_set)
driver.close()
driver.quit()
