# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator
import xml.etree.ElementTree as ET
import subprocess
import os
import shutil
# ------------------------------------------


# Run script
"""
python3 translate.py
"""
# ------------------


# Requirements:
"""
1) Python 3.x  
   ▸ Check version: `python3 --version` or `python --version`  
   ▸ Installation:
			 macOS:
				 - Use Homebrew: `brew install python`

			 Linux (Ubuntu/Debian):
				 - `sudo apt update && sudo apt install python3`

			 Windows:
				 - Download the installer from: https://www.python.org/downloads/windows/
				 - Make sure to check "Add Python to PATH" during installation

2) Library: deep_translator  
   ▸ Install using: `pip install deep-translator`

3) Tool: lconvert (part of Qt tools)
   ▸ Installation:
			 macOS:
				 - `brew install qt`

			 Linux (e.g. Ubuntu):
				 - `sudo apt-get install qttools5-dev-tools`

			 Windows:
				 - Download Qt from: https://www.qt.io/download

4) Test lconvert availability:
     - Run: `lconvert --version`

5) Internet connection is required (translations use Google Translate)
"""
# -------------------------------------------------------------------------------


# Initializing variables - Main
name = "reMarkable"

output_Dir = "output"
output_Language = "cs"

input_QM = f"qm/{name}_en.qm"

intermediate_TS = f"{output_Dir}/{name}_en.ts"

output_TS = f"{output_Dir}/{name}_{output_Language}.ts"
output_QM = f"{output_Dir}/system_Translation_UI.qm"
# -----------------------------------------------------


# Dictionary with your own translations (if the google translation was wrong)
dictionary_Translations = {
		# Full key = Searches by kontextu
    "CreateMenu|Folder|": "Složku",
    "Sidebar|Notebooks|": "Sešitů",
    "Sidebar|Ebooks|": "E-knih",
    "ToolbarPositionMenu|Left": "Levá",
    "ToolbarPositionMenu|Right": "Pravá",

		# Simple key = Searches for all occurrences
		"Large": "Velká",
    "Record ideas, write, and sketch": "Zaznamenávejte nápady, pište a kreslete",
    "Organize your content": "Uspořádejte svůj obsah",
    "Jot down your thoughts": "Zapište své myšlenky",
    "Export": "Exportovat",
    "Duplicate": "Duplikovat",
    "Move": "Presunout",
    "Send by email": "Odeslat e-mailem",
    "General": "Obecné",
    "Unpair": "Zrušit párování",
    "Factory reset": "Obnovení továrního nastavení",
    "Reset": "Obnovit",
    "Release notes": "Poznámky k vydání",
    "Advanced": "Pokročilé",
    "Passcode": "Heslo",
    "Choose the hand you prefer to write and draw with.": "Vyberte ruku, kterou dáváte přednost psaní a kreslení.",
    "Standard": "Standardní",
    "About": "O zařízení",
    "Black": "Černá",
    "White": "Bílá",
    "Thin": "Tenká",
    "Thick": "Tlustá",
    "Selection eraser": "Guma pro výběr",
    "Erase all": "Vymazat vše",
    "Close": "Zavřít",
    "Back": "Zpět",
    "PDFs": "PDF",
    "Search": "Hledat",
    "Create new": "Vytvořit nový (novou)",
    "%1 was moved to Trash": "%1 bylo přesunuto do Koše",
    "New notebook": "Nový sešit",
    "Long-press for quick sheet": "Dlouhé stisknutí pro rychlý list",
    "Sort by": "Třídit podle",
    "Last opened": "Naposledy otevřeno",
    "Alphabetical (A-Z)": "Abecedy (A-Z)",
    "Alphabetical (Z-A)": "Abecedy (Z-A)",
    "File size": "Velikosti souboru",
    "Page count": "Počtu stránek",
    "Filter by": "Filtrovat dle",
    "Tags": "Štítky",
    "Trash": "Koš",
    "Cloud": "Uložiště",
    "Storage": "Disk",
    "Handedness": "Ruka",
    "Grayscale pens": "Pera ve stupních šedi",
    "Last modified": "Naposledy upraveno",
    "Date created": "Datum vytvoření",
}

# Dictionary for correction of all occurrences
# Je to z důvodu, že toto slovo může být použito ve více větách, tak abych nemusel mít jednotlivé věty v dictionary_Translations.
# Protože tam chci upravit pouze toto jedno slovo.
# Již opravuji přeložené slovo.
dictionary_Postprocess = {
    "e -maily": "e-maily",
}
# -------------------------------------------------------------------------------------------------------------------------------


# Number of plural forms according to the target language
map_Plural_Forms = {}

# 1 form (Japanese, Korean, Chinese, Vietnamese, Turkish, Hungarian, Indonesian, Thai)
for lang in ["ja", "ko", "zh", "vi", "tr", "hu", "id", "th"]:
    map_Plural_Forms[lang] = 1

# 2 forms (English, German, French, Spanish, Italian, Portuguese, Dutch, Swedish, Danish, Norwegian, Finnish)
for lang in ["en", "de", "fr", "es", "it", "pt", "nl", "sv", "da", "no", "fi"]:
    map_Plural_Forms[lang] = 2

# 3 forms (Czech, Slovak, Polish, Russian, Ukrainian)
for lang in ["cs", "sk", "pl", "ru", "uk"]:
    map_Plural_Forms[lang] = 3

# 4 forms (Slovenian)
for lang in ["sl"]:
    map_Plural_Forms[lang] = 4

# 6 forms (Arabic)
for lang in ["ar"]:
    map_Plural_Forms[lang] = 6
# -----------------------------------------------------------------------------------------------------------


# Function
def apply_Postprocessing(text):
    for wrong, correct in dictionary_Postprocess.items():
        text = text.replace(wrong, correct)
    return text
# -------------------------------------------------------


# Function
def convert_To_QM(path_File_TS, path_File_QM):
    try:
        subprocess.run(["lconvert", "-i", path_File_TS, "-o", path_File_QM], check=True)
        print(f"{path_File_TS} to {path_File_QM} conversion was successful.")
    except Exception as e:
        print(f"Conversion error ts → qm: {e}")
# --------------------------------------------------------------------------------------


# Function
def convert_To_TS(path_File_QM, path_File_TS):
    try:
        subprocess.run(["lconvert", "-i", path_File_QM, "-o", path_File_TS], check=True)
        print(f"{path_File_QM} to {path_File_TS} conversion was successful.")
    except Exception as e:
        print(f"Conversion error qm → ts: {e}")
# --------------------------------------------------------------------------------------


# Function
def translate_Google(text, source_lang="en", target_Lang="cs"):
    try:
        translated = GoogleTranslator(source=source_lang, target=target_Lang).translate(text)
        return translated.strip()
    except Exception as e:
        print(f"Translation error '{text}': {e}")
        return text
# -------------------------------------------------------------------------------------------

# Function
def clear_Directory(path):
    if os.path.exists(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
# ------------------------------------------------------------------------


def translate_TS(path_Input, output_path_File_TS, output_path_File_QM=None, target_Lang="cs"):
    tree = ET.parse(path_Input)
    root = tree.getroot()

    messages = root.findall(".//message")
    total = len(messages)
    count = 0

    plural_Forms = map_Plural_Forms.get(target_Lang.lower(), 2)  # default 2

    for context in root.findall("context"):
        context_Name = context.find("name").text if context.find("name") is not None else ""
        for message in context.findall("message"):
            count += 1
            percent = (count / total) * 100

            source = message.find("source")
            translation = message.find("translation")
            comment = message.find("comment")

            if source is None or not source.text or source.text.strip() == "":
                continue

            text_Source = source.text.strip()
            text_Comment = comment.text.strip() if comment is not None else ""

            key_Full = f"{context_Name}|{text_Source}|{text_Comment}"
            key_Simple = text_Source

            numerus = message.attrib.get("numerus") == "yes"

            if translation is None:
                translation = ET.SubElement(message, "translation")
                translation.text = ""

            if numerus:
                numerus_Items = translation.findall("numerusform")

                if len(numerus_Items) < plural_Forms:
                    for _ in range(plural_Forms - len(numerus_Items)):
                        ET.SubElement(translation, "numerusform")
                    numerus_Items = translation.findall("numerusform")

                for i, numerusform in enumerate(numerus_Items):
                    original_text = numerusform.text.strip() if numerusform.text else ""

                    if key_Full in dictionary_Translations:
                        text_Translated = dictionary_Translations[key_Full]
                    elif key_Simple in dictionary_Translations:
                        text_Translated = dictionary_Translations[key_Simple]
                    else:
                        text_Translated = translate_Google(original_text, source_lang="en", target_Lang=target_Lang)

                    text_Translated = apply_Postprocessing(text_Translated)
                    numerusform.text = text_Translated
            else:
                if key_Full in dictionary_Translations:
                    translation_Text = dictionary_Translations[key_Full]
                    print(f"[{percent:.1f}%] Translate with custom full key:")
                    print(f"\033[32moriginal   → {key_Full}\033[0m")
                    print(f"\033[31mtranslated → {translation_Text}\033[0m\n")
                    translation.text = translation_Text
                elif key_Simple in dictionary_Translations:
                    translation_Text = dictionary_Translations[key_Simple]
                    print(f"[{percent:.1f}%] Translate with custom simple key:")
                    print(f"\033[32moriginal   → {key_Simple}\033[0m")
                    print(f"\033[31mtranslated → {translation_Text}\033[0m\n")
                    translation.text = translation_Text
                else:
                    if not translation.text or translation.text.strip() == "" or translation.text.strip() == text_Source:
                        translated = translate_Google(text_Source, source_lang="en", target_Lang=target_Lang)
                        translated = apply_Postprocessing(translated)
                        print(f"[{percent:.1f}%] Translate with Google:")
                        print(f"\033[32moriginal   → {text_Source}\033[0m")
                        print(f"\033[31mtranslated → {translated}\033[0m\n")
                        translation.text = translated

    tree.write(output_path_File_TS, encoding="utf-8", xml_declaration=True)
    print(f"\033[1mTranslated file saved to: {output_path_File_TS}\033[0m")

    if output_path_File_QM:
        convert_To_QM(output_path_File_TS, output_path_File_QM)
# -----------------------------------------------------------------------------------------------------------------------


# Main
if __name__ == "__main__":
    clear_Directory("output")

    convert_To_TS(input_QM, intermediate_TS)
    translate_TS(intermediate_TS, output_TS, output_QM, target_Lang=output_Language)
# ----------------------------------------------------------------------------------
