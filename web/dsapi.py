#pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains


def quastiontojson(quastion):
    driver = webdriver.Firefox()

    ai_url = "https://huggingface.co/openai/gpt-oss-120b"
    driver.get(ai_url)
    sleep(0.2)
    cookie = {"name":"token","value":"FEAACHTfmatvqmPtAkwgcKoVYgMGuVnSAIfHVvJDDenZhUoOuUtEAHcmXyCcKaWZIuHazghdllTizQNBlalWHuziDaVpwqwIQbCDSlDSCgXdBZWWavRusMsyiSoAvRhN","domain":"huggingface.co"}
    #i'd put a new token over here if this dosent worked, signup into huggingface and insert your token into "value"
    driver.add_cookie(cookie)
    driver.get(ai_url)
    

    sleep(5)
    width = driver.execute_script("return window.innerWidth;")
    height = driver.execute_script("return window.innerHeight;")
    actions = ActionChains(driver)
    actions.move_by_offset(width / 2, height / 2).click().perform()
    actions.move_by_offset(width / 2, height / 2).click().perform()
    
    inputs = driver.find_elements(By.CSS_SELECTOR, '.rounded-t-none')
    input_text = inputs[0]
    input_submit = inputs[1]
    
    quastion = quastion.replace('\n',' ').replace('\r',' ')
    
    input_text.click()
    input_text.send_keys(str(quastion))
    input_submit.click()
    
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
    driver = webdriver.Firefox()
    
    ai_url = "https://huggingface.co/deepseek-ai/DeepSeek-V3-0324"
    driver.get(ai_url)
    cookie = {"name":"token","value":"FEAACHTfmatvqmPtAkwgcKoVYgMGuVnSAIfHVvJDDenZhUoOuUtEAHcmXyCcKaWZIuHazghdllTizQNBlalWHuziDaVpwqwIQbCDSlDSCgXdBZWWavRusMsyiSoAvRhN","domain":"huggingface.co"}
    #again you have to put a token in here to
    driver.add_cookie(cookie)
    driver.get(ai_url)
    
    #dismis_this = driver.find_element(By.CSS_SELECTOR, '[class~="btn"][class~="ring"][class~="ring-white/10"]')
    #dismis_this.click()
    sleep(5)
    width = driver.execute_script("return window.innerWidth;")
    height = driver.execute_script("return window.innerHeight;")
    actions = ActionChains(driver)
    actions.move_by_offset(width / 2, height / 2).click().perform()
    actions.move_by_offset(width / 2, height / 2).click().perform()
    
    inputs = driver.find_elements(By.CSS_SELECTOR, '.rounded-t-none')
    input_text = inputs[0]
    input_submit = inputs[1]
    default_len = len(driver.find_elements(By.CSS_SELECTOR, ".prose-widget.text-smd.prose.break-words"))
    quastion = quastion.replace('\n',' ').replace('\r',' ')
    input_text.click()
    input_text.send_keys(str(quastion))
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
