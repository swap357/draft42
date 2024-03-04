import streamlit as st


def get_help():
    # create help menu in markdown format
    help_message = """\n
    #### Hello, I'm Draft42!
    I'm a chatbot that can help you with any questions you have.\n

    Here are some commands you can use:
    - `/help`: Displays this help message.
    - `/clear`: Clears the chat history.
    - `/about`: Displays information about this app.
    or you can simply type your message and I will respond.

    I can talk to models as well as some local functions and tools, all in natural^ spoken language. 
    Here are some local tools I've been trained to use:
    - shell: to validate and execute shell commands.

    Some conversation starters:
    - What is the meaning of life?
    - what's 42+42-42*42/42
    - current cpu, memory, disk usage in the system
    """
    return help_message

def clear_chat():
    st.session_state.conversation.clear()
    st.rerun()

def about_app():
    about_message = """
    This is a chatbot app that demonstrates function-calling using local or OPENAI models.
    The app uses Streamlit for the user interface.
    Developed by [Swapnil Patel](https://autoscaler.sh/).
    """
    return about_message

