import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("📊 Gemini Chat with Data + Dictionary")

# 1. Insert API Key
st.subheader("1. Insert Gemini API Key")
gemini_api_key = st.text_input("Gemini API Key", placeholder="Paste your API Key here...", type="password")

model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        # model = genai.GenerativeModel("gemini-pro")
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

        st.success("✅ API Key configured successfully.")
    except Exception as e:
        st.error(f"❌ Error setting up Gemini model: {e}")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "data_dict" not in st.session_state:
    st.session_state.data_dict = None
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# 2. Upload Data Dictionary
st.subheader("2. Upload Data Dictionary (CSV or Excel)")
dict_file = st.file_uploader("Upload a data dictionary file", type=["csv", "xlsx"])

if dict_file is not None:
    try:
        if dict_file.name.endswith(".csv"):
            st.session_state.data_dict = pd.read_csv(dict_file)
        else:
            st.session_state.data_dict = pd.read_excel(dict_file)
        st.success("📘 Data dictionary loaded.")
        st.dataframe(st.session_state.data_dict)
    except Exception as e:
        st.error(f"❌ Could not read data dictionary: {e}")

# 3. Upload Main Data
st.subheader("3. Upload Main Data (CSV only)")
data_file = st.file_uploader("Upload your main dataset", type=["csv"])

if data_file is not None:
    try:
        st.session_state.uploaded_data = pd.read_csv(data_file)
        st.success("📁 Data file loaded.")
        st.write("### Data Example")
        st.dataframe(st.session_state.uploaded_data.head())
    except Exception as e:
        st.error(f"❌ Could not read main data file: {e}")

# 4. Ask the Bot
st.subheader("4. Ask the AI (Chatbot)")

if prompt := st.chat_input("Type your question..."):
    st.session_state.chat_history.append(("user", prompt))
    st.chat_message("user").markdown(prompt)

    if model:
        try:
            # Add context if data exists
            context = ""
            if st.session_state.uploaded_data is not None:
                context += "\n\nData Preview:\n" + st.session_state.uploaded_data.to_string()
            if st.session_state.data_dict is not None:
                context += "\n\nData Dictionary:\n" + st.session_state.data_dict.to_string()

            full_prompt = f"{prompt}\n\n{context}"

            response = model.generate_content(full_prompt)
            reply = response.text

            print(full_prompt)
            st.session_state.chat_history.append(("assistant", reply))
            st.chat_message("assistant").markdown(reply)

        except Exception as e:
            st.error(f"❌ Error during response: {e}")
    else:
        st.warning("⚠️ Please enter a valid Gemini API key.")

# Show chat history
for role, msg in st.session_state.chat_history:
    if role != "user":
        st.chat_message(role).markdown(msg)
