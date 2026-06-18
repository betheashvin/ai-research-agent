from flask import Flask, render_template, request, redirect, send_file
from dotenv import load_dotenv

load_dotenv()

from services.research import research_topic
from database import init_db, save_report, get_report, get_reports, delete_report

init_db()
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    report = None

    if request.method == "POST":
        topic = request.form["topic"]
        report = research_topic(topic)
        save_report(topic, report)
    
    return render_template('index.html', report=report)

@app.route("/history")
def history():
    reports = get_reports()
    return render_template("history.html", reports=reports)

@app.route('/report/<int:id>')
def report_page(id):
    report = get_report(id)

    return render_template("report.html", report=report)

@app.route("/delete/<int:id>")
def delete(id):

    delete_report
    redirect("/history")

@app.route("/export/<int:id>")
def export(id):
    report = get_report(id)
    filename = f"{report[1].md}"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report[2])
    
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
