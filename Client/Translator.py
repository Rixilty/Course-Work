import asyncio
from googletrans import Translator

CONFIG_FILE = "config.txt"

translator = Translator()

def translate_text(target_text):
    # Getting the language code from config.txt
    try:
        with open(CONFIG_FILE, "r") as f:
            lang_code = f.read().strip().lower()
    except:
        lang_code = "en" # Default to English if file fails

    # If it's already in English or if it's null return the text
    if lang_code == "en" or lang_code == "null":
        return target_text

    # Otherwise, translate it using a synchronous wrapper
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(translator.translate(target_text, dest=lang_code))
        return result.text
    except Exception as e:
        return target_text # Return original text if internet fails