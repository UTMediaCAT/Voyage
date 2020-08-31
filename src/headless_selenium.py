from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path=r'C:\Users\Alex\source\repos\SeleniumTest\packages\Selenium.Chrome.WebDriver.2.45\driver\chromedriver.exe', chrome_options=options)
web_name = 'https://www.dpa-international.com/'
driver.get(web_name)
"""try:
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "footer"))
    )
finally:
"""
cells = driver.find_elements_by_css_selector('.cell')
article_links = []
print(len(cells))
for cell in cells:
    article_links.append(web_name+cell.get_attribute("data-link"))
print(article_links)
