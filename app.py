import streamlit as st
import pandas as pd
from utils import ask_llm
import os
from chart_generator import generate_chart

st.set_page_config(page_title="Excel Analyst AI")

st.title("📊 Excel Analyst AI")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file is not None:
    os.makedirs("temp", exist_ok=True)

    file_path = os.path.join("temp", uploaded_file.name)

if uploaded_file:
    df = pd.read_excel(file_path)

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # Show columns
    st.write("### Columns:", list(df.columns))

    # ------------------------
    # 💬 Ask Question
    # ------------------------
    query = st.text_input("Ask question about your data")

    if query:
        prompt = f"""
        You are a data analyst.
        Given this dataset columns: {list(df.columns)}

        Answer this question:
        {query}
        """

        answer = ask_llm(prompt)

        st.subheader("🤖 AI Answer")
        st.write(answer)

    # ------------------------
    # 📊 Chart Section
    # ------------------------
    st.subheader("📊 Generate Chart")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["bar", "line", "pie"]
    )

    x_col = st.selectbox("Select X-axis", df.columns)
    y_col = st.selectbox("Select Y-axis", df.columns)

    if st.button("Generate Chart"):
        chart = generate_chart(df, chart_type, x_col, y_col)
        st.pyplot(chart)