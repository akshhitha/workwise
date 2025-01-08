import streamlit as st
from coldmail import Chain
from coldmail import Portfolio
from utils import clean_text
from coldmail import create_streamlit_app
# Page setup
st.set_page_config(page_title="Work Wise", layout="wide")

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Pages
def home_page():
    st.title("Work Wise")
    st.write("enter desc later. also add logo")

    # Image placeholder (replace with an actual image file)
    #st.image("https://www.shutterstock.com/image-vector/stress-work-vector-illustration-taking-260nw-2416852225.jpg", caption="replace image")

    # Services section
    st.write("---")
    st.write("## Our Services")

    # Create columns for the service cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("https://png.pngtree.com/png-vector/20190129/ourmid/pngtree-email-vector-icon-png-image_355828.jpg", width=60)  # Icon placeholder
        st.subheader("Cold Email")
        st.write("enter desc later, decide a name.")
        if st.button("Double click", key="strategy"):
            navigate_to("Strategy")

    with col2:
        st.image("https://t3.ftcdn.net/jpg/02/26/42/06/360_F_226420649_vlXjp3JyUrnW5EHY00dvhbqkVdUfyafj.jpg", width=60)  # Icon placeholder
        st.subheader("PDF Chat")
        st.write("enter desc later. decide a name")
        if st.button("Double click", key="results"):
            navigate_to("Results")

    with col3:
        st.image("https://via.placeholder.com/100", width=60)  # Icon placeholder
        st.subheader("Dummy")
        st.write("enter desc later. decide a name")
        if st.button("More", key="expertise"):
            navigate_to("Expertise")

    with col4:
        st.image("https://via.placeholder.com/100", width=60)  # Icon placeholder
        st.subheader("Dummy")
        st.write("enter desc later. decide a name")
        if st.button("More", key="support"):
            navigate_to("Support")

    # Footer section
    st.write("---")
    st.write("trademark add")

def strategy_page():
    st.title("Cold Email Generation")
    st.write("enter steps here")
    if st.button("Back to Home"):
        navigate_to("Home")

    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)

def results_page():
    st.title("Results")
    st.write("Detailed information about our Results services.")
    if st.button("Back to Home"):
        navigate_to("Home")

def expertise_page():
    st.title("Expertise")
    st.write("Detailed information about our Expertise services.")
    if st.button("Back to Home"):
        navigate_to("Home")

def support_page():
    st.title("Support")
    st.write("Detailed information about our Support services.")
    if st.button("Back to Home"):
        navigate_to("Home")

# Route to the appropriate page
if st.session_state.current_page == "Home":
    home_page()
elif st.session_state.current_page == "Strategy":
    strategy_page()
elif st.session_state.current_page == "Results":
    results_page()
elif st.session_state.current_page == "Expertise":
    expertise_page()
elif st.session_state.current_page == "Support":
    support_page()
