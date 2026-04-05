import os
import re
import json
import time
import Translator
from googletrans import LANGUAGES

# Defining the files to scrape
FILES_TO_SCRAPE = ["LanguageSelection.py", "Main.py", "Updated_GUI.py"]

def generate_json_files():
    print("Scanning files for strings...")
    discovered_strings = set()

    # Looking for translate_text("TEXT")
    pattern = re.compile(r'translate_text\("([^"]+)"\)')

    for file in FILES_TO_SCRAPE:
        if os.path.exists(file):
            print(f"Scraping {file}...")
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                matches = pattern.findall(content)
                for i in matches:
                    discovered_strings.add(i)
        else:
            print(f"File {file} not found. Skipping...")

    print(f"Found {len(discovered_strings)} strings...")

    # Translation loop
    os.makedirs("languages", exist_ok=True)

    for code in LANGUAGES.keys():
        if code == "en":
            continue # skip english
        print(f"Processing {code} ({LANGUAGES[code]})...")

        # Change the code in config.txt so the Translator knows its target
        with open("config.txt", "w") as f:
            f.write(code)

        cache = {}
        for string in discovered_strings:
            try:
                # Calling translate_text
                cache[string] = Translator.translate_text(string)
                # 0.1s delay to be nice to google
                time.sleep(0.1)
            except Exception as e:
                print(f"Failed to translate {string}: {e}")

        # Save the json file
        with open(f'languages/{code}.json', "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)
            print(f"{code} ({LANGUAGES[code]}) Completed!)")

    print(f"{code} ({LANGUAGES[code]}) complete!")

if __name__ == "__main__":
    os.environ["SCRAPING"] = "true" # so Translator.py doesn't try to read its own cache
    generate_json_files()
    print("CACHE GENERATION COMPLETE")
