import argostranslate.package
import argostranslate.translate
from langdetect import detect
import json
import os

from six import text_type

CONFIG_FILE = "config.txt"

def install_if_missing(from_code, to_code):
    # Insure the required NMT model is installed locally
    try:
        installed = argostranslate.package.get_installed_packages()
        if any(pkg.from_code == from_code and pkg.to_code == to_code for pkg in installed):
            return True
        argostranslate.package.update_package_index()
        available = argostranslate.package.get_available_packages()
        package = next(filter(lambda x: x.from_code == from_code and x.to_code == to_code, available), None)

        if package:
            argostranslate.package.install_from_path(package.download())
            return True
    except Exception as e:
        print(e)
    return False

def translate_text(target_text):
    # Getting the language code from config.txt
    try:
        with open(CONFIG_FILE, "r") as f:
            lang_code = f.read().strip().lower()
    except:
        lang_code = "en" # Default to English if file fails

    # If it's already in English or if it's null return the text
    if lang_code in ["en", "null", ""]:
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

    # Fallback to Argos for the UI if missing from cache

    try:
        install_if_missing("en", lang_code)
        return argostranslate.translate.translate(target_text, "en", lang_code)
    except:
        return target_text

def translate_message(incoming_message):
    # Getting the user's preferred language from config.txt
    try:
        with open(CONFIG_FILE, "r") as f:
            my_lang = f.read().strip().lower()
    except:
        my_lang= "en"

    if my_lang in ["en", "null", ""]:
        return incoming_message

    # Detect the message's language (source)
    try:
        # This is local on the user's CPU
        install_if_missing("en", my_lang)
        return argostranslate.translate.translate(incoming_message, "en", my_lang)
    except:
        return incoming_message

def translate_outgoing(text_to_send):
    # Coverts outgoing message into English before sending it to the server
    try:
        # If the message is just numbers or empty don't try to detext it
        if not text_to_send or text_to_send.strip().isdigit():
            return text_to_send

        source_lang = detect(text_to_send)
        if source_lang == "en":
            return text_to_send

        if install_if_missing(source_lang, "en"):
            return argostranslate.translate.translate(text_to_send, source_lang, "en")
    except Exception as e:
        return text_to_send
    return text_to_send
