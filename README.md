 # Arthavivek 🎓

**ArthaVivek:** An AI-powered financial literacy coach 🧠 using Streamlit, MongoDB, & LLMs to deliver personalized financial wisdom for India's youth.

---

## ✨ Key Features

* **🤖 Persona-Based AI Coach:** Delivers tailored financial advice for "Students" and "Early-Career Professionals".
* **💡 Curated Knowledge Hub:** A dynamic feed with simplified summaries of the latest financial news and educational articles.
* **🌐 Multilingual Support:** The AI's response can be translated into multiple Indian languages, including Hindi, Marathi, and more.
* **📚 Related Content Suggestions:** Provides links to relevant YouTube videos and blogs for deeper learning on financial topics.
* **🛡️ Safe & Educational:** Built with strong guardrails to provide responsible financial education, not specific investment advice.

---

## 🏗️ Architecture Overview

Arthavivek is built using a **Retrieval-Augmented Generation (RAG)** architecture.

1.  **User Query:** A user asks a question through the Streamlit UI.
2.  **Retrieve:** The system queries a **MongoDB Atlas** database to find the most relevant, pre-processed financial articles.
3.  **Augment:** The retrieved context is combined with the user's query and a detailed system prompt.
4.  **Generate:** The complete prompt is sent to an **LLM (GPT-4o)**, which generates a safe, helpful, and context-aware response.



---

## 🛠️ Technology Stack

* **Frontend:** Streamlit
* **Backend Logic:** Python
* **Database:** MongoDB Atlas
* **AI Engine:** OpenAI (GPT-4o)
* **Core AI Framework:** LangChain
* **Translation:** Googletrans
* **Data Ingestion:** BeautifulSoup, Requests

---

## 🚀 Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/arthavivek.git](https://github.com/your-username/arthavivek.git)
    cd arthavivek
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Create a file named `.env` in the root directory and add your secret keys:
    ```
    MONGO_URI="your_mongodb_connection_string"
    LLM_API_KEY="your_openai_api_key"
    ```

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

