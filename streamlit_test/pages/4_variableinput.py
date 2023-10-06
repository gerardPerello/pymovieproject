import streamlit as st

st.write('# Solution using input widgets')

# a selection for the user to specify the number of rows
num_rows = st.slider('Number of rows', min_value=1, max_value=10)

# columns to lay out the inputs
grid = st.columns(1)

# Function to create a row of widgets (with row number input to assure unique keys)
def add_row(row):
    with grid[0]:
        st.text_input('pla', key=f'input_name{row}')

# Loop to create rows of input widgets
for r in range(num_rows):
    add_row(r)