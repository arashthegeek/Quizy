from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC

chrome_path = r"C:\Program Files\chrome-win64\chrome.exe"
chromedriver_path = r"C:\Users\USER\Desktop\Django\testmaker\testmaker\testmaker\web\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
chrome_options.binary_location = chrome_path
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://huggingface.co/deepseek-ai/DeepSeek-V3-0324")
while True:
    print('abolhol2')
    ready_state = driver.execute_script('return document.readyState')
    if ready_state == 'complete':
        break
    print('abolhol')
    sleep(0.2)  # کمی تاخیر برای جلوگیری از پر شدن کنسول
input('')