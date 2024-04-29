import streamlit as st

options = st.multiselect(
    'Select the files',
    )

st.write('You selected:', options)