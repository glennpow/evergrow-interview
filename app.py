
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from fpdf import FPDF


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]asdf/'


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        content = request.form["content"]

        def parse_number(input):
            try:
                return float(input)
            except ValueError:
                return None

        entries = [parse_number(line.strip()) for line in content.split("\n")]
        entries = [entry for entry in entries if entry]

        if len(entries) == 0:
            flash("No numerical entries received!")
            return redirect(url_for("index"))
        print(f"Exporting PDF ({len(entries)} entries)")

        return export_pdf(entries)
    return render_template("index.html")


@app.route("/export")
def export_pdf(entries):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=18)
    pdf.cell(200, 10, txt="Evergrow", ln=1, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Numerical Entries:", ln=2, align="L")
    for i, entry in enumerate(entries):
        pdf.cell(200, 10, txt=f"[{i}] {entry}", ln=i + 3, align="L")

    filename = "result.pdf"
    #pdf.output(filename)

    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set("Content-Disposition", "attachment", filename=filename)
    response.headers.set("Content-Type", "application/pdf")
    return response


if (__name__ == "__main__"):
    app.run()
