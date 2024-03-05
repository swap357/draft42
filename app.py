""" Main application file for the Streamlit app. """

import streamlit as st
from utils.gpt import GPTModelManager
from utils.conversation import Conversation
from utils.utils import get_help, clear_chat, about_app
from tools.tools import Tools

# system_message = """
#     You are a snarky, highly intelligent chatbot.\
#     You are also here to make them make them think about the world in a totally different way.\
#     You do not provide messages that seem censorious or condescending.\
#     Feel free to use your creativity, humor, emojis, and anything else that makes the conversation more engaging.\
#     Capabilities: You can markdown based on the input you receive. 'tool' is just local function you used to process the input.\
#     Please respond accurately focusing on current user prompt ONLY and use context lightly.
#     Respond with markdown code block for code for code snippets, regex and other code related stuff.
#     """

generic_system_message = """
    You are a snarky, highly intelligent chatbot.\
    Your name is {model_name}, a Large Language Model.
    Address all members and assistants in the conversation, not just the last speaker or user.
    Capabilities: You can markdown based on the input you receive.
    Respond with markdown code block for code for code snippets.
"""

models_map = {
    "gpt-3.5-turbo": {
        'use_local': False,
        'avatar': "🤖",
        'system_message': generic_system_message.format(model_name="GPT-3.5-turbo")
    },
    "gpt-4-0125-preview": {
        'use_local': False,
        'avatar': "🧠",
        'system_message': generic_system_message.format(model_name="GPT-4-0125")
    },
    "llama2": {
        'use_local': True,
        'avatar': "🦙",
        'system_message': generic_system_message.format(model_name="Llama2")
    },
}


with st.sidebar:
    selected_models = st.multiselect(
        "Select Assistants:",
        options=list(models_map.keys()),
        default=[list(models_map.keys())[0]],  # Default to the first model
    )
    st.write(f"Selected Assistants: {', '.join(selected_models)}")

# Update session state to handle multiple selected models
if 'selected_models' not in st.session_state or st.session_state.selected_models != selected_models:
    st.session_state.selected_models = selected_models

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
                    with st.chat_message("tool", avatar='🛠️'):
                        st.write(command_response)
            else:
                with st.chat_message("tool", avatar='🛠️'):
                    st.write(f"Command '{command}' not recognized.")
  
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.conversation.add_message("user", prompt)
        
        for model_name in st.session_state.selected_models:
            
            # Initialize the GPT model manager
            gpt = GPTModelManager(use_local=models_map[model_name]['use_local'], system_message=models_map[model_name]['system_message'])

            model_settings = {
                "model": model_name,
                "temperature": 0.7,  # Customize as needed
            }
            
            function_response = ""
            full_prompt = st.session_state.conversation.format_for_gpt()
            
            functions_obj = gpt.generate_response(full_prompt, model_settings, response_model=Tools)
            if functions_obj:
                function_response, tool = functions_obj.process()

                if function_response:
                    if tool == "text":
                        with st.chat_message(model_name, avatar=models_map[model_name]['avatar']):
                            st.markdown(function_response)
                        st.session_state.conversation.add_message(model_name, function_response)
                    else:            
                        with st.chat_message("tool", avatar='🛠️'):
                            st.markdown(function_response)
                        st.session_state.conversation.add_message("tool", function_response)
                        break
            else:
                response = gpt.generate_response(full_prompt, model_settings)
                if response:
                    with st.chat_message(model_name, avatar=models_map[model_name]['avatar']):
                        st.markdown(response)
                    st.session_state.conversation.add_message(model_name, response)
                else:
                    with st.chat_message(model_name, avatar=models_map[model_name]['avatar']):
                        st.write("I'm sorry, I don't have a response to that.")