import streamlit as st
import backend

st.set_page_config(page_title="Assignment Harshwal Consulting Services")
st.title("Harshwal Consulting Services , Assignment ")
st.write("Upload a PDF and ask questions from its content.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    try:
        message = backend.process_pdf(uploaded_file)
        st.success(message)

        question = st.text_input("Ask a question about the PDF content:")

        if st.button("Search"):
            if question:
                with st.spinner("Generating answer..."):
                    answer = backend.answer_question(question)
                st.subheader("Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question first.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("Please upload a PDF to begin.")
