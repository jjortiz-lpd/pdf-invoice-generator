"""
generate_invoices.py
---------------------
Real-world problem this solves:
    A freelancer/small business has several clients each month and is
    manually copy-pasting a Word/Excel invoice template for every one -
    updating line items, re-totaling by hand, and exporting to PDF one
    at a time.

What this script does:
    Reads a single CSV export (invoice_data.csv) containing line items
    for ALL clients, groups them by invoice number, and generates one
    clean, professional PDF invoice per client - fully automated.

Run:
    python3 generate_invoices.py
Output:
    invoices/INV-1001.pdf, invoices/INV-1002.pdf, ...

Customize:
    - Edit YOUR_BUSINESS below with your own name/contact details.
    - Change TAX_RATE if you need to charge tax.
    - Swap invoice_data.csv for your own export (same column names).
"""
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "invoice_data.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "invoices")

YOUR_BUSINESS = {
    "name": "Juan José Ortiz / Hope",
    "tagline": "Python & Excel Automation Services",
    "email": "juanjortiz016@gmail.com",
    "location": "Bogota, Colombia",
}

TAX_RATE = 0.0  # e.g. 0.19 for 19% VAT - set to 0 if not applicable

ACCENT = colors.HexColor("#1F4E78")
LIGHT_GREY = colors.HexColor("#F2F2F2")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("InvoiceTitle", parent=styles["Title"], textColor=ACCENT,
                              fontSize=26, alignment=2, spaceAfter=0)
label_style = ParagraphStyle("Label", parent=styles["Normal"], fontSize=9,
                              textColor=colors.grey)
normal = styles["Normal"]
biz_name_style = ParagraphStyle("BizName", parent=styles["Normal"], fontSize=14,
                                 textColor=ACCENT, leading=17)


def build_invoice_pdf(invoice_number, rows):
    first = rows.iloc[0]
    out_path = os.path.join(OUTPUT_DIR, f"{invoice_number}.pdf")
    doc = SimpleDocTemplate(out_path, pagesize=letter,
                             topMargin=0.6 * inch, bottomMargin=0.6 * inch,
                             leftMargin=0.6 * inch, rightMargin=0.6 * inch)
    story = []

    # --- header: business info left, "INVOICE" + number right ---
    header_data = [[
        Paragraph(f"<b>{YOUR_BUSINESS['name']}</b><br/>{YOUR_BUSINESS['tagline']}"
                  f"<br/>{YOUR_BUSINESS['email']}<br/>{YOUR_BUSINESS['location']}", normal),
        Paragraph(f"<para align='right'><font size=24 color='#1F4E78'><b>INVOICE</b></font>"
                  f"<br/><font size=11>{invoice_number}</font></para>", normal),
    ]]
    header_table = Table(header_data, colWidths=[3.5 * inch, 3.5 * inch])
    header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(header_table)
    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", color=ACCENT, thickness=1.2))
    story.append(Spacer(1, 14))

    # --- bill-to / dates ---
    bill_to = Paragraph(
        f"<font size=9 color='grey'>BILL TO</font><br/>"
        f"<b>{first['Client Name']}</b><br/>{first['Client Address']}<br/>{first['Client Email']}",
        normal,
    )
    dates = Paragraph(
        f"<font size=9 color='grey'>INVOICE DATE</font><br/><b>{first['Invoice Date']}</b>"
        f"<br/><br/><font size=9 color='grey'>DUE DATE</font><br/><b>{first['Due Date']}</b>",
        normal,
    )
    info_table = Table([[bill_to, dates]], colWidths=[4.2 * inch, 2.8 * inch])
    info_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(info_table)
    story.append(Spacer(1, 22))

    # --- line items table ---
    table_data = [["Description", "Qty", "Unit Price", "Amount"]]
    subtotal = 0.0
    for _, r in rows.iterrows():
        qty = float(r["Quantity"])
        price = float(r["Unit Price"])
        amount = qty * price
        subtotal += amount
        table_data.append([
            r["Description"], f"{qty:g}", f"${price:,.2f}", f"${amount:,.2f}"
        ])

    tax = subtotal * TAX_RATE
    total = subtotal + tax

    table_data.append(["", "", "Subtotal", f"${subtotal:,.2f}"])
    if TAX_RATE > 0:
        table_data.append(["", "", f"Tax ({TAX_RATE * 100:.0f}%)", f"${tax:,.2f}"])
    table_data.append(["", "", "TOTAL DUE", f"${total:,.2f}"])

    n_items = len(rows)
    line_table = Table(table_data, colWidths=[3.4 * inch, 0.7 * inch, 1.4 * inch, 1.5 * inch])
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, n_items), [colors.white, LIGHT_GREY]),
        ("LINEBELOW", (0, 0), (-1, 0), 1, ACCENT),
        ("FONTNAME", (2, n_items + 1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (2, n_items + 1), (-1, n_items + 1), 0.75, colors.grey),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    line_table.setStyle(TableStyle(style))
    story.append(line_table)
    story.append(Spacer(1, 30))

    story.append(HRFlowable(width="100%", color=colors.lightgrey, thickness=0.75))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<font size=9 color='grey'>Thank you for your business! "
        "Payment can be made via bank transfer or the link provided separately.</font>",
        normal,
    ))

    doc.build(story)
    return out_path


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(CSV_PATH)
    generated = []
    for invoice_number, rows in df.groupby("Invoice Number"):
        path = build_invoice_pdf(invoice_number, rows)
        generated.append(path)
        print(f"Generated {path}")
    print(f"\n{len(generated)} invoice(s) created in '{OUTPUT_DIR}/'")


if __name__ == "__main__":
    main()
