import openai
import PyPDF2
import streamlit as st
import base64


# Initialize connection.
def init_connection():
    openai.api_key = st.secrets["openai"]['apikey']


prompt = '''You are Smart AI working on technical drawing data of mechanical part \
            analysis the information from the random text data \
            specially raw material, part weight and quanity data \
            give information in JSON format
            '''

def extract_information_from_pdf(uploaded_file):
    with uploaded_file as file:
        file_content = file.read()
        # Embedding PDF in HTML
        base64_pdf = base64.b64encode(file_content).decode("utf-8")

        # Embedding PDF in HTML
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1200" height="900" type="application/pdf">'
        pdf_reader = PyPDF2.PdfReader(file)
        text ={}
        page_len = len(pdf_reader.pages)
        for i in range(page_len):
            text[f"Page no {i}"] = pdf_reader.pages[i].extract_text()
        return text, pdf_display
    
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def context_(prompt , data):
    context = [ {'role':'system', 'content':f"""
                    {prompt}
                    here is the raw data: '''{data}'''
                    """} ]
    
    return context

def full_context_parser(prompt , data):
    res = {}
    
    if len(data) > 1:
        for i in range(len(data)):
            if data[f'Page no {i}'] == '':
                res[f'Page no {i}'] =  context_(prompt,"data is not there")
            else:
                res[f'Page no {i}'] = context_(prompt,data[f'Page no {i}'])
    
    if len(data) == 1:
        if data['Page no 0'] == '':
            res['Page no 0'] =  context_(prompt,"data is not there")
            # print ("data is not there")
        else:
            res[f'Page no 0'] =  context_(prompt,data['Page no 0'])

    return res


def gpt_response(prompt_data):
    res = {}
    init_connection()
    if len(prompt_data) > 1:
        for i in range(len(prompt_data)):
            if "data is not there" in prompt_data[f'Page no {i}'][0]['content'] :
                # print("_mul"*50)
                # print(prompt_data[f'Page no {i}'])
                # print("_"*50)
                res[f'Page no {i}'] =  "data is not there"
            else:
                # print("_sub__"*50)
                # print(prompt_data[f'Page no {i}'][0])
                # print("_"*50)
                res[f'Page no {i}'] = get_completion_from_messages(prompt_data[f'Page no {i}'])
    
    if len(prompt_data) == 1:
        if "data is not there" in prompt_data['Page no 0'][0]['content']:
            res[f'Page no {i}'] =  "data is not there"
            # print("_add"*50)
            # print (prompt_data['Page no 0'][0])
            # print("_"*50)
        else:
            # print("_error"*50)
            # print(prompt_data['Page no 0'])
            # print(type(prompt_data['Page no 0']))
            # print("_"*50) 
            res[f'Page no 0'] =  get_completion_from_messages(prompt_data['Page no 0'])
    return res
