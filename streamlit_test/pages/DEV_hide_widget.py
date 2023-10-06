import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data (replace this with your actual data)
data = {
    'PlayerID': [1, 2, 3, 4, 5],
    'Score': [85, 92, 78, 95, 88]
}

# Create a DataFrame from the sample data
df = pd.DataFrame(data)

# Streamlit app
st.title('Player Data Visualization')

# Dropdown menu for selecting Player ID
selected_player_id = st.selectbox('Select Player ID', df['PlayerID'])

# Display the chart only if a player ID is selected
if selected_player_id:
    # Filter the DataFrame based on the selected player ID
    selected_player_data = df[df['PlayerID'] == selected_player_id]

    # Create a line chart using Plotly Express
    fig = px.line(selected_player_data, x='PlayerID', y='Score', title=f'Player {selected_player_id} Score')
    
    # Display the chart
    st.plotly_chart(fig)
else:
    st.write('Please select a Player ID to view the chart.')
