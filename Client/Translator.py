import asyncio
from googletrans import Translator

translator = Translator()

message = "Hallo Welt!"
destination = "en"

# Define as an async function
async def detect_language(text):
    # await the coroutine to get the actual result
    lang_detect = await translator.detect(text) # detect the language of the text
    return lang_detect.lang # return the detected language

async def translate(text):
    source = await detect_language(text)
    if source != destination:
        # await translation result
        translated_message = await translator.translate(text, dest='en', src=source)
        return translated_message.text # return translated messsage
    return text #  return the original text if it's already in the destination language

# A main function to run the async code
async def main():
    language_detected = await detect_language(message)
    result = await translate(message)
    print("Language detected:", language_detected)
    print("Translated text:", result)

if __name__ == "__main__":
    asyncio.run(main())