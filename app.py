from flask import Flask, render_template, request
from delhi_high_court_scraper import fetch_case_data
from database import log_query

app = Flask(__name__)

@app.route('/')
def index():
    # full list of case types
    case_types = [
        "ADMIN.REPORT", "ARB.A.", "ARB. A. (COMM.)", "ARB.P.", "BAIL APPLN.", "CA", "CA (COMM.IPD-CR)",
        "C.A.(COMM.IPD-GI)", "C.A.(COMM.IPD-PAT)", "C.A.(COMM.IPD-PV)", "C.A.(COMM.IPD-TM)", "CAVEAT(CO.)",
        "CC(ARB.)", "CCP(CO.)", "CCP(REF)", "CEAC", "CEAR", "CHAT.A.C.", "CHAT.A.REF", "CMI", "CM(M)",
        "CM(M)-IPD", "C.O.", "CO.APP.", "CO.APPL.(C)", "CO.APPL.(M)", "CO.A(SB)", "C.O.(COMM.IPD-CR)",
        "C.O.(COMM.IPD-GI)", "C.O.(COMM.IPD-PAT)", "C.O. (COMM.IPD-TM)", "CO.EX.", "CONT.APP.(C)",
        "CONT.CAS(C)", "CONT.CAS.(CRL)", "CO.PET.", "C.REF.(O)", "CRL.A.", "CRL.L.P.", "CRL.M.C.",
        "CRL.M.(CO.)", "CRL.M.I.", "CRL.O.", "CRL.O.(CO.)", "CRL.REF.", "CRL.REV.P.", "CRL.REV.P.(MAT.)",
        "CRL.REV.P.(NDPS)", "CRL.REV.P.(NI)", "C.R.P.", "CRP-IPD", "C.RULE", "CS(COMM)", "CS(OS)", "CS(OS) GP",
        "CUSAA", "CUS.A.C.", "CUS.A.R.", "CUSTOM A.", "DEATH SENTENCE REF.", "DEMO", "EDC", "EDR",
        "EFA(COMM)", "EFA(OS)", "EFA(OS)  (COMM)", "EFA(OS)(IPD)", "EL.PET.", "ETR", "EX.F.A.", "EX.P.",
        "EX.S.A.", "FAO", "FAO (COMM)", "FAO-IPD", "FAO(OS)", "FAO(OS) (COMM)", "FAO(OS)(IPD)", "GCAC",
        "GCAR", "GTA", "GTC", "GTR", "I.A.", "I.P.A.", "ITA", "ITC", "ITR", "ITSA", "LA.APP.", "LPA",
        "MAC.APP.", "MAT.", "MAT.APP.", "MAT.APP.(F.C.)", "MAT.CASE", "MAT.REF.", "MISC. APPEAL(PMLA)",
        "OA", "OCJA", "O.M.P.", "O.M.P. (COMM)", "OMP (CONT.)", "O.M.P. (E)", "O.M.P. (E) (COMM.)",
        "O.M.P.(EFA)(COMM.)", "OMP (ENF.) (COMM.)", "O.M.P.(I)", "O.M.P.(I) (COMM.)", "O.M.P. (J) (COMM.)",
        "O.M.P. (MISC.)", "O.M.P.(MISC.)(COMM.)", "O.M.P.(T)", "O.M.P. (T) (COMM.)", "O.REF.", "RC.REV.",
        "RC.S.A.", "RERA APPEAL", "REVIEW PET.", "RFA", "RFA(COMM)", "RFA-IPD", "RFA(OS)", "RFA(OS)(COMM)",
        "RF(OS)(IPD)", "RSA", "SCA", "SDR", "SERTA", "ST.APPL.", "STC", "ST.REF.", "SUR.T.REF.", "TEST.CAS.",
        "TR.P.(C)", "TR.P.(C.)", "TR.P.(CRL.)", "VAT APPEAL", "W.P.(C)", "W.P.(C)-IPD", "WP(C)(IPD)",
        "W.P.(CRL)", "WTA", "WTC", "WTR"
    ]

    return render_template("index.html", case_types=case_types)


@app.route('/result', methods=['POST'])
def result():
    print("PRINTED FROM RESULT")
    case_type = request.form['case_type']
    case_number = request.form['case_number']
    year = request.form['year']
    
    data = fetch_case_data(case_type, case_number, year)

    return render_template('result.html', results=data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

