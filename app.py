import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from langchain_openai import ChatOpenAI
from pandasai.responses.streamlit_response import StreamlitResponse
import os,glob
from langchain_google_genai import ChatGoogleGenerativeAI
pwd=os.getcwd()
from dotenv import load_dotenv
import os
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)
st.title(" ⚛ Data Analysis And Visualization Tool 📶")
st.sidebar.title("AnalyzeX 📶")
st.sidebar.header("𝐖𝐄𝐋𝐂𝐎𝐌𝐄 🤗")
st.sidebar.title("About This Tool")

st.sidebar.write("""
Welcome to **AnalyzeX** – your ultimate solution for data analysis and visualization.  
Upload your datasets and gain instant insights with:  
- Comprehensive analysis  
- Interactive visualizations  
- User-friendly interface  
""")

file = st.sidebar.file_uploader("Upload your file in XLSV or CSV", type=["xlsx", "csv"])


def query_enhancer(user_query, columns):
    """
    Enhance the user query based on the columns of the dataframe.
    If a column name is part of the user's query, replace it with the actual column name.
    """
    enhanced_query = user_query
    for column in columns:
        if column.lower() in user_query.lower():  # case-insensitive match
            enhanced_query = enhanced_query.replace(column.lower(), column)
    return enhanced_query


if file:
    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine="openpyxl")  # Specify the engine for Excel files
        elif file.name.endswith('.csv'):
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding='latin1')  # Handle alternate encodings
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        st.stop()

    
    sdf = SmartDataframe(df,
                         config={"llm": llm, "response_parser": StreamlitResponse, "save_charts": True,
                                 "save_charts_path": os.getcwd()})

    columns = df.columns.tolist()
    options = ["chat", "plot"]
    selected_option = st.selectbox("Choose an option", options)

    if selected_option == "chat":
        query_type = st.selectbox("Choose a query type", ["Type Your Message"])

        if query_type == "Type Your Message":
            user_input = st.text_area("Ask your question here")
            if user_input:
                enhanced_query = query_enhancer(user_input, columns)
                btn = st.button("Submit")

                if btn:
                    response = sdf.chat(enhanced_query)
                    st.write(response)

    if (selected_option=="plot"):
        user_input = st.text_area("Ask your question here for plotting")
        if user_input:
                enhanced_query = query_enhancer(user_input, columns)
                btn = st.button("Submit")
            
                if btn:
                    response = sdf.chat(enhanced_query)
                    file = glob.glob(os.getcwd() + "/*.png")
                    if file:
                        st.image(image=file[0], caption="Plot for: " + user_input, width=1024)
   
                