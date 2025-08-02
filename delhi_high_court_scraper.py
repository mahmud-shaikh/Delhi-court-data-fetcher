from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- SETUP SELENIUM CHROME DRIVER ---
options = Options()
options.add_argument("--headless")  # Optional: runs in background
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

    with open("response_output_1.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # print(driver.page_source)

    wait = WebDriverWait(driver, 10)

    # Wait until all form fields are present
    wait.until(EC.presence_of_element_located((By.ID, "case_type")))
    wait.until(EC.presence_of_element_located((By.ID, "case_number")))
    wait.until(EC.presence_of_element_located((By.ID, "case_year")))
    wait.until(EC.presence_of_element_located((By.ID, "captcha-code")))

    # Fill the form
    driver.find_element(By.ID, "case_type").send_keys("CRL.M.C.")
    driver.find_element(By.ID, "case_number").send_keys("1474")
    driver.find_element(By.ID, "case_year").send_keys("2022")

    # Get captcha text from span
    captcha_value = driver.find_element(By.ID, "captcha-code").text.strip()
    print(f"captcha value: {captcha_value}")

    # Now wait for the input box to type captcha (this may be dynamically added)
    wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
    captcha_input_element = driver.find_element(By.ID, "captchaInput")
    captcha_input = captcha_input_element.send_keys(captcha_value)


    entered = captcha_input_element.get_attribute("value")
    print("Entered Captcha:", entered)

 
    # Submit the form
    submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "search"))
    )
    time.sleep(2)
    submit_button.click()

    # # Wait for the result table to load
    # wait.until(EC.presence_of_element_located((By.ID, "caseTable")))
    # table = driver.find_element(By.ID, "caseTable")
    # print("\n✅ Case Status Table Found:\n")
    # print(table.text)

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    driver.quit()
