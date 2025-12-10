import os
import subprocess
import sys
import venv

# Fonction pour créer l'environnement virtuel
def create_virtualenv(env_dir):
    """
    Crée un environnement virtuel dans le répertoire spécifié.

    Cette fonction vérifie si le répertoire `env_dir` existe déjà. Si ce n'est pas le cas, elle crée un nouvel 
    environnement virtuel dans ce répertoire en utilisant le module `venv`. Si le répertoire existe déjà, la 
    fonction affiche un message informant que l'environnement virtuel est déjà présent.

    Arguments :
        env_dir (str) : Le chemin du répertoire où l'environnement virtuel doit être créé.

    Exemple :
        >>> create_virtualenv("venv")
        Création de l'environnement virtuel dans venv...
    """
    if not os.path.exists(env_dir):
        print(f"Création de l'environnement virtuel dans {env_dir}...")
        venv.create(env_dir, with_pip=True)
    else:
        print(f"L'environnement virtuel existe déjà à {env_dir}")

# Fonction pour installer les dépendances
def install_requirements(env_dir):
    """
    Installe les dépendances listées dans le fichier `requirements.txt` dans l'environnement virtuel.

    Cette fonction utilise le gestionnaire de paquets `pip` pour installer les dépendances spécifiées dans le 
    fichier `requirements.txt`. Elle détermine l'emplacement de l'exécutable `pip` en fonction du système 
    d'exploitation (Windows ou non), puis exécute la commande `pip install -r requirements.txt` dans l'environnement 
    virtuel.

    Arguments :
        env_dir (str) : Le chemin du répertoire de l'environnement virtuel où `pip` sera exécuté.

    Exemple :
        >>> install_requirements("venv")
        Installation des dépendances depuis requirements.txt...
    """
    pip_path = os.path.join(env_dir, "bin", "pip") if sys.platform != 'win32' else os.path.join(env_dir, "Scripts", "pip.exe")
    
    print("Installation des dépendances depuis requirements.txt...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])

# Principal
def main():
    """
    Fonction principale pour configurer l'environnement virtuel, installer oracledb et les dépendances.

    Cette fonction crée un environnement virtuel, puis installe la bibliothèque `oracledb` à l'aide de la fonction 
    `install_wheel()`. Ensuite, elle installe les dépendances supplémentaires listées dans `requirements.txt` en 
    utilisant la fonction `install_requirements()`. Enfin, un message est affiché pour informer que l'environnement 
    virtuel est prêt.

    Exemple d'utilisation :
        >>> main()
        Création de l'environnement virtuel dans venv...
        Installation des dépendances depuis requirements.txt...
        L'environnement virtuel est prêt avec les dépendances installées.
    """
    env_dir = "venv"  # Dossier de l'environnement virtuel
    
    # Créer l'environnement virtuel
    create_virtualenv(env_dir)

    # Installer les dépendances
    install_requirements(env_dir)
    
    print("L'environnement virtuel est prêt avec les dépendances installées.")

if __name__ == "__main__":
    main()
