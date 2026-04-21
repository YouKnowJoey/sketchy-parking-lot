'''
Project Name: Sketchy Parking Lot
Authors: Joey Garcia and Reilly Rodriguez Spencer

Purpose: Use Fasttext language identification to predict text language. The language will be used as a feature in the unsupervised learning pipeline.
'''

from pathlib import Path
import fasttext

class SketchyLangID:
    def __init__(self):
        BASE_DIR = Path().resolve().parent
        self.MODEL_PATH = BASE_DIR / "models" / "lid.176.ftz"
        self.model = fasttext.load_model(str(self.MODEL_PATH))

    def clean_text_lang(self, text):
        if not isinstance(text, str):
            return ""
        return text.replace("\n", " ").strip()

    def detect_language(self, text):
        if not isinstance(text, str) or text.strip() == "":
            return "0"

        clean_text = self.clean_text_lang(text)
        prediction = self.model.predict(clean_text)
        lang = prediction[0][0].replace("__label__", "")
        confidence = prediction[1][0]

        return lang, confidence
