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

def apply_data_manipulations(df, manipulations):
    # Example implementation - adjust based on actual needs
    # Process filters
    if manipulations.filters:
        for filter_op in manipulations.filters:
            if filter_op.operation == 'equals':
                # Expecting value to be a list with one element for 'equals'
                df = df[df[filter_op.column] == filter_op.value[0]]
            elif filter_op.operation == 'less_than':
                # Expecting value to be a list with one element for 'less_than'
                df = df[df[filter_op.column] < filter_op.value[0]]
            elif filter_op.operation == 'greater_than':
                # Expecting value to be a list with one element for 'greater_than'
                df = df[df[filter_op.column] > filter_op.value[0]]
            elif filter_op.operation == 'between':
                # Expecting value to be a list with two elements for 'between'
                lower_bound, upper_bound = filter_op.value
                df = df[(df[filter_op.column] >= lower_bound) & (df[filter_op.column] <= upper_bound)]
    
    # Process cleans
    if manipulations.cleans:
        for clean_op in manipulations.cleans:
            if clean_op.method == 'fill_missing':
                df[clean_op.column].fillna(clean_op.value, inplace=True)
            elif clean_op.method == 'drop':
                df.dropna(subset=[clean_op.column], inplace=True)
            # Add more conditions for other cleaning methods

    
    return df