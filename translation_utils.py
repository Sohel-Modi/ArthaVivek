from googletrans import Translator
import streamlit as st

@st.cache_resource
def get_translator():
    """Initializes and returns the Translator object."""
    print("Initializing Google Translator...")
    return Translator()

# The final, comprehensive map of Indian languages supported by Google Translate
LANG_CODE_MAP = {
    # Official Languages
    "हिन्दी (Hindi)": "hi",
    # 8th Schedule Languages
    "অসমীয়া (Assamese)": "as",
    "বাংলা (Bengali)": "bn",
    "ગુજરાતી (Gujarati)": "gu",
    "कोंकणी (Konkani)": "gom",
    "मैथिली (Maithili)": "mai",
    "മലയാളം (Malayalam)": "ml",
    "ꯃꯤꯇꯩꯂꯣꯟ (Manipuri/Meitei)": "mni-Mtei",
    "मराठी (Marathi)": "mr",
    "ଓଡିଆ (Odia)": "or",
    "ਪੰਜਾਬੀ (Punjabi)": "pa",
    "संस्कृतम् (Sanskrit)": "sa",
    "संथाली (Santali)": "sat",
    "सिन्धी (Sindhi)": "sd",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "اردو (Urdu)": "ur",
    # Other Widely Spoken Languages
    "भोजपुरी (Bhojpuri)": "bho",
}

async def translate(text_to_translate: str, target_language: str) -> str:
    """
    Translates English text to the selected target language using Google Translate.
    """
    if target_language == "English":
        return text_to_translate
    
    lang_code = LANG_CODE_MAP.get(target_language)
    if not lang_code:
        return "Language not supported."

    try:
        translator = get_translator()
        translated_obj = await translator.translate(text_to_translate, dest=lang_code)
        return translated_obj.text
    except Exception as e:
        print(f"Error during translation: {e}")
        return "Translation service failed. Please check your internet connection."
    
# from googletrans import Translator  -------------- Old Best
# import streamlit as st

# @st.cache_resource
# def get_translator():
#     print("Initializing Google Translator...")
#     return Translator()

# LANG_CODE_MAP = {
#     "English": "en",
#     "हिन्दी (Hindi)": "hi",
#     "मराठी (Marathi)": "mr",
#     "ગુજરાતી (Gujarati)": "gu",
#     "বাংলা (Bengali)": "bn",
#     "తెలుగు (Telugu)": "te",
#     "தமிழ் (Tamil)": "ta"
# }

# async def translate(text_to_translate: str, target_language: str) -> str:
#     if target_language == "English":
#         return text_to_translate
    
#     lang_code = LANG_CODE_MAP.get(target_language)
#     if not lang_code:
#         return "Language not supported."

#     try:
#         translator = get_translator()
#         # Add the 'await' keyword here
#         translated_obj = await translator.translate(text_to_translate, dest=lang_code)
#         return translated_obj.text
#     except Exception as e:
#         print(f"Error during translation: {e}")
#         return "Translation service failed. Please check your internet connection."

