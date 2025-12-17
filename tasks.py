import shutil
import subprocess
import sys

from invoke import task

def updateTranslations():
    python_executable = sys.executable
    cmd = [python_executable, './src/scripts/update_translations.py']
    result = subprocess.run(cmd, encoding="utf-8")

    cmd = [
        'pyside6-rcc', 
        'src/rpg_companion/i18n/translations.qrc', 
        '-o', 'src/rpg_companion/i18n/translations_rc.py',
    ]
    result = subprocess.run(cmd, encoding="utf-8")

@task
def test(c):
    """Exécute les tests unitaires avec pytest."""
    cmd = ['pytest', '-x', '--color=yes']
    result = subprocess.run(cmd, encoding="utf-8")

@task
def coverage(c):
    """Lance les tests avec couverture et génère un rapport HTML."""
    cmd = ['pytest', '--color=yes', '--cov=rpg_companion', '--cov-report=html',  './src/__tests__/']
    result = subprocess.run(cmd, encoding="utf-8")

@task
def ico(c):
    """
    Génération de l'icone
    """
    python_executable = sys.executable
    cmd = [python_executable, './src/scripts/make_icon.py']
    result = subprocess.run(cmd, encoding="utf-8")

@task(pre=[ico])
def rpg(c):
    """
    Exécution de RPG Companion
    """
    python_executable = sys.executable

    updateTranslations()

    cmd = [python_executable, './src/main.py']
    result = subprocess.run(cmd, encoding="utf-8")

@task(pre=[ico])
def build(c):
    """
    Construction de l'exécutable
    """
    python_executable = sys.executable
    cmd = [python_executable, './src/scripts/make_version_info.py']
    result = subprocess.run(cmd, encoding="utf-8")

    updateTranslations()

    # Construction des arguments de la ligne de commande
    exec_name = 'RpgCompanion'
    cmd = [
        'pyinstaller', 
        '--name', exec_name, 
        '--onedir', 
        '--windowed', 
        '--noconfirm', 
        '--icon=icon.ico',
        '--add-data', 'src/rpg_companion/assets/:./rpg_companion/assets/', 
        '--add-data', 'src/rpg_companion/data/:./rpg_companion/data/', 
        '--version-file=version_info.txt',
        'src/main.py'
    ]

    result = subprocess.run(cmd, encoding="utf-8")
