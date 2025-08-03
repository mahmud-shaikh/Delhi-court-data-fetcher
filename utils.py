from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def extract_case_table(html, driver):
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
        print(f"ORDER_URL ->>>>>>>>>>>>> {order_url}")

        # Create and invoke a new function that calls the ORDERS link and fetch the first 2 links
        order_link_data = fetch_case_links(order_url, driver)
        print(f"ORDER LINK DATA: {order_link_data}")

        # Petitioner vs Respondent
        parties = cols[2].get_text(separator=" ", strip=True)

        # Listing Info
        listing_info = cols[3].get_text(separator=" | ", strip=True)

        result.append({
            "sr_no": sno,
            "case": case_text.replace("Orders", "").strip(),
            "parties": parties,
            "listing_date": listing_info,
            "order_link": order_link_data["order_link"],
            "order_link_text": order_link_data["order_link_text"]
        })

    print(f"RESULT: {result}")

    return result


def fetch_case_links(order_link, driver):
    driver.get(order_link)

    wait = WebDriverWait(driver, 10)

    # Wait until all form fields are present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#caseTable tbody tr td")))

    time.sleep(10)

    case_table_value = driver.find_element(By.ID, "caseTable").text.strip()
    # print(f"case table value: {case_table_value}")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", id="caseTable")
    result = []

    if not table:
        return []

    first_order_link_element = table.find("tbody").find("a")
    order_link = first_order_link_element["href"]
    order_link_text = first_order_link_element.text.strip()
    print(f"First Order Link: {first_order_link_element}")
    print(f"Order Link: {order_link}")
    print(f"Order Link Text: {order_link_text}")

    with open("response_output_2.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    return {
        "order_link": order_link,
        "order_link_text": order_link_text
    }
