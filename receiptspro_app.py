
import streamlit as st
import pandas as pd
import pdfplumber
import re

st.set_page_config(page_title="ReceiptsPro", layout="wide")
st.title("ReceiptsPro: PDF Statement Parser")
st.caption("🔒 Your uploaded file is processed temporarily and not stored permanently. For personal use only.")

uploaded_file = st.file_uploader("Upload your bank statement PDF", type="pdf")

def extract_transactions_from_pdf(file):
    transactions = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
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

if uploaded_file is not None:
    df = extract_transactions_from_pdf(uploaded_file)
    st.subheader("📝 Edit Your Transactions")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    st.subheader("📊 Spending Summary by Category")
    edited_df["Cleaned Category"] = edited_df["Location & Category"].apply(lambda x: x.split()[-1])
    category_summary = edited_df.groupby("Cleaned Category")["Amount ($)"].sum().reset_index()
    st.dataframe(category_summary, use_container_width=True)

    st.download_button(
        label="📥 Download Cleaned CSV",
        data=edited_df.to_csv(index=False),
        file_name="cleaned_transactions.csv",
        mime="text/csv"
    )
