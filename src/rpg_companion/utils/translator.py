import logging
from PySide6.QtCore import QTranslator, QLocale, QLibraryInfo, QCoreApplication

from PySide6.QtWidgets import QApplication

from rpg_companion.config.config_manager import ConfigManager
import rpg_companion.i18n.translations_rc  # important pour PyInstaller

class Translator:
    _instance = None

    def __init__(self):
        self.config = ConfigManager()
        self.translator = QTranslator()
        self.current_lang = None
        self.log = logging.getLogger("rpg_companion")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Translator()
        return cls._instance

    def load_language(self, lang_code: str):
        """Charge une langue (ex: 'fr_FR', 'en_US')"""

        if self.current_lang == lang_code:
            return  # déjà chargé

        qm_path = f":/i18n/{lang_code}.qm"

        if self.translator.load(qm_path):
            self.current_lang = lang_code
            QApplication.instance().installTranslator(self.translator)
            self.log.info(f"[i18n] Loaded language: {lang_code}")
        else:
            self.log.error(f"[i18n] Failed to load translation: {qm_path}")

    def reload_from_config(self):
        lang = self.config.general()["language"]
        self.load_language(lang)
