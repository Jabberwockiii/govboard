import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# Function to read JSON data
def read_json_file(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

# Title of the app
st.title('Award Amount Visualization')

# List available JSON files in the directory
json_files = [f for f in os.listdir('.') if f.endswith('.json')]
selected_file = st.sidebar.selectbox('Select a JSON file', json_files)

# Granularity selection
granularity = st.sidebar.selectbox('Select granularity', ['Monthly', 'Quarterly', 'Yearly'])

# Date column selection
date_column = st.sidebar.selectbox('Select date column', ['Start Date', 'End Date'])

# Read the selected JSON file
df = read_json_file(selected_file)

# Check if DataFrame is empty
if not df.empty:
    # Check if the selected date column exists
    if date_column in df.columns:
        # Convert date strings to datetime objects
        df[date_column] = pd.to_datetime(df[date_column])
        # Sorting the data by the selected date column
        df = df.sort_values(by=date_column)

        # Resample the data based on selected granularity
        if granularity == 'Monthly':
            df_resampled = df.resample('M', on=date_column).sum()
        elif granularity == 'Quarterly':
            df_resampled = df.resample('Q', on=date_column).sum()
        else:  # Yearly
            df_resampled = df.resample('Y', on=date_column).sum()

        # Plotting with Plotly
        fig = px.line(df_resampled, x=df_resampled.index, y='Award Amount', markers=True,
                      labels={date_column: date_column, 'Award Amount': 'Award Amount'},
                      title=f'Award Amount Over Time ({granularity}, {date_column})')
        fig.update_layout(xaxis_title=date_column, yaxis_title='Award Amount')

        # Show plot in Streamlit using Plotly
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"The selected JSON file does not contain a '{date_column}' column.")
else:
    st.error("The selected JSON file is empty.")
