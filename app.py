import streamlit as st
from Home import show_home
from Housing_Matchmaker import show_housing_matchmaker
from Resource_Navigator import show_resource_navigator
from Mental_Health_Chatbot import show_mental_health_chatbot
from Resume_Job_Finder import show_resume_job_finder
from Admin_Dashboard import show_admin_dashboard

def main():
    st.set_page_config(page_title="Pathway AI: Smart Homeless Assistance Hub", layout="wide")
    st.title("Pathway AI: Smart Homeless Assistance Hub")

    # Create a sidebar for page navigation
    pages = {
        "Home": show_home,
        "Housing Matchmaker": show_housing_matchmaker,
        "Resource Navigator": show_resource_navigator,
        "Mental Health Chatbot": show_mental_health_chatbot,
        "Resume & Job Finder": show_resume_job_finder,
        "Admin Dashboard": show_admin_dashboard
    }

    # Sidebar selectbox
    page_selection = st.sidebar.selectbox("Go to page:", list(pages.keys()))
    
    # Call the selected page function
    pages[page_selection]()

if __name__ == "__main__":
    main()
