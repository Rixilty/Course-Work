from googletrans import Translator

translator = Translator()

message = "Hello"
destination = "en"

def detect_language(text):
    lang_detect = translator.detect(text)
    return lang_detect.lang

def translate(text):
    source = detect_language(text)
    if source != destination:
        translated_message = translator.translate(text, dest='en', src=source)
        return translated_message.text

translate(message)