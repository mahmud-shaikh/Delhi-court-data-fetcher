from database import close_conn, init_db, log_query
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils import extract_case_table

def fetch_case_data(case_type, case_number, year):
    # --- SETUP SELENIUM CHROME DRIVER ---
    options = Options()
    # options.add_argument("--headless")  # Optional: runs in background
    driver = webdriver.Chrome(options=options)
    conn = init_db()

    try:
        driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

        wait = WebDriverWait(driver, 10)

        # Wait until all form fields are present
        wait.until(EC.presence_of_element_located((By.ID, "case_type")))
        wait.until(EC.presence_of_element_located((By.ID, "case_number")))
        wait.until(EC.presence_of_element_located((By.ID, "case_year")))
        wait.until(EC.presence_of_element_located((By.ID, "captcha-code")))

        # Fill the form
        driver.find_element(By.ID, "case_type").send_keys(case_type)
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(year)

        # Get captcha text from span
        captcha_value = driver.find_element(By.ID, "captcha-code").text.strip()

        # Now wait for the input box to type captcha (this may be dynamically added)
        wait.until(EC.presence_of_element_located((By.ID, "captchaInput")))
        captcha_input_element = driver.find_element(By.ID, "captchaInput")
        captcha_input_element.send_keys(captcha_value)


        entered = captcha_input_element.get_attribute("value")

        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "search")))
        time.sleep(1)
        submit_button.click()
        
        time.sleep(1)

        html=driver.page_source

        log_query(conn,case_type,case_number,year,html)

        # Let JS load the result
        cases = extract_case_table(html, driver)

        return cases

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        # Close the DB connecton
        close_conn(conn)
        driver.quit()
