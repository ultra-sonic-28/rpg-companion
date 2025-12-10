# generate_version_info.py
# Génère version_info.txt pour PyInstaller
import os
import datetime
import importlib.util

# --- Chargement dynamique de version.py ---
VERSION_FILE = os.path.join("src", "rpg_companion", "version", "version.py")

spec = importlib.util.spec_from_file_location("version", VERSION_FILE)
version_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version_module)

VERSION_STR = str(version_module.version_app)  # ex: "1.3.2"
VERSION_TUPLE = tuple(map(int, VERSION_STR.split("."))) + (0,) * (4 - len(VERSION_STR.split(".")))

# --- Date compilation ---
TODAY = datetime.datetime.now()
DATE_STR = TODAY.strftime("%Y-%m-%d")
date_today = (TODAY.year, TODAY.month, TODAY.day)
BUILD_DATE_STR = TODAY.strftime("%Y-%m-%d %H:%M:%S")
DATE_TUPLE = (TODAY.year, TODAY.month, TODAY.day, TODAY.hour, TODAY.minute, TODAY.second)

# ----------- Write build_info.py -----------
BUILD_INFO_PATH = os.path.join("src", "rpg_companion", "build_info.py")

with open(BUILD_INFO_PATH, "w", encoding="utf-8") as f:
    f.write(
f'''# Auto-generated during build
BUILD_DATE = "{BUILD_DATE_STR}"
'''
    )

print("[OK] build_info.py généré :", BUILD_INFO_PATH)

# --- Construction du contenu ---
content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={VERSION_TUPLE},
    prodvers={VERSION_TUPLE},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date={date_today}
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',
          [
            StringStruct('CompanyName', 'ultra-sonic-28'),
            StringStruct('FileDescription', 'RPG Companion — Assistant pour jeux de rôle'),
            StringStruct('FileVersion', '{VERSION_STR}'),
            StringStruct('InternalName', 'rpg-companion'),
            StringStruct('LegalCopyright', '© {TODAY.year} ultra-sonic-28'),
            StringStruct('OriginalFilename', 'rpg-companion.exe'),
            StringStruct('ProductName', 'RPG Companion'),
            StringStruct('ProductVersion', '{VERSION_STR}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x0409, 1200])])
  ]
)
"""

# --- Écriture du fichier ---
OUTPUT_FILE = "version_info.txt"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[OK] version_info.txt généré avec la version {VERSION_STR} en date du {DATE_STR}")
