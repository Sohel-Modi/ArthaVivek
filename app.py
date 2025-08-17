import streamlit as st

# --- Page Configuration ---
# Set the page title and icon for the browser tab
st.set_page_config(page_title="ArthaVivek", page_icon="🎓", layout="wide")

# --- Main Title and Subtitle ---
st.title("🎓 ArthaVivek")
st.caption("Financial Wisdom | समृद्धी के ओर पहला कदम")

st.write("---")

# --- Two-Column Layout ---
# Create two columns: one for the AI Coach, one for the Knowledge Hub
col1, col2 = st.columns([2, 1]) # The AI Coach column is twice as wide


# --- Column 1: The AI Coach Interface ---
with col1:
    st.header("🤖 Your AI Financial Coach")
    
    # Persona Selection
    st.subheader("Step 1: Select your persona")
    persona = st.radio(
        "Choose who you are:",
        ("Student (विद्यार्थी)", "Early-Career Professional (युवा पेशेवर)"),
        horizontal=True,
    )

    # User Input
    st.subheader("Step 2: Ask your question")
    user_query = st.text_area(
        "Enter your financial question here:",
        placeholder="e.g., How can I start investing with ₹500?",
        height=150
    )

    # Submit Button
    if st.button("Get Advice", type="primary", use_container_width=True):
        if user_query:
            # This is where we will call our AI agent in a future step
            st.success("Button clicked! We will connect the AI logic here on Day 5.")
            # For now, just show a placeholder response
            st.markdown("Thinking...") 
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
