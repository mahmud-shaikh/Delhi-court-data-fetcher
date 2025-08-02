from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

# --- SETUP SELENIUM CHROME DRIVER ---
options = Options()
# options.add_argument("--headless")  # Optional: runs in background
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
    # submit_button = WebDriverWait(driver, 10).until(
    # EC.element_to_be_clickable((By.ID, "search"))
    # )
    # time.sleep(2)
    # submit_button.click()

    submit_button = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    submit_button.click()

    time.sleep(10)
    html=driver.page_source
    
    def extract_case_table(html):
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", id="caseTable")
        result = []

        if not table:
            return []

        rows = table.find("tbody").find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            sno = cols[0].text.strip()

            # Case Number and Status
            case_text = cols[1].get_text(separator=" ", strip=True)
            order_link = cols[1].find("a", string="Orders")
            order_url = order_link["href"] if order_link else "Not available"

            # Petitioner vs Respondent
            parties = cols[2].get_text(separator=" ", strip=True)

            # Listing Info
            listing_info = cols[3].get_text(separator=" | ", strip=True)

            result.append({
                "S.No.": sno,
                "Diary No. / Case No.": case_text,
                "Petitioner Vs. Respondent": parties,
                "Listing Date / Court No.": listing_info,
                "Order Link": order_url
            })

        return result

    # Let JS load the result

    cases = extract_case_table(html)
    print(f"Cases: {cases}")

    # Pretty-print the result
    for case in cases:
        for k, v in case.items():
            print(f"{k}: {v}")
        print("-" * 50)

        # # Wait for the result table to load
        # wait.until(EC.presence_of_element_located((By.ID, "caseTable")))
        # table = driver.find_element(By.ID, "caseTable")
        # print("\n✅ Case Status Table Found:\n")
        # print(table.text)

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    driver.quit()
