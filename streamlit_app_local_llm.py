import streamlit as st
import ollama

# streamlit run yourscript.py
st.set_page_config(page_title = 'Chat with your Local LLM')

with st.sidebar:
    st.title('💬 You first chatBot!')
    st.write("Ask me anything")

    st.subheader('Specify your Model and parameter ')
    selected_model = st.sidebar.selectbox('Choose a local model', ['llama3.1', 'llama2','mistral'], key='selected_model')

    st.markdown('You have chosen your model and parameters:')
    st.markdown(f"{selected_model}")

# Initialize chat
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages - history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat messages history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

st.sidebar.subheader('Manage your chat history')  
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def chat_history(model, messages):
    response = ollama.chat(model=model, messages = messages)
    return response['message']['content']


if prompt := st.chat_input("Your are chatting with local LLM"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_history(selected_model, st.session_state.messages)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)