import streamlit as st
from db_utils import get_db_connection, get_latest_updates 
from agent import get_financial_advice  

# --- Page Configuration ---
st.set_page_config(page_title="Arthavivek", page_icon="🎓", layout="wide")

# --- Main Title and Subtitle ---
st.title("🎓 Arthavivek")
st.caption("Financial Wisdom  | समृद्धी की ओर पहला कदम")

st.write("---")

# --- Database Connection ---
client, db, knowledge_base, updates_collection = get_db_connection()

# --- Two-Column Layout ---
col1, col2 = st.columns([2, 1])

# --- Column 1: The AI Coach Interface ---
with col1:
    st.header("🤖 Your AI Financial Coach")
    
    st.subheader("Step 1: Select your persona")
    persona_options = ("Student (विद्यार्थी)", "Early-Career Professional (युवा पेशेवर)")
    persona = st.radio("Choose who you are:", persona_options, horizontal=True)
    persona_english = persona.split(" ")[0]

    st.subheader("Step 2: Ask your question")
    user_query = st.text_area("Enter your financial question here:", placeholder="e.g., How can I start investing with ₹500?", height=150)

    if st.button("Get Advice", type="primary", use_container_width=True):
        if user_query and client:
            with st.spinner("Arthavivek is thinking..."):
                # --- NEW: Handle the dictionary response ---
                response_data = get_financial_advice(user_query, persona_english)
                
                # Display the main text answer
                st.markdown(response_data['answer'])

                # --- NEW: Display related content if it exists ---
                if response_data['videos'] or response_data['blogs']:
                    st.write("---")
                    st.subheader("For Deeper Knowledge 📚")
                    for video_url in response_data['videos']:
                        st.video(video_url)
                    for blog_url in response_data['blogs']:
                        st.link_button("Read a related blog post", blog_url)

        elif not client:
            st.error("Database connection failed.")
        else:
            st.warning("Please enter a question.")

# --- Column 2: The Knowledge Hub ---
with col2:
    st.header("💡 Knowledge Hub")
    if client:
        latest_articles = get_latest_updates(updates_collection)
        if latest_articles:
            for article in latest_articles:
                st.subheader(article['title'])
                st.caption(f"Source: {article['source']} | Published: {article['date_published']}")
                st.markdown(article['summary'])
                st.link_button("Read More", article['original_link'])
                st.write("---")
        else:
            st.info("No articles found in the Knowledge Hub yet.")
    else:
        st.warning("Could not connect to the Knowledge Hub.")



# with col1:
#     st.header("🤖 Your AI Financial Coach")
    
#     # Persona Selection
#     st.subheader("Step 1: Select your persona")
#     persona_options = ("Student (विद्यार्थी)", "Early-Career Professional (युवा पेशेवर)")
#     persona = st.radio(
#         "Choose who you are:",
#         persona_options,
#         horizontal=True,
#     )
#     # Extract the English part of the persona for the backend
#     persona_english = persona.split(" ")[0]

#     # User Input
#     st.subheader("Step 2: Ask your question")
#     user_query = st.text_area(
#         "Enter your financial question here:",
#         placeholder="e.g., How can I start investing with ₹500?",
#         height=150
#     )

#     # Submit Button
#     if st.button("Get Advice", type="primary", use_container_width=True):
#         if user_query and client:
#             with st.spinner("Arthavivek is thinking..."):
#                 response = get_financial_advice(user_query, persona_english)
#                 st.markdown(response)
#         elif not client:
#             st.error("Database connection failed. Please check your credentials and network.")
#         else:
#             st.warning("Please enter a question before getting advice.")


# # --- Column 2: The Knowledge Hub ---
# with col2:
#     st.header("💡 Knowledge Hub")
    
#     if client:
#         # Fetch the latest updates using our new function
#         latest_articles = get_latest_updates(updates_collection)
        
#         if latest_articles:
#             for article in latest_articles:
#                 st.subheader(article['title'])
#                 st.caption(f"Source: {article['source']} | Published: {article['date_published']}")
#                 st.markdown(article['summary'])
#                 st.link_button("Read More", article['original_link'])
#                 st.write("---")
#         else:
#             st.info("No articles found in the Knowledge Hub yet.")
#     else:
#         st.warning("Could not connect to the Knowledge Hub.")
