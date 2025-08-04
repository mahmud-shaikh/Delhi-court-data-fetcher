
# 🏛 Court-Data Fetcher

A Python-based web app to fetch and log case details from the **Delhi High Court** website using Selenium, BeautifulSoup, and SQLite. The project provides a simple form interface and programmatically bypasses dynamic content like CAPTCHA.

---

## 📍 Court Chosen

**Delhi High Court**  
Website: [https://delhihighcourt.nic.in/app/get-case-type-status](https://delhihighcourt.nic.in/app/get-case-type-status)

---

## ⚙️ Setup Steps

### 1. Clone the Repository
```bash
git clone https://github.com/mahmud-shaikh/Delhi-court-data-fetcher
cd Delhi-court-data-fetcher
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (see below)

### 5. Run the Flask App
```bash
python app.py
```

---

## 🤖 CAPTCHA Strategy

The Delhi High Court website uses a **simple text-based CAPTCHA** that appears in a `span` element.  
This app:

- Reads the text directly from `#captcha-code`
- Enters it into the `#captchaInput` field
- Uses `WebDriverWait` to handle DOM readiness
- Automatically submits the form once CAPTCHA is handled

---

## 🧪 Features

- ✅ Input form for **Case Type**, **Case Number**, and **Year**
- ✅ Web scraping using **Selenium WebDriver**
- ✅ Dynamic form field interaction and CAPTCHA solving
- ✅ Parses case table and extracts **first “Order” link**
- ✅ Logs full HTML responses to **SQLite**
- ✅ Well-structured modular design using `utils.py` and `delhi_high_court_scraper.py`
- ✅ Graceful error handling and cleanup of driver/DB

---

## 🌱 Sample `.env` File

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

---

## 📁 Project Structure

```
court-data-fetcher/
│
├── app.py                         # Flask app entry point
├── delhi_high_court_scraper.py   # Core scraping logic (uses Selenium)
├── utils.py                       # Case table + order link extraction
├── database.py                    # SQLite init, insert, and teardown
├── templates/
│   ├── index.html                 # Case form page
│   └── result.html                # Case results
├── requirements.txt
└── README.md
```

---

## 🧩 File Roles

- **`app.py`**: Runs the Flask app, manages routing and form submission
- **`delhi_high_court_scraper.py`**: Automates form filling, CAPTCHA solving, and result submission
- **`utils.py`**: Parses the result HTML to extract structured case data
- **`database.py`**: Manages SQLite connection and logs raw HTML from each query
- **`templates/`**: Contains Jinja2-based HTML templates for form and result pages

---

## 🧪 Sample Code Snippets

#### 📦 Form Filling with CAPTCHA:
```python
captcha_value = driver.find_element(By.ID, "captcha-code").text.strip()
driver.find_element(By.ID, "captchaInput").send_keys(captcha_value)
```

#### 🔍 Extract Table Using `utils.py`:
```python
from utils import extract_case_table
cases = extract_case_table(driver.page_source, driver)
```

---

## 📝 License

This project is licensed under the **MIT License**.
