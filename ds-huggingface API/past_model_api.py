#pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.support import expected_conditions as EC

def quastiontojson(quastion):
    chrome_path = r"C:\Program Files\chrome-win64\chrome.exe" #-----------here
    if chrome_path == "":
        print("please insert your chrome browser address to (/testmaker/web/ai.py --> quastiontojson().chrome_path)")
        exit()
    chromedriver_path = r"C:\Users\USER\Desktop\Django\testmaker\testmaker\testmaker\web\chromedriver-win64\chromedriver.exe" #-----------here
    if chromedriver_path == "":
        print("please insert your selenium chrome driver(i put it into /testmaker/web/chromedriver-win64/chromedriver.exe) address to (/testmaker/web/ai.py --> quastiontojson().chromedriver_path")
        exit()
    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    ai_url = "https://huggingface.co/deepseek-ai/DeepSeek-V3-0324"
    print(1)
    driver.get(ai_url)
    print(2)
    sleep(0.2)
    cookie = {"name":"token","value":"mIIhClmsUfGWrVYNBdbnIZjYUgCjLIYJPPAaLGxyRUcEnblgAvPxbEAOTnnxeYBFyqzGSLRnkqXyHglDkFJZYHEPLzktbToGWqFRyEMUwkuVWijatrWuuzoZkVlXMYsf","domain":"huggingface.co"}
    #i'd put a new token over here if this dosent worked, signup into huggingface and insert your token into "value"
    driver.add_cookie(cookie)
    print(3)
    driver.get(ai_url)
    print(4)
    dismis_this = driver.find_element(By.CSS_SELECTOR, '[class~="btn"][class~="ring"][class~="ring-white/10"]')
    dismis_this.click()
    inputs = driver.find_elements(By.CSS_SELECTOR, '.rounded-t-none')
    input_text = inputs[0]
    input_submit = inputs[1]

    input_text.send_keys(quastion)
    input_submit.click()
    ele = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, 'code'))
    )
    
    sleep(40)
    #ai_response_paragraphs = ai_response_div.find_elements(By.CSS_SELECTOR, 'p')
    #ai_response_text = ""
    #TODO try in here in case the course was too long and if there was error jump to line 33
    #for j in ai_response_paragraphs:
    #    ai_response_text += str(j.text)
        
    #TODO: get_element <code> and every span in it is our need
    #ai_response_span = ai_response_div.find_elements(By.TAG_NAME, 'span')#hljs-punctuation hljs-attr hljs-string hljs-number hljs-literal and...
    ai_response_code = driver.find_elements(By.TAG_NAME, 'code')
    ai_response = ""

    ai_response = ai_response_code[len(ai_response_code)-1].text
    driver.close()
    return ai_response

def aichat(quastion):
    chrome_path = r"C:\Program Files\chrome-win64\chrome.exe" #------------here
    if chrome_path == "":
        print("please insert your chrome browser address to (/testmaker/web/ai.py --> aichat().chrome_path)")
        exit()
    chromedriver_path = r"C:\Users\USER\Desktop\Django\testmaker\testmaker\testmaker\web\chromedriver-win64\chromedriver.exe" #-----------here
    if chromedriver_path == "":
        print("please insert your selenium chrome driver(i put it into /testmaker/web/chromedriver-win64/chromedriver.exe) address to (/testmaker/web/ai.py --> aichat().chromedriver_path")
        exit()

    chrome_options = Options()
    chrome_options.binary_location = chrome_path
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    

    
    ai_url = "https://huggingface.co/deepseek-ai/DeepSeek-V3-0324"
    driver.get(ai_url)
    cookie = {"name":"token","value":"mIIhClmsUfGWrVYNBdbnIZjYUgCjLIYJPPAaLGxyRUcEnblgAvPxbEAOTnnxeYBFyqzGSLRnkqXyHglDkFJZYHEPLzktbToGWqFRyEMUwkuVWijatrWuuzoZkVlXMYsf","domain":"huggingface.co"}
    #again you have to put a token in here to
    driver.add_cookie(cookie)
    driver.get(ai_url)
    #driver.refresh()
    dismis_this = driver.find_element(By.CSS_SELECTOR, '[class~="btn"][class~="ring"][class~="ring-white/10"]')
    dismis_this.click()
    inputs = driver.find_elements(By.CSS_SELECTOR, '.rounded-t-none')
    input_text = inputs[0]
    input_submit = inputs[1]
    default_len = len(driver.find_elements(By.CSS_SELECTOR, ".prose-widget.text-smd.prose.break-words"))
    input_text.send_keys(quastion)
    input_submit.click()
    
    sleep(40)
    
    elements = driver.find_elements(By.CSS_SELECTOR, ".prose-widget.text-smd.prose.break-words")
    element = elements[len(elements)-1]
    
    ai_response_text = ""
    try:
        ai_response_text += element.text
    except:
        driver.close()
        return "Unsucssesful."
    driver.close()
    return ai_response_text