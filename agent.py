import os
from dotenv import load_dotenv
from openai import OpenAI
from db_utils import get_db_connection

# --- Load API Key and Initialize Clients ---
load_dotenv()
openai_api_key = os.getenv("LLM_API_KEY")
if not openai_api_key:
    raise ValueError("LLM_API_KEY not found. Please check your .env file.")

client = OpenAI(api_key=openai_api_key)
db_client, db, knowledge_base, updates = get_db_connection()


def get_financial_advice(query: str, persona: str) -> dict:
    """
    This is the core RAG function.
    It now returns a dictionary with the answer and related links.
    """
    if not db_client:
        return {"answer": "Error: Database connection is not available.", "videos": [], "blogs": []}

    # --- 1. RETRIEVAL ---
    try:
        # We retrieve the full documents now, not just the content
        retrieved_docs = list(knowledge_base.find(
            {"$text": {"$search": query}},
            {'score': {'$meta': 'textScore'}}
        ).sort([('score', {'$meta': 'textScore'})]).limit(3))

        context = "\n---\n".join([doc['content'] for doc in retrieved_docs])
        
        # --- NEW: Extract related links ---
        related_videos = []
        related_blogs = []
        for doc in retrieved_docs:
            related_videos.extend(doc.get('related_videos', []))
            related_blogs.extend(doc.get('related_blogs', []))
        
        # Remove duplicate links
        related_videos = list(set(related_videos))
        related_blogs = list(set(related_blogs))

        if not context:
            context = "No specific information found. Please provide general advice."

    except Exception as e:
        print(f"Database retrieval error: {e}")
        context = "Error retrieving information. Please provide general advice."
        related_videos, related_blogs = [], []

    # --- 2. AUGMENTATION: Upgraded Prompt ---
    system_prompt = f"""
    You are 'Arthavivek', a friendly and wise financial coach for India's youth.
    Your user is a '{persona}'. Your goal is to provide simple, safe, and encouraging financial education, NOT specific investment advice.
    RULES:
    1.  Use the provided 'CONTEXT' to form your primary answer.
    2.  Format your answer using markdown. Use headings, bold text, and bullet points to make it easy to read.
    3.  **If the user's question is not related to finance, economics, investing, or careers, you MUST politely decline to answer. Gently guide them back to financial topics. Do not answer non-financial questions.**
    4.  Do NOT recommend any specific stocks, mutual funds, or products.
    5.  Speak in a mix of simple English and Hindi (Hinglish).
    6.  Keep the tone encouraging, like a knowledgeable friend.
    7.  Do not include a disclaimer in your response, as it is already handled by the user interface.
    """
        # system_prompt = f"""
    # You are 'Arthavivek', a friendly and wise financial coach for India's youth.
    # Your user is a '{persona}'. Your goal is to provide simple, safe, and encouraging financial education.
    # RULES:
    # 1.  Use the provided 'CONTEXT' to form your primary answer.
    # 2.  **Format your answer using markdown.** Use headings, bold text, and bullet points to make it easy to read.
    # 3.  Do NOT recommend specific stocks or products.
    # 4.  Speak in a mix of simple English and Hindi (Hinglish).
    # 5.  Keep the tone encouraging, like a knowledgeable friend.
    # 6.  Include a clear disclaimer at the end: "**Disclaimer:** This is for educational purposes only. Please consult a SEBI registered financial advisor."
    # """
    user_prompt = f"CONTEXT:\n{context}\n\nMY QUESTION:\n{query}"

    # --- 3. GENERATION ---
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
        )
        answer = response.choices[0].message.content
        
        # Return a dictionary now
        return {
            "answer": answer,
            "videos": related_videos,
            "blogs": related_blogs
        }

    except Exception as e:
        print(f"LLM generation error: {e}")
        return {"answer": "Sorry, I am having trouble processing your request right now.", "videos": [], "blogs": []}


# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from db_utils import get_db_connection

# # --- Load API Key and Initialize Clients ---
# load_dotenv()
# openai_api_key = os.getenv("LLM_API_KEY")
# if not openai_api_key:
#     raise ValueError("LLM_API_KEY not found. Please check your .env file.")

# client = OpenAI(api_key=openai_api_key)
# db_client, db, knowledge_base, updates = get_db_connection()


# def get_financial_advice(query: str, persona: str) -> str:
#     """
#     This is the core RAG function.
#     It retrieves context from MongoDB and uses it to generate a financial advice response.
#     """
#     if not db_client:
#         return "Error: Database connection is not available."

#     # --- 1. RETRIEVAL: Find relevant knowledge from our database ---
#     # We use a simple text search in MongoDB. This requires a "text index".
#     # The search looks for the user's query keywords within our stored documents.
#     try:
#         retrieved_docs = knowledge_base.find(
#             {"$text": {"$search": query}},
#             {'score': {'$meta': 'textScore'}}
#         ).sort([('score', {'$meta': 'textScore'})]).limit(3)

#         context = "\n---\n".join([doc['content'] for doc in retrieved_docs])
        
#         if not context:
#             context = "No specific information found. Please provide general advice."

#     except Exception as e:
#         print(f"Database retrieval error: {e}")
#         context = "Error retrieving information. Please provide general advice."


#     # --- 2. AUGMENTATION: Build a detailed prompt for the LLM ---
#     # This is the most important step: "Prompt Engineering".
#     system_prompt = f"""
#     You are 'Arthavivek', a friendly and wise financial coach for India's youth.
#     Your user is a '{persona}'. Your goal is to provide simple, safe, and encouraging financial education, NOT specific investment advice.
#     You must follow these rules strictly:
#     1.  Use the provided 'CONTEXT' to form your primary answer.
#     2.  Do not recommend any specific stocks, mutual funds, or products.
#     3.  Speak in a mix of simple English and Hindi (Hinglish).
#     4.  Keep the tone encouraging, like a knowledgeable friend.
#     5.  Include a clear disclaimer at the end: "Disclaimer: This is for educational purposes only. Please consult a SEBI registered financial advisor."
#     """

#     user_prompt = f"""
#     CONTEXT:
#     {context}
    
#     MY QUESTION:
#     {query}
#     """

#     # --- 3. GENERATION: Call the LLM to get the final response ---
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             temperature=0.7,
#         )
#         return response.choices[0].message.content

#     except Exception as e:
#         print(f"LLM generation error: {e}")
#         return "Sorry, I am having trouble processing your request right now." 
