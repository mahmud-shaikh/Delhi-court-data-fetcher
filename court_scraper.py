import requests
from bs4 import BeautifulSoup

def fetch_case_data(case_type, case_number, year):
    base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"

    # https://services.ecourts.gov.in/ecourtindia_v6/?p=casestatus&state_code=HR&dist_code=12&court_code=1&cno=433&ctype=CA&cyear=2023
    
    params = {
        "p": "casestatus",
        "state_code": "HR",  # Haryana
        "dist_code": "12",   # Faridabad
        "court_code": "1",
        "cno": case_number,
        "ctype": case_type,
        "cyear": year
    }

    print(params)

    try:
        res = requests.get(base_url, params=params, timeout=60)
        res.raise_for_status()
        print("HELOOOOO")
        with open("response_output.html", "w", encoding="utf-8") as f:
            f.write(res.text)
    except requests.exceptions.RequestException as e:
        print("ERROR OCCURRED")
        return {"error": f"Network error or bad request: {str(e)}"}

    soup = BeautifulSoup(res.text, "html.parser")

    try:
        case_title_tag = soup.find("div", class_="case_title")
        if not case_title_tag:
            return {"error": "Case not found or invalid input. Please verify the case type/number/year."}

        case_title = case_title_tag.text.strip()
        date_sections = soup.find_all("div", class_="col-md-4 col-sm-4")
        
        filing_date = date_sections[0].text.strip().split(":")[-1].strip()
        next_hearing = date_sections[1].text.strip().split(":")[-1].strip()

        link_tag = soup.find("a", string="View Orders")
        if link_tag:
            pdf_url = base_url + link_tag["href"]
        else:
            pdf_url = "No PDF available."

        return {
            "case_title": case_title,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "latest_order_link": pdf_url
        }

    except Exception as e:
        return {"error": f"Parsing failed. Details: {str(e)}"}

if __name__ == "__main__":
    result = fetch_case_data("CA", "433", "2023")  # ← This is a valid case
    print(result)

# fetch_case_data("CA", "433", "2023")