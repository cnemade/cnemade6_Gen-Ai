import streamlit as st
import os
import pandas as pd

from rag_Pipeline import (
    load_pdf,
    load_excel,
    split_docs,
    create_vector_store,
    create_rag_chain
)

from chart_generator import generate_chart

st.set_page_config(page_title="RAG App", layout="wide")
st.title("📄 RAG App (PDF + Excel + Ollama)")

uploaded_file = st.file_uploader("Upload file", type=["pdf", "xlsx"])

if uploaded_file is not None:
    # ------------------------
    # 📁 Save File
    # ------------------------
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    # ------------------------
    # 📄 Load Docs
    # ------------------------
    if uploaded_file.name.endswith(".pdf"):
        docs = load_pdf(file_path)
        df = None  # No DataFrame for PDF
    else:
        docs = load_excel(file_path)
        df = pd.read_excel(file_path)

    # ------------------------
    # ✂️ Split Docs
    # ------------------------
    chunks = split_docs(docs)

    if not chunks:
        st.error("No content extracted from file!")
        st.stop()

    # ------------------------
    # 🧠 RAG Pipeline
    # ------------------------
    db = create_vector_store(chunks)
    rag = create_rag_chain(db)

    # ------------------------
    # 💬 Query Section
    # ------------------------
    query = st.text_input("Ask a question")

    if query:
        with st.spinner("Thinking..."):
            answer = rag(query)

        st.subheader("### Answer:")
        st.write(answer)

    # ------------------------
    # 📊 Chart Section (Excel only)
    # ------------------------
    if df is not None:
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