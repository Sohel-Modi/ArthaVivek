import streamlit as st
from db_utils import get_db_connection
from agent import get_financial_advice  

# --- Page Configuration ---
st.set_page_config(page_title="Arthavivek", page_icon="🎓", layout="wide")

# --- Main Title and Subtitle ---
st.title("🎓 Arthavivek")
st.caption("Financial Wisdom  | समृद्धी की ओर पहला कदम")

st.write("---")

# --- Database Connection (runs only once) ---
client, db, knowledge_base, updates = get_db_connection()

# --- Two-Column Layout ---
col1, col2 = st.columns([2, 1])

# --- Column 1: The AI Coach Interface ---
with col1:
    st.header("🤖 Your AI Financial Coach")
    
    # Persona Selection
    st.subheader("Step 1: Select your persona")
    persona_options = ("Student (विद्यार्थी)", "Early-Career Professional (युवा पेशेवर)")
    persona = st.radio(
        "Choose who you are:",
        persona_options,
        horizontal=True,
    )
    # Extract the English part of the persona for the backend
    persona_english = persona.split(" ")[0]

    # User Input
    st.subheader("Step 2: Ask your question")
    user_query = st.text_area(
        "Enter your financial question here:",
        placeholder="e.g., How can I start investing with ₹500?",
        height=150
    )

    # Submit Button
    if st.button("Get Advice", type="primary", use_container_width=True):
        if user_query and client:  # Check if query exists and DB is connected
            # --- 2. THIS IS THE MAGIC PART ---
            # Replace placeholder with the actual call to our AI agent
            with st.spinner("Arthavivek is thinking..."):
                response = get_financial_advice(user_query, persona_english)
                st.markdown(response) # Display the formatted response
        elif not client:
            st.error("Database connection failed. Please check your credentials and network.")
        else:
            st.warning("Please enter a question before getting advice.")

# --- Column 2: The Knowledge Hub ---
with col2:
    st.header("💡 Knowledge Hub")
    st.info("Simplified summaries of the latest financial news and policies will appear here. We will build this on Day 6.")
    
    # Placeholder content
    st.subheader("Example: RBI's Latest Update")
    st.write("A brief, easy-to-understand summary of a recent RBI policy will be displayed here.")
    
    st.subheader("Example: What is a Demat Account?")
    st.write("A simple explanation of a common financial concept will be shown here.")

