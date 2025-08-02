from flask import Flask, render_template, request
from court_scraper import fetch_case_data
from database import log_query

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    case_type = request.form['case_type']
    case_number = request.form['case_number']
    year = request.form['year']
    
    data = fetch_case_data(case_type, case_number, year)
    log_query(case_type, case_number, year, str(data))

    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

