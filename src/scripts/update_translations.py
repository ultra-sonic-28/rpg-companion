# scripts/update_translations.py
import subprocess
from pathlib import Path
import os
import re
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree as ET
from xml.dom import minidom

# -------------------------------------------------------------
# Mise à jour des fichiers .ts
# -------------------------------------------------------------
BASE_DIR = Path("src/rpg_companion")
TS_FILES = [
    BASE_DIR / "i18n" / "en_US.ts",
    BASE_DIR / "i18n" / "fr_FR.ts",
]

TRANSLATION_RE = re.compile(r"""_\(\s*(['"])(.*?)\1\s*\)""")
CLASS_RE = re.compile(r'^class\s+([A-Za-z_][A-Za-z0-9_]*)\s*[\(:]')


def extract_translations():
    results = []
    for filepath in BASE_DIR.rglob("*.py"):
        current_class = None
        with open(filepath, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                cls_match = CLASS_RE.match(line.strip())
                if cls_match:
                    current_class = cls_match.group(1)

                for match in TRANSLATION_RE.finditer(line):
                    text = match.group(2)
                    results.append({
                        "file": str(filepath).replace("\\", "/"),
                        "line": lineno,
                        "class": current_class or "Global",
                        "text": text
                    })
    return results


def load_existing_translations(ts_path):
    """Charge les traductions existantes depuis un .ts"""
    existing = {}
    if ts_path.exists():
        dom = minidom.parse(str(ts_path))
        for context_elem in dom.getElementsByTagName("context"):
            context_name_elem = context_elem.getElementsByTagName("name")[0]
            context_name = context_name_elem.firstChild.nodeValue if context_name_elem.firstChild else ""
            for message_elem in context_elem.getElementsByTagName("message"):
                source_elem = message_elem.getElementsByTagName("source")[0]
                source_text = source_elem.firstChild.nodeValue if source_elem.firstChild else ""
                translation_elem = message_elem.getElementsByTagName("translation")[0]
                translation_text = translation_elem.firstChild.nodeValue if translation_elem.firstChild else ""
                existing[(context_name, source_text)] = translation_text
    return existing

def save_translations(ts_path: Path, messages, existing_translations):
    """
    Sauvegarde les messages extraits dans un fichier TS.
    messages: list de dicts avec keys: text, class, file, line
    existing_translations: dict {(context, text): translation}
    """
    # Compteurs
    translated_count = 0
    untranslated_count = 0
    existing_count = len(existing_translations)
    all = len(messages)

    # Dictionnaire context -> messages
    context_map = {}
    for msg in messages:
        ctx_name = msg["class"] or "Global"
        context_map.setdefault(ctx_name, []).append(msg)

    # Création XML
    root = Element("TS", version="2.1", language=ts_path.stem)
    for ctx_name, msgs in context_map.items():
        ctx_elem = SubElement(root, "context")
        name_elem = SubElement(ctx_elem, "name")
        name_elem.text = ctx_name
        for msg in msgs:
            key = (ctx_name, msg["text"])
            translation_text = existing_translations.get(key, "")
            if translation_text:
                translated_count += 1
            else:
                untranslated_count += 1

            message_elem = SubElement(ctx_elem, "message")
            location_elem = SubElement(message_elem, "location")
            location_elem.set("filename", str(Path(msg["file"]).resolve()))
            location_elem.set("line", str(msg["line"]))

            source_elem = SubElement(message_elem, "source")
            source_elem.text = msg["text"]

            translation_elem = SubElement(message_elem, "translation")
            if translation_text:
                translation_elem.text = translation_text
            else:
                translation_elem.set("type", "unfinished")

    # Formatage lisible
    xml_bytes = ET.tostring(root, encoding="utf-8")  # <- ElementTree.tostring(root)
    xml_dom = minidom.parseString(xml_bytes)
    xml_str = xml_dom.toprettyxml(indent="  ", encoding="utf-8")
    ts_path.write_bytes(xml_str)

    print(f"Updating '{ts_path}'...")
    new = all - existing_count
    print(f"    Found {all} source text(s) ({new} new and {existing_count} already existing: {translated_count} translated, {untranslated_count - new} untranslated)")



# -------------------------------------------------------------
# Compilation des .qm
# -------------------------------------------------------------
def compile_qm():
    print("Compiling .qm files...")
    for ts in TS_FILES:
        subprocess.run(["pyside6-lrelease", str(ts)], check=True)
        #subprocess.run(["../.bintools/linguist_6.10.0/lrelease", str(ts)], check=True)

# -------------------------------------------------------------
# main :)
# -------------------------------------------------------------
extracted = extract_translations()
print(f"Extracted {len(extracted)} strings from Python sources.")

for ts_file in TS_FILES:
    existing = load_existing_translations(ts_file)
    save_translations(ts_file, extracted, existing)

compile_qm()
