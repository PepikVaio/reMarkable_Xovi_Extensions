# Requirements:
# -------------

1) Python 3.x
  ▸ Check version: `python3 --version` or `python --version`
  ▸ Installation:
    ▸ macOS:
      - Use Homebrew: `brew install python`
    ▸ Linux (Ubuntu/Debian):
      - `sudo apt update && sudo apt install python3`
    ▸ Windows:
      - Download the installer from: https://www.python.org/downloads/windows/
      - Make sure to check "Add Python to PATH" during installation

2) Library: deep_translator
  ▸ Install using: `pip install deep-translator` (or via requirements.txt file)

3) Tool: lconvert (part of Qt tools)
  ▸ Installation:
    ▸ macOS:
      - `brew install qt`
    ▸ Linux (e.g. Ubuntu):
      - `sudo apt-get install qttools5-dev-tools`
    ▸ Windows:
      - Download Qt from: https://www.qt.io/download

  ▸ Test: (lconvert availability)
    ▸ Run: `lconvert --version`

4) Internet connection is required (translations use Google Translate)


# Description:
# ------------

Folder custom_Translation: (you can add more files, look at the translations_cs.json)
  ▸ Json files with corrected phrases, because not everything will translate correctly

    ▸ dictionary_Translations
      - Dictionary with your own translations (if the google translation was wrong)
      - _comment_Full
        ▸ Searches by kontext
      - _comment_Simple
        ▸ Searches for all occurrences

    ▸ dictionary_Postprocess
      - Dictionary for correction of all occurrences

Folder input:
  ▸ QM file with texts from reMarkable

Folder output: (python script fills with data)
  ▸ QM and TS files with translated texts from input QM file



# Run script
# ----------

python3 translate.py
