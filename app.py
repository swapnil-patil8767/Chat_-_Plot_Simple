import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse
import os, glob
from dotenv import load_dotenv

# Import ChatGroq instead of ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # It's better to store your Groq API key in .env

# Initialize the LLM using ChatGroq
llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,  # Use the Groq API key from environment variables
    model_name="llama-3.1-70b-versatile"
)

st.title("SalesPulse Analytics 📶")

st.sidebar.title("SalesPulse Analytics 📶")
st.sidebar.header("𝐖𝐄𝐋𝐂𝐎𝐌𝐄 🤗")
st.sidebar.title("About This Tool")
st.sidebar.write("This tool is designed specifically for **Sales Analytics** for **Small Enterprises**. ")
st.sidebar.write("Features include:")
st.sidebar.markdown("- Detailed insights 📈")
st.sidebar.markdown("- Visualizations 📊")
st.sidebar.markdown("- Customized reports 📝")
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

        elif query_type == "Sales vs Profit":
            user_input = "Sales vs Profit"  # Predefined query for Sales vs Profit
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                st.write(response)

        elif query_type == "Date vs Profit":
            user_input = "Date vs Profit"  # Predefined query for Date vs Profit
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                st.write(response)

    elif selected_option == "plot":
        query_type = st.selectbox("Choose a plot query type", ["Type Your Message", "Sales vs Profit", "Date vs Profit","Product Category vs Sales","Product Category vs Profit","date vs Sales","Product Category vs Margin"])

        if query_type == "Type Your Message":
            user_input = st.text_area("Ask your question here for plotting")
            if user_input:
                enhanced_query = query_enhancer(user_input, columns)
                btn = st.button("Submit")

                if btn:
                    response = sdf.chat(enhanced_query)
                    file = glob.glob(os.getcwd() + "/*.png")
                    if file:
                        st.image(image=file[0], caption="Plot for: " + user_input, width=1024)

        elif query_type == "Sales vs Profit":
            user_input = "Sales vs Profit"  # Predefined query for Sales vs Profit plotting
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                file = glob.glob(os.getcwd() + "/*.png")
                if file:
                    st.image(image=file[0], caption="Plot for: " + user_input, width=1024)

        elif query_type == "Date vs Profit":
            user_input = "Date vs Profit"  # Predefined query for Date vs Profit plotting
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                file = glob.glob(os.getcwd() + "/*.png")
                if file:
                    st.image(image=file[0], caption="Plot for: " + user_input, width=1024)

        
        elif query_type == "Product Category vs Sales":
            user_input = "Product Category vs Sales"  # Predefined query for Date vs Profit plotting
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                file = glob.glob(os.getcwd() + "/*.png")
                if file:
                    st.image(image=file[0], caption="Plot for: " + user_input, width=1024)

        elif query_type == "Product Category vs Profit":
            user_input = "Product Category vs Profit"  # Predefined query for Date vs Profit plotting
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                file = glob.glob(os.getcwd() + "/*.png")
                if file:
                    st.image(image=file[0], caption="Plot for: " + user_input, width=1024)
        

        elif query_type == "date vs Sales":
            user_input = "Date vs Sales"  # Predefined query for Date vs Profit plotting
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                file = glob.glob(os.getcwd() + "/*.png")
                if file:
                    st.image(image=file[0], caption="Plot for: " + user_input, width=1024)

        elif query_type == "Product Category vs Margin":
            user_input = "Product Category vs Margin"  # Predefined query for Date vs Profit plotting
            enhanced_query = query_enhancer(user_input, columns)
            btn = st.button("Submit")

            if btn:
                response = sdf.chat(enhanced_query)
                file = glob.glob(os.getcwd() + "/*.png")
                if file:
                    st.image(image=file[0], caption="Plot for: " + user_input, width=1024)
