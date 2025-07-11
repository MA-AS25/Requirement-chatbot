import streamlit as st
import openai
import pandas as pd
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the Excel data
df = pd.read_excel("List.xlsx")

# App title
st.set_page_config(page_title="3D Printer Chatbot with ChatGPT")
st.write("Ask me about a 3D printer part or function for which you would like to know the requirements:")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    submitted = st.form_submit_button("Send")

# If submitted, process user input
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare Excel context string
    context = ""
    for _, row in df.iterrows():
        context += f"{row['Title']} ({row['Part name']}): {row['Description']}\n"

    # Call ChatGPT API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant for 3D printer specifications. Here are the known details:\n\n{context}"},
            *st.session_state.messages
        ]
    )

    reply = response['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")
