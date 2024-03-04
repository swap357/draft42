""" Main application file for the Streamlit app. """

import streamlit as st
from utils.gpt import GPTModelManager
from utils.conversation import Conversation
from utils.utils import get_help, clear_chat, about_app
from tools.tools import Tools

system_message = """
    You are a snarky, highly intelligent chatbot.\
    Your name is Draft42, a reference to the meaning of life, the universe, and everything.\
    You were created by Swapnil Patel, a software engineer and ML enthusiast.\
    You are also here to make them make them think about the world in a totally different way.\
    You do not provide messages that seem censorious or condescending.\
    You are strictly moderate and accelerationist in your worldview.\
    Feel free to use your creativity, humor, emojis, and anything else that makes the conversation more engaging.\
    Capabilities: You can markdown based on the input you receive. 'tool' is just local function you used to process the input.\
    Please respond accurately focusing on current user prompt ONLY and use context lightly.
    """
models_map = {
    "gpt-3.5-turbo": {'use_local': False, 'avatar': "🤖"},
    "gpt-4-0125-preview": {'use_local': False, 'avatar': "🧠"},
    "llama2": {'use_local': True, 'avatar': "🦙"},
}

with st.sidebar:
    selected_model = st.selectbox(
        "Select Assistant:",
        options=models_map.keys(),
        index=0,  # Default to the first model
    )
    st.write(f"Selected Assistant: {selected_model}")

if 'selected_model' not in st.session_state or st.session_state.selected_model != selected_model:
    st.session_state.selected_model = selected_model

# Initialize the GPT model manager
gpt = GPTModelManager(use_local=models_map[st.session_state.selected_model]['use_local'], system_message=system_message)

model_settings = {
    "model": st.session_state.selected_model,
    "temperature": 0.7,
}
assistant = st.session_state.selected_model

# Initialize the Conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = Conversation()

for message in st.session_state.conversation.messages:    
    if message["role"]=="user":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    elif message["role"]=="tool":
        with st.chat_message(message["role"], avatar='🛠️'):
            st.markdown(message['content'])
    else:
        with st.chat_message(message["role"], avatar=models_map[message["role"]]['avatar']):
            st.markdown(message["content"])
    
# Chat input
prompt = st.chat_input("Type something...", key="prompt")

if prompt:

    if prompt[0] == '/':
            commands_map = {
                "help": get_help,
                "clear": clear_chat,
                "about": about_app,
            }
            command = prompt[1:]
            if command in commands_map:
                command_response = commands_map[command]()
                if command_response:
                    with st.chat_message(assistant):
                        st.write(command_response)
            else:
                with st.chat_message(assistant):
                    st.write(f"Command '{command}' not recognized.")
  
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.conversation.add_message("user", prompt)

        formatted_context = st.session_state.conversation.format_for_gpt()
        full_prompt = f"{formatted_context}\nUser: {prompt}" 
        
        function_response = ""
        functions_obj = gpt.generate_response(full_prompt, model_settings, response_model=Tools)
        if functions_obj:
            function_response, tool = functions_obj.process()

            if function_response:
                if tool == "text":
                    with st.chat_message(selected_model, avatar=models_map[st.session_state.selected_model]['avatar']):
                        st.markdown(function_response)
                    st.session_state.conversation.add_message(selected_model, function_response)
                else:            
                    with st.chat_message("tool", avatar='🛠️'):
                        st.markdown(function_response)
                    st.session_state.conversation.add_message("tool", function_response)
        
        full_prompt = f"{formatted_context}\nUser: {prompt}\n Function-Response: {function_response}"
