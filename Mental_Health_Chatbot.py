import streamlit as st
import openai
from transformers import pipeline
import sqlite3
import datetime
#from twilio.rest import Client  # Uncomment if you wish to use Twilio for emergency alerts

# -------------------------------
# Initialize Sentiment Analysis
# -------------------------------
sentiment_analyzer = pipeline("sentiment-analysis")

# -------------------------------
# Set your OpenAI API key
# -------------------------------
openai.api_key = "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"  # Replace with your actual OpenAI API key

# -------------------------------
# Initialize Conversation History (in session state)
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "system", "content": "You are a compassionate and understanding mental health assistant. Engage in an empathetic conversation and provide thoughtful responses based on the user's emotional state."}
    ]

# -------------------------------
# Initialize (or connect to) the SQLite Database
# -------------------------------
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def save_message(role, content):
    """Save a single message (role and content) to the database."""
    cursor.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)", (role, content))
    conn.commit()

def show_conversation_history():
    """Retrieve and display the conversation history from the database."""
    cursor.execute("SELECT role, content, timestamp FROM chat_history ORDER BY id ASC")
    rows = cursor.fetchall()
    if rows:
        st.subheader("Conversation History")
        for row in rows:
            role, content, timestamp = row
            st.write(f"**{role.capitalize()}** ({timestamp}): {content}")
    else:
        st.info("No conversation history found.")

def show_mental_health_chatbot():
    st.subheader("Mental Health Chatbot")
    st.write("""
    This is a 24/7 chat space. Please be open and honest, and type any issues on your mind here so we can help you out.
    """)

    # Chat input from the user
    user_input = st.text_area("Type your feelings or concerns here...", height=150)

    if st.button("Send to Chatbot"):
        if not user_input.strip():
            st.error("Please enter your feelings or concerns before sending.")
        else:
            # Append the user's message to the conversation history (session state)
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            save_message("user", user_input)  # Save to the database

            # Call GPT-4 Turbo for a personalized compassionate response
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=st.session_state["chat_history"],
                    temperature=0.9,
                    max_tokens=200
                )
                chatbot_reply = response.choices[0].message.content
                # Append bot response to conversation history
                st.session_state["chat_history"].append({"role": "assistant", "content": chatbot_reply})
                save_message("assistant", chatbot_reply)  # Save to the database
            except Exception as e:
                st.error(f"Error communicating with the AI: {e}")
                return

            # Display the bot's reply on the webpage
            st.write("**Bot:**", chatbot_reply)

            # Run sentiment analysis on the user input and print to console
            sentiment = sentiment_analyzer(user_input)[0]
            print("Sentiment analysis:", sentiment)

            # Check for significant distress based on sentiment
            
            if sentiment["label"] == "NEGATIVE" and sentiment["score"] > 0.9:
                # st.warning("We detect significant emotional distress. If you are in immediate danger, please call 911 immediately.")
                # Example placeholder for Twilio emergency escalation:
                """
                client = Client("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN")
                message = client.messages.create(
                    body="Alert: A user is experiencing severe emotional distress and may need immediate assistance.",
                    from_="+1234567890",  # Your Twilio phone number
                    to="+0987654321"       # Emergency contact number
                )
                st.write("Emergency alert sent to your designated contacts.")
                """

    # Button to display conversation history from the database
    if st.button("Show Conversation History"):
        show_conversation_history()


# To use this page, call show_mental_health_chatbot() in your main Streamlit app.
