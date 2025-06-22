
import streamlit as st
import pandas as pd
from multi_bank_parser import parse_pdf_by_bank

st.set_page_config(page_title="ReceiptsPro", layout="wide")
st.title("ReceiptsPro: PDF Statement Parser")
st.caption("🔒 Your uploaded file is processed temporarily and not stored permanently. For personal use only.")

uploaded_file = st.file_uploader("Upload your bank statement PDF", type="pdf")

if uploaded_file is not None:
    df, message = parse_pdf_by_bank(uploaded_file)

    if df.empty:
        st.warning(message)
    else:
        st.subheader("📝 Edit Your Transactions")
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if "Location & Category" in edited_df.columns:
            edited_df["Cleaned Category"] = edited_df["Location & Category"].apply(lambda x: x.split()[-1])
            category_summary = edited_df.groupby("Cleaned Category")["Amount ($)"].sum().reset_index()
            st.subheader("📊 Spending Summary by Category")
            st.dataframe(category_summary, use_container_width=True)
        else:
            st.info("📎 No category data available for this bank format.")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=edited_df.to_csv(index=False),
            file_name="cleaned_transactions.csv",
            mime="text/csv"
        )
