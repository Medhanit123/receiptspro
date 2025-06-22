
import pdfplumber
import re
import pandas as pd

def detect_bank(pdf):
    text_preview = ""
    with pdfplumber.open(pdf) as pdf_file:
        for page in pdf_file.pages[:1]:
            text_preview += page.extract_text()
    if "CIBC" in text_preview:
        return "CIBC"
    elif "TD Canada Trust" in text_preview or "TD" in text_preview:
        return "TD"
    elif "BMO" in text_preview or "Bank of Montreal" in text_preview:
        return "BMO"
    elif "Scotiabank" in text_preview or "Scotia" in text_preview:
        return "Scotiabank"
    elif "Royal Bank of Canada" in text_preview or "RBC" in text_preview:
        return "RBC"
    else:
        return "Unknown"

def parse_pdf_by_bank(pdf):
    bank = detect_bank(pdf)
    if bank == "CIBC":
        return parse_cibc(pdf)
    elif bank == "TD":
        return parse_td(pdf)
    elif bank == "BMO":
        return parse_bmo(pdf)
    elif bank == "Scotiabank":
        return parse_scotiabank(pdf)
    elif bank == "RBC":
        return parse_rbc(pdf)
    else:
        return pd.DataFrame(), "Unsupported bank or unrecognized format."

# Example stub parsers (only CIBC implemented so far)
def parse_cibc(pdf):
    transactions = []
    with pdfplumber.open(pdf) as pdf_file:
        for page in pdf_file.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    match = re.match(r"([A-Z][a-z]{2} \d{2})\s+([A-Z][a-z]{2} \d{2})\s+(.+?)\s{2,}(.+?)\s+([\d,]+\.\d{2})$", line)
                    if match:
                        trans_date, post_date, description, location_category, amount = match.groups()
                        transactions.append({
                            "Transaction Date": trans_date,
                            "Post Date": post_date,
                            "Description": description.strip(),
                            "Location & Category": location_category.strip(),
                            "Amount ($)": float(amount.replace(',', ''))
                        })
    return pd.DataFrame(transactions)

def parse_td(pdf):
    # Placeholder for TD parser logic
    return pd.DataFrame()

def parse_bmo(pdf):
    # Placeholder for BMO parser logic
    return pd.DataFrame()

def parse_scotiabank(pdf):
    # Placeholder for Scotiabank parser logic
    return pd.DataFrame()

def parse_rbc(pdf):
    # Placeholder for RBC parser logic
    return pd.DataFrame()

