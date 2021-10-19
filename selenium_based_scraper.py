from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/results?search_query=raag+malkauns&sp=EgIQAQ%253D%253D")

userdata = driver.find_element_by_xpath('//*[@id="video-title"]')
links = []

for i in userdata:
    links.append(i.get_attribute('href'))

print(len(links))