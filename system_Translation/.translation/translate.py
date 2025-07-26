# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
# ------------------------------------------


# Number of plural forms according to the output language
map_Plural_Forms = {}

# 1 form (Japanese, Korean, Chinese, Vietnamese, Turkish, Hungarian, Indonesian, Thai)
for lang in ["ja", "ko", "zh", "vi", "tr", "hu", "id", "th"]:
    map_Plural_Forms[lang] = 1

# 2 forms (French, Spanish, Italian, Portuguese, Dutch, Swedish, Danish, Norwegian, Finnish)
for lang in ["en", "de", "fr", "es", "it", "pt", "nl", "sv", "da", "no", "fi", "et", "el", "is", "nb"]:
    map_Plural_Forms[lang] = 2

# 3 forms (Czech, Slovak, Polish, Russian, Ukrainian)
for lang in ["cs", "sk", "pl", "ru", "uk", "ro"]:
    map_Plural_Forms[lang] = 3

# 4 forms (Slovenian)
for lang in ["sl"]:
    map_Plural_Forms[lang] = 4

# 6 forms (Arabic)
for lang in ["ar"]:
    map_Plural_Forms[lang] = 6
# -----------------------------------------------------------------------------------------------------------


# Function
def apply_Postprocessing(text, dictionary_Postprocess):
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
def load_Translations(json_path):
    if not os.path.isfile(json_path):
        print(f"\nWarning: Translation JSON file '{json_path}' not found. Using empty dictionaries.")
        return {}, {}
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("dictionary_Translations", {}), data.get("dictionary_Postprocess", {})
# -------------------------------------------------------------------------------------------------


# Function
def translate_Google(text, input_Language=None, output_Language=None):
    try:
        translated = GoogleTranslator(source=input_Language, target=output_Language).translate(text)
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

# Function
def translate_TS(path_Input, output_path_File_TS, output_path_File_QM=None, output_Language=None, input_Language=None, dictionary_Translations=None, dictionary_Postprocess=None, text_Styles=None):
    if dictionary_Translations is None:
        dictionary_Translations = {}
    if dictionary_Postprocess is None:
        dictionary_Postprocess = {}

    tree = ET.parse(path_Input)
    root = tree.getroot()

    messages = root.findall(".//message")
    total = len(messages)
    count = 0

    plural_Forms = map_Plural_Forms[output_Language.lower()]

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
                        text_Translated = translate_Google(original_text, input_Language=input_Language, output_Language=output_Language)

                    text_Translated = apply_Postprocessing(text_Translated, dictionary_Postprocess)
                    numerusform.text = text_Translated
            else:
                if key_Full in dictionary_Translations:
                    translation_Text = dictionary_Translations[key_Full]
                    print(f"[{percent:.2f}%] Translate with custom full key: (from {input_Language} to {output_Language})")
                    print(f"{text_Styles['green']}original   → {key_Full}{text_Styles['reset']}")
                    print(f"{text_Styles['red']}translated → {translation_Text}{text_Styles['reset']}\n")
                    translation.text = translation_Text
                elif key_Simple in dictionary_Translations:
                    translation_Text = dictionary_Translations[key_Simple]
                    print(f"[{percent:.2f}%] Translate with custom simple key: (from {input_Language} to {output_Language})")
                    print(f"{text_Styles['green']}original   → {key_Simple}{text_Styles['reset']}")
                    print(f"{text_Styles['red']}translated → {translation_Text}{text_Styles['reset']}\n")
                    translation.text = translation_Text
                else:
                    # Pokud budu chtít kontrolu jestli v <translation></translation> již něco je, aby nepřekládalo znovu
                    # if not translation.text or translation.text.strip() == "" or translation.text.strip() == text_Source:
                        translated = translate_Google(text_Source, input_Language=input_Language, output_Language=output_Language)
                        translated = apply_Postprocessing(translated, dictionary_Postprocess)
                        print(f"\n[{percent:.2f}%] Translate with Google: (from {input_Language} to {output_Language})")
                        print(f"{text_Styles['green']}original   → {text_Source}{text_Styles['reset']}")
                        print(f"{text_Styles['red']}translated → {translated}{text_Styles['reset']}")
                        translation.text = translated

    tree.write(output_path_File_TS, encoding="utf-8", xml_declaration=True)
    print(f"\n{text_Styles['bold']}Translated file saved to: {output_path_File_TS}{text_Styles['reset']}")

    if output_path_File_QM:
        convert_To_QM(output_path_File_TS, output_path_File_QM)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Main
if __name__ == "__main__":

    try:
        # ============================================= ⚠️ LANGUAGE CONFIG WARNING ⚠️ ==============================================
        #
        #   The "available_languages" list below must match the one defined in:
        #       • system_Translation.qmd (like: var languages_New = [new_Language])
        #       • application.qrc        (like: <file>translations/reMarkable_[new_Language].qm</file>)
        #
        #   Please make sure the language is included in the "map_Plural_Forms" below!
        #
        # ==========================================================================================================================


        # --------------------------------------------------  USER CONFIGURATION  --------------------------------------------------

        name = "reMarkable"
        file_Language = "de"

        input_Language = "en"
        input_QM = f"input/{name}_{file_Language}.qm"

        intermediate_TS = f"input/{name}_{file_Language}.ts"
        available_languages = ["cs", "da", "el", "es", "et", "fi", "fr", "hu", "is", "it", "nb", "nl", "pl", "pt", "ro", "sk", "sv"]
        # --------------------------------------------------------------------------------------------------------------------------


        # ---------------------------------------------  OTHER CONFIGURATION  ---------------------------------------------

        # Terminal colors
        text_Styles = {
            "red": "\033[91m",
            "green": "\033[32m",
            "bold": "\033[1m",
            "italic": "\033[3m",
            "reset": "\033[0m"
        }

        # Welcome (about)
        text_Welcome = (
            f"\n"
            f"    {text_Styles['bold']}Welcome to the Qt TS/QM translation script!{text_Styles['reset']}\n"
            f"    This script translates texts from English to your chosen languages using Google Translate.\n\n"
            f"    Make sure you have internet connection and required tools installed.\n"
            f"    {text_Styles['italic']}Available languages: ({', '.join(available_languages)}){text_Styles['reset']}\n"
            f"    ==========================================================================================\n"
        )

        # Ask user for output languages (same as before)
        text_Output_Language = (
            f"\n"
            f"{text_Styles['bold']}Enter the output language code(s) separated by comma:{text_Styles['reset']}\n"
            f"Your choice please: "
        )

        # Ask user for input plural
        text_Input_Plurar = (
            f"\n"
            f"{text_Styles['bold']}Please enter the number of plural forms for this language (1-6).{text_Styles['reset']}\n"
            f"Language '{lang}' is not in the plural forms map (so manual input is needed).\n"
            f"This means how many different plural forms the language uses.\n\n"
            f"{text_Styles['italic']}Examples:\n"
            f" - 1: Japanese, Korean (no plural)\n"
            f" - 2: English, French\n"
            f" - 3: Czech, Polish\n"
            f" - 4: Slovenian\n"
            f" - 6: Arabic\n{text_Styles['reset']}\n"
            f"Your input: "
        )
        # ------------------------------------------------------------------------------------------------------------------

        
        # -------------------------------------------------------------  START PYTHON SCRIPT  -------------------------------------------------------------
        print(text_Welcome)

        # Prompt user to select valid output languages and define their plural form if needed
        while True:
            user_input = input(text_Output_Language).strip().lower()
            selected_languages = [lang.strip() for lang in user_input.split(",") if lang.strip()]

            valid_languages = []
            error_found = False

            for lang in selected_languages:
                if lang not in available_languages:
                    print(f"\n{text_Styles['red']}Language '{lang}' is not in the \"available_languages\" list.{text_Styles['reset']} Please try again.")
                    error_found = True
                    break

            if error_found:
                continue

            for lang in selected_languages:
                if lang not in map_Plural_Forms:
                    while True:
                        plural_input = input(text_Input_Plurar).strip()

                        if plural_input.isdigit() and int(plural_input) in [1, 2, 3, 4, 6]:
                            map_Plural_Forms[lang] = int(plural_input)
                            break
                        else:
                            print(f"{text_Styles['red']}Invalid input. Please enter one of the following numbers: 1-6.{text_Styles['reset']}")
                valid_languages.append(lang)

            if valid_languages:
                break
            else:
                print(f"\n{text_Styles['red']}No valid languages selected.{text_Styles['reset']} Please try again.")

        # Proceed with translations as before
        for output_Language in selected_languages:
            print(f"\n{text_Styles['bold']}Starting translation for: {output_Language}{text_Styles['reset']}")

            output_Dir = f"output/{output_Language}"
            output_TS = f"{output_Dir}/{name}_{output_Language}.ts"
            output_QM = f"{output_Dir}/{name}_{output_Language}.qm"

            json_file = f"custom_Translations/translations_{output_Language}.json"
            dictionary_Translations, dictionary_Postprocess = load_Translations(json_file)

            os.makedirs(output_Dir, exist_ok=True)
            clear_Directory(output_Dir)

            if os.path.exists(intermediate_TS):
                os.remove(intermediate_TS)
                print(f"Removed old intermediate TS: {intermediate_TS}")

            convert_To_TS(input_QM, intermediate_TS)

            translate_TS(
                intermediate_TS,
                output_TS,
                output_QM,
                input_Language=input_Language,
                output_Language=output_Language,
                dictionary_Translations=dictionary_Translations,
                dictionary_Postprocess=dictionary_Postprocess,
                text_Styles=text_Styles
            )
        # -------------------------------------------------------------------------------------------------------------------------------------------------

    except KeyboardInterrupt:
        print("\n\nTranslation script aborted by user (Ctrl+C). Exiting...\n")
        sys.exit(0)

# End main