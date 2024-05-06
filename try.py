import streamlit as st
st.session_state.submitted_to_github = False
def submitted_to_github():
    st.session_state.submitted_to_github = True

submitted_to_github1 = st.checkbox('Upload to GitHub')

# st.session_state.submitted_to_github
if submitted_to_github1:
    st.session_state.submitted_to_github = True
st.session_state.submitted_to_github
# , key='submitted_to_github', on_change=submitted_to_github