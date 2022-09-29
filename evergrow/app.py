
from flask import Flask, flash, make_response, redirect, render_template, request, url_for
from fpdf import FPDF


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]asdf/'


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        content = request.form["content"]

        try:
            entries = parse_entries(content)
        except ValueError as e:
            flash(str(e))
            return redirect(url_for("index"))
        print(f"Exporting PDF ({len(entries)} entries)")

        pdf = format_pdf(entries)

        filename = "result.pdf"
        response = make_response(pdf)
        response.headers.set("Content-Disposition", "attachment", filename=filename)
        response.headers.set("Content-Type", "application/pdf")
        return response
    return render_template("index.html")


def parse_entries(content):
    def parse_entry(input):
        try:
            return float(input)
        except ValueError:
            return None

    entries = [parse_entry(line.strip()) for line in content.split("\n")]
    entries = [entry for entry in entries if entry]

    if len(entries) == 0:
        raise ValueError("No numerical entries received!")

    return entries


def format_pdf(entries):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=18)
    pdf.cell(200, 10, txt="Evergrow", ln=1, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Numerical Entries:", ln=2, align="L")
    for i, entry in enumerate(entries):
        pdf.cell(200, 10, txt=f"[{i}] {entry}", ln=i + 3, align="L")

    return pdf.output(dest="S").encode("latin-1")


if (__name__ == "__main__"):
    app.run()
