from pathlib import Path
from PIL import Image

SRC = Path("./src/resources/logo-512x512.png")
DST = Path("icon.ico")

sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

def generate_icon():
    img = Image.open(SRC)
    img.save(DST, format='ICO', sizes=sizes)
    print(f"[OK] {DST} updated.")

def main():
    # Si icon.ico n'existe pas → générer
    if not DST.exists():
        print(f"[INFO] {DST} does not exist → generating.")
        generate_icon()
        return

    # Vérifier les dates de modification
    src_mtime = SRC.stat().st_mtime
    dst_mtime = DST.stat().st_mtime

    if src_mtime > dst_mtime:
        print(f"[INFO] Source PNG is newer → regenerating {DST}.")
        generate_icon()
    else:
        print(f"[SKIP] {DST} is up to date.")

if __name__ == "__main__":
    main()
