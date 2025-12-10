from rpg_companion.app.application import Application
from rpg_companion.i18n.i18n import install_global_translation

# --- injection globale du _() avant de faire quoique ce soit ---
install_global_translation()

def main() -> int:
    app = Application()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
