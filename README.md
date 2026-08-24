# PDF Invoice Generator

![Build](https://github.com/jjortiz-lpd/pdf-invoice-generator/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

Turns one CSV of line items into professional, branded PDF invoices — one
per client, fully automated, in about a second.

## The problem

A freelancer or small business re-types the same invoice template for every
client every month, manually totaling line items and exporting each one to
PDF by hand.

## What the script does

1. Reads `invoice_data.csv` — all clients' line items in one file
2. Groups rows by invoice number
3. Generates a clean, branded PDF per invoice — header, bill-to block,
   itemized table, subtotal/tax/total — using `reportlab`

Three sample invoices are included in [`invoices/`](invoices) so you can see
the output without running anything.

## Skills demonstrated

- Python (`pandas`, `reportlab`)
- PDF generation and page layout
- Templating a recurring business document from tabular data

## Run it yourself

```bash
pip install -r requirements.txt
python generate_invoices.py
```

Output: `invoices/INV-1001.pdf`, `invoices/INV-1002.pdf`, `invoices/INV-1003.pdf`.
A GitHub Actions workflow (see the badge above) runs this exact command
against the sample CSV on every push.

## Project structure

```
pdf-invoice-generator/
├── generate_invoices.py   # reads the CSV, groups by invoice, renders each PDF
├── invoice_data.csv       # sample line items for 3 clients
├── invoices/               # sample output PDFs
├── requirements.txt
└── .github/workflows/ci.yml
```

## Adapting this for a client

- Edit the `YOUR_BUSINESS` dict at the top of `generate_invoices.py` (or make it read from the client's own business info)
- Set `TAX_RATE` if the client needs to charge tax
- Point `CSV_PATH` at their real export — from QuickBooks, a Google Sheet, or wherever their client/billing data already lives

## License

MIT — see [LICENSE](LICENSE).
