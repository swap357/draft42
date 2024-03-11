""" Main application file for the Streamlit app. """

import streamlit as st

from utils.conversation import Conversation
from utils.utils import get_help, clear_chat, about_app

from tools.shell import ShellCommand
from tools.text_response import TextResponse
from utils.gpt import GPTModelManager
from tools.chart import PlotLike
from tools.df_manipulation import DataFrameManipulation
from utils.utils import apply_data_manipulations
import plotly.graph_objects as go
import os
import pandas as pd

from itertools import cycle


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

if "tool_history" not in st.session_state:
    st.session_state.tool_history = Conversation(short_term_memory_size=2)

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

def use_tool(prompt,response_model):
    tool_model = "gpt-4-0125-preview"
    gpt = GPTModelManager(use_local=models_map[tool_model]['use_local'], system_message=models_map[tool_model]['system_message'])
    model_settings = {
        "model": tool_model,
        "temperature": 0.7,  # Customize as needed
    }
    tool_obj = gpt.generate_response(prompt, model_settings, response_model=response_model)
    return tool_obj

def plot(query, expected_response_model=PlotLike):
    
    st.session_state.tool_history.add_message("user", query)
    
    fig = go.Figure()

    data_dir = "data/"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    csv_headers = {}
    for file in csv_files:
        df = pd.read_csv(os.path.join(data_dir, file))
        csv_headers[file] = df.columns.tolist()

    history = st.session_state.tool_history.format_for_gpt()
    gpt_prompt = f"""Analyze the following CSV headers: {csv_headers}. 
    Based on the user's query: '{query}', 
    and considering the historical context: '{history}', 
    determine the most appropriate CSV file and its columns to use for creating a plot. 
    Please specify the CSV file name, the columns for the x-axis and y-axis, and any other relevant details such as plot type that should be applied.
    """
    
    st.session_state.tool_history.add_message("plotPrompt", gpt_prompt)
    print(gpt_prompt)
    print("----------")
    
    plot_like = use_tool(gpt_prompt, expected_response_model)  # Assuming use_tool now returns a PlotLike instance
    plot_response = plot_like.__dict__
    st.session_state.tool_history.add_message("plotGPT", plot_response)
    
    # Loop through each Trace object in the PlotLike object
    # pretty print plotlike
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(plot_like.__dict__)

    for trace in plot_like.traces:
        df = pd.read_csv(os.path.join(data_dir, trace.df_file_path))

        # Check if the trace is for the primary or secondary y-axis
        if trace.yaxis == 'y2':
            # Add trace to the figure for the secondary y-axis
            fig.add_trace(go.Scatter(
                x=df[trace.x_column], 
                y=df[trace.y_column], 
                name=trace.name, 
                mode=trace.mode,  # Use the mode attribute
                line=dict(color=trace.color),
                yaxis='y2'  # Specify this trace is for the secondary y-axis
            ))
        else:
            # Add trace to the figure for the primary y-axis
            fig.add_trace(go.Scatter(
                x=df[trace.x_column], 
                y=df[trace.y_column], 
                name=trace.name, 
                mode=trace.mode,  # Use the mode attribute
                line=dict(color=trace.color)
            ))

    # Update layout with new fields from PlotLike
    fig.update_layout(
        title=plot_like.title,
        xaxis_title=plot_like.layout_xaxis_title,
        xaxis_type=plot_like.layout_xaxis_type,
        yaxis_title=plot_like.layout_yaxis_title,
        yaxis_type=plot_like.layout_yaxis_type,
        
        showlegend=True,
        height=600
    )
    
    if plot_like.xaxis_range:
        fig.update_xaxes(range=plot_like.xaxis_range)
    if plot_like.yaxis_range:
        fig.update_yaxes(range=plot_like.yaxis_range)
    
    # Conditionally add the second y-axis if specified
    if plot_like.yaxis2_title and plot_like.yaxis2_type:
        print("yaxis2 updated")
        fig.update_layout(
            yaxis2=dict(
                title=plot_like.yaxis2_title,
                titlefont=dict(color="blue"),
                tickfont=dict(color="blue"),
                overlaying="y",
                side="right",
            )
        )
    
    return fig

# Chat input
prompt = st.chat_input("Type something...", key="prompt")

if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)
    
    if prompt[0] == '/':
        commands_map = {
            "help": (get_help, None),
            "clear": (clear_chat, None),
            "about": (about_app, None),
            "shell": (use_tool, ShellCommand),
            "text": (use_tool, TextResponse),
            "plot": (plot, PlotLike),
            }
        
        command, *args = prompt[1:].split()
        args = " ".join(args)
        print(command)
        if command in commands_map:
            if args:

                response_obj = commands_map[command][0](args, commands_map[command][1])
            else:
                response_obj = commands_map[command][0]()
            
            if response_obj:
                if command == "plot":
                    with st.chat_message("tool", avatar='🛠️'):
                        st.plotly_chart(response_obj)
                else:
                    with st.chat_message("tool", avatar='🛠️'):
                        st.markdown(response_obj.process())

        else:
            with st.chat_message("tool", avatar='🛠️'):
                st.markdown(f"Command '{command}' not recognized.")

    else:
        for model_name in st.session_state.selected_models:
            
            # Initialize the GPT model manager
            gpt = GPTModelManager(use_local=models_map[model_name]['use_local'], system_message=models_map[model_name]['system_message'])

            model_settings = {
                "model": model_name,
                "temperature": 0.7,  # Customize as needed
            }
            
            function_response = ""
            full_prompt = st.session_state.conversation.format_for_gpt()
            
            response = gpt.generate_response(full_prompt, model_settings).response
            if response:
                with st.chat_message(model_name, avatar=models_map[model_name]['avatar']):
                    st.markdown(response)
                st.session_state.conversation.add_message(model_name, response)
            else:
                with st.chat_message(model_name, avatar=models_map[model_name]['avatar']):
                    st.write("I'm sorry, I don't have a response to that.")