from googletrans import Translator
import streamlit as st

@st.cache_resource
def get_translator():
    print("Initializing Google Translator...")
    return Translator()

LANG_CODE_MAP = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "मराठी (Marathi)": "mr",
    "ગુજરાતી (Gujarati)": "gu",
    "বাংলা (Bengali)": "bn",
    "తెలుగు (Telugu)": "te",
    "தமிழ் (Tamil)": "ta"
}

async def translate(text_to_translate: str, target_language: str) -> str:
    if target_language == "English":
        return text_to_translate
    
    lang_code = LANG_CODE_MAP.get(target_language)
    if not lang_code:
        return "Language not supported."

    try:
        translator = get_translator()
        # Add the 'await' keyword here
        translated_obj = await translator.translate(text_to_translate, dest=lang_code)
        return translated_obj.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return "Translation service failed. Please check your internet connection."

# import streamlit as st
# from transformers import pipeline

# # Use Streamlit's cache to store the model and avoid reloading it.
# # This also solves the conflict with PyTorch and Streamlit's watcher.
# @st.cache_resource
# def load_translator(model_name):
#     """Loads a translation model using Streamlit's cache."""
#     print(f"Loading model: {model_name}...")
#     try:
#         return pipeline("translation", model=model_name)
#     except Exception as e:
#         print(f"Could not load model {model_name}: {e}")
#         return None

# # Maps the language name to the specific Hugging Face model
# MODEL_MAP = {
#     "हिन्दी (Hindi)": "Helsinki-NLP/opus-mt-en-hi",
#     # You can add other languages here in the future
# }

# def translate(text_to_translate: str, target_language: str) -> str:
#     """
#     Translates English text to the selected target language.
#     """
#     if target_language == "English":
#         return text_to_translate

#     model_name = MODEL_MAP.get(target_language)
#     if not model_name:
#         return "No translation model available for the selected language."

#     translator = load_translator(model_name)
#     if not translator:
#         return "Translation service is unavailable."

#     try:
#         translated_text = translator(text_to_translate, max_length=1024)
#         return translated_text[0]['translation_text']
#     except Exception as e:
#         print(f"Error during translation: {e}")
#         return "Could not translate text."


# from transformers import pipeline

# try:
#     translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
#     print("Translation model loaded successfully.")
# except Exception as e:
#     translator = None
#     print(f"Could not load translation model: {e}")

# def translate_to_hindi(text_to_translate: str) -> str:
#     """
#     Translates a given English text to Hindi using the pre-loaded model.
#     """
#     if not translator:
#         return "Translation service is unavailable."
    
#     # The model may struggle with very long text, so we can split it if needed.
#     # For now, we'll translate the whole block.
#     try:
#         translated_text = translator(text_to_translate, max_length=1024)
#         return translated_text[0]['translation_text']
#     except Exception as e:
#         print(f"Error during translation: {e}")
#         return "Could not translate text."