import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


st.title('"Chatbpox')

with st.sidebar:
    st.title('Huggingface Account')
    hf_email = st.text_input('E-mail')
    hf_pass = st.text_input('Password', type='password')

if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {'role': 'assistant', 'content': 'How may I help you'}]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])


def generate_response(promt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create chatbox
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(promt_input)


if promt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({'role': 'user', 'content': promt})
    with st.chat_message('user'):
        st.write(promt)

# Generation a new response if last message is not from assistant
if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        with st.spinner("Thinking ..."):
            response = generate_response(promt, hf_email, hf_pass)
            st.write(response)
        message = {'role': 'assistant', 'content': response}
        st.session_state.messages.append(message)
