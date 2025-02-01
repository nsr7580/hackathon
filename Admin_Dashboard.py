import streamlit as st

def show_admin_dashboard():
    st.subheader("Admin Dashboard")
    st.write("""
    Monitor usage analytics, user data trends, and manage resources from this dashboard.
    """)

    # Placeholder metrics
    st.metric("Active Users", "350", "+10% from last week")
    st.metric("Housing Requests", "1200", "+5% from last week")
    st.metric("Jobs Found", "210", "+2% from last week")

    st.write("""
    **Future Enhancements**:
    - Advanced analytics with Plotly or Dash integrations.
    - Secure authentication for admin access.
    - GraphQL API for efficient data querying.
    """)

