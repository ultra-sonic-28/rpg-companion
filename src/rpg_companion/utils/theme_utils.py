import subprocess
import sys

if sys.platform.startswith("win"):
    import winreg
elif sys.platform == "darwin":
    import subprocess


def is_windows_dark_mode() -> bool:
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0  # 0 = dark, 1 = light
    except Exception:
        return False


def is_macos_dark_mode() -> bool:
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True, text=True
        )
        return result.stdout.strip().lower() == "dark"
    except Exception:
        return False


def get_system_theme() -> str:
    """
    Retourne "dark" ou "light" selon le thème système.
    Par défaut "light" si non détectable ou Linux.
    """
    if sys.platform.startswith("win"):
        return "dark" if is_windows_dark_mode() else "light"
    elif sys.platform == "darwin":
        return "dark" if is_macos_dark_mode() else "light"
    else:
        return "light"
