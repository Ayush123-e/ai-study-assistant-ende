import streamlit as st
from rag import rag_pipeline

st.set_page_config(page_title="AI Study Assistant", layout="wide")

st.title("📚 AI Study Assistant")
st.write("Ask questions about AI, Machine Learning, DevOps, and Data Science.")

# User input
query = st.text_input("Enter your question:")

if st.button("Search"):

    if query.strip() == "":
        st.warning("Please enter a question.")
    else:

        answer, results = rag_pipeline(query)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Top Relevant Documents")

        for r in results:
            st.write("Score:", r["score"])
            st.write(r["metadata"]["text"])
            st.write("---")
