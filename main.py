import streamlit as st
from utilites import *




st.set_page_config(page_title="File Uploader", page_icon=":clipboard:", layout="wide")

tab1,tab2 = st.tabs(["PDF Txt Extraction","No code"])

with tab1:

    if "visibility" not in st.session_state:
            st.session_state.visibility = "visible"
            st.session_state.disabled = True

    st.checkbox("Edit Prompt", key="disabled")

    with st.form(key='columns_in_form'):
        c1, c2 = st.columns(2)
        with c1:
            pdf_file = st.file_uploader("Choose a 2D Design File", type=["pdf"])
        with c2:
            prompt = st.text_input("prompt data",value = prompt,label_visibility=st.session_state.visibility,disabled=st.session_state.disabled)

        submitButton = st.form_submit_button(label = 'Calculate')

    if pdf_file is not None:
        
        raw_txt,pdf_display = extract_information_from_pdf(pdf_file)
        context_parsed = full_context_parser(prompt,raw_txt)
        ai_responses = gpt_response(context_parsed)

        st.write(raw_txt)
        # st.write(context_parsed)
        st.write(ai_responses)

        # Display the PDF in the Streamlit app
        st.markdown(pdf_display, unsafe_allow_html=True)
