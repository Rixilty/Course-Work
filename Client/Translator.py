import asyncio
from googletrans import Translator
import json
import os

CONFIG_FILE = "config.txt"

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

    # Check if we already have a pre-generated translation in our json file
    cache_file = f"languages/{lang_code}.json"
    # Skip cache if we are scraping
    is_scraping = os.environ.get("SCRAPING") == "true"
    if os.path.exists(cache_file) and not is_scraping:
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                # If the string exists in the json file return it immediately
                if target_text in cache_data:
                    return cache_data[target_text]
        except Exception as e:
            print(f"Cache error: {e}")

    # API fallback in case the cache doesn't work or if a string is missing

    translator = Translator()

    # Otherwise, translate it using a synchronous wrapper
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(translator.translate(target_text, dest=lang_code))
        return result.text
    except Exception as e:
        return target_text # Return original text if internet fails

def translate_message(incoming_message):
    # Getting the user's preferred language from config.txt
    try:
        with open(CONFIG_FILE, "r") as f:
            my_lang = f.read().strip().lower()
    except:
        my_lang= "en"

    translator = Translator()

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Detect the langauge of the message
        lang_detect = loop.run_until_complete(translator.detect(incoming_message))
        source_lang = lang_detect.lang

        # Only translate if the message isn't in the same language as the user's
        if source_lang == my_lang:
            return incoming_message

        # Translate to the user's language if it doesn't match
        result = loop.run_until_complete(translator.translate(incoming_message, dest=my_lang))
        return result.text

    except Exception as e:
        return incoming_message # Return original message if it fails