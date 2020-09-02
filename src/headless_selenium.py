from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
def get_articles_from_site(driver, web_name):
    site_regex_secure = r'https://www.(.*)'
    site_regex_insecure = r'http://www.(.*)'
    page_name = re.search(site_regex_secure, web_name).group(1)
    if 'www.' in web_name:
        if 'https' in web_name:
            shortened_web_name = 'https://'+page_name
        elif 'http' in web_name:
            shortened_web_name = 'http://'+page_name
    else:
        shortened_web_name = web_name
    print(page_name, web_name)
    driver.get(web_name)
    time.sleep(20)
    if driver.find_elements_by_css_selector(".mfp-content .popup"):
        driver.find_element_by_css_selector(".mfp-content .popup .link-close-popup > *").click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".mfp-content .popup")))

    time.sleep(10)
    cells = driver.find_elements_by_tag_name('a')
    article_links = []
    weed_out = []
    print(len(cells))
    for cell in cells:
        if cell.get_attribute("href") != None:
            link = cell.get_attribute("href")
        else:
            link = cell.get_attribute("src")
        if link and link != '' and page_name in link and link != shortened_web_name and link != web_name+"#":
            article_links.append(link)
        else:
            weed_out.append(link)
    print(len(article_links), article_links)
    print(weed_out)
    
options = Options()
# Comment this out if you want the headless mode to be disabled
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#####################################
driver = webdriver.Chrome(chrome_options=options)
web_name = 'https://www.dpa-international.com/'
driver.get(web_name)
cells = driver.find_elements_by_css_selector('.cell')
article_links = []
print(len(cells))
for cell in cells:
    article_links.append(web_name+cell.get_attribute("data-link"))
print(article_links)
web_name = 'https://www.indianexpress.com/'
get_articles_from_site(driver, web_name)
web_name = 'https://www.jadaliyya.com/'
get_articles_from_site(driver, web_name)
web_name = 'https://www.bbc.com/'
get_articles_from_site(driver, web_name)
driver.close()
driver.quit()
