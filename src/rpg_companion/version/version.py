"""
Ce module contient la définition de la classe `Version` qui permet de gérer des versions logicielles.

La classe `Version` permet de représenter, manipuler et comparer des versions composées de trois parties :
major, minor et patch. Elle offre des méthodes pour incrémenter ces parties indépendamment et pour
comparer des objets `Version` entre eux.

Les versions suivent la convention de versionnement sémantique (SemVer), où :
- `major` est incrémenté lors de changements incompatibles avec les versions précédentes,
- `minor` est incrémenté lors de l'ajout de nouvelles fonctionnalités de manière rétrocompatible,
- `patch` est incrémenté pour des corrections de bugs ou des améliorations mineures.

Fonctionnalités principales :
- Incrémenter les parties `major`, `minor`, et `patch` d'une version.
- Comparer deux versions logicielles pour déterminer leur ordre relatif.
- Convertir une version en chaîne de caractères pour un affichage facile.

Classes:
    - `Version`: Représente une version logicielle avec des méthodes pour manipuler et comparer les versions.

Méthodes :
    - `increment_major`: Incrémente la version majeure et réinitialise la version mineure et patch à 0.
    - `increment_minor`: Incrémente la version mineure et réinitialise la version patch à 0.
    - `increment_patch`: Incrémente la version de correction (patch).
    - `compare`: Compare la version actuelle avec une autre version.
    - `__str__`: Retourne la version sous forme de chaîne de caractères.
"""
class Version:
    """
    Représente une version logicielle composée de trois parties : major, minor et patch.

    Cette classe permet de définir, incrémenter et comparer des versions logicielles, 
    en suivant la convention de versionnement sémantique (SemVer). Elle permet de manipuler
    les versions sous forme d'entiers, avec la possibilité d'incrémenter les parties major, 
    minor et patch indépendamment.

    Attributes:
        major (int): La version majeure.
        minor (int): La version mineure.
        patch (int): La version de correction (patch).

    Methods:
        __str__: Retourne une chaîne représentant la version au format "major.minor.patch".
        increment_major: Incrémente la version majeure et réinitialise la version mineure et patch à 0.
        increment_minor: Incrémente la version mineure et réinitialise le patch à 0.
        increment_patch: Incrémente la version patch.
        compare: Compare la version actuelle avec une autre version et retourne la différence sous forme d'entier.
    """

    def __init__(self, major, minor, patch) -> None:
        """
        Initialise une instance de la classe Version.

        Args:
            major (int): La version majeure.
            minor (int): La version mineure.
            patch (int): La version de correction (patch).
        """
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self) -> str:
        """
        Retourne la version sous forme de chaîne de caractères.

        Returns:
            str: La version sous la forme "major.minor.patch".
        """
        return f"{self.major}.{self.minor}.{self.patch}"

    def increment_major(self) -> "Version":
        """
        Incrémente la version majeure et réinitialise la version mineure et patch.

        Cette méthode met à jour la version majeure, et réinitialise la version mineure et
        la version patch à 0. Elle suit la convention du versionnement sémantique pour
        marquer une nouvelle version majeure.

        Returns:
            Version: L'objet `Version` actuel avec la version majeure incrémentée.
        """
        self.major += 1
        self.minor = 0  # Réinitialise les autres parties
        self.patch = 0
        return self

    def increment_minor(self) -> "Version":
        """
        Incrémente la version mineure et réinitialise la version patch.

        Cette méthode met à jour la version mineure et réinitialise la version patch à 0,
        suivant ainsi les règles du versionnement sémantique pour l'ajout de nouvelles
        fonctionnalités de manière rétrocompatible.

        Returns:
            Version: L'objet `Version` actuel avec la version mineure incrémentée.
        """
        self.minor += 1
        self.patch = 0  # Réinitialise le patch
        return self

    def increment_patch(self) -> "Version":
        """
        Incrémente la version de correction (patch).

        Cette méthode incrémente uniquement la version de correction (patch), idéale
        pour les corrections de bugs et les petites améliorations sans rupture de compatibilité.

        Returns:
            Version: L'objet `Version` actuel avec la version patch incrémentée.
        """
        self.patch += 1
        return self

    def compare(self, other) -> int:
        """
        Compare la version actuelle avec une autre version.

        Cette méthode compare les versions de manière séquentielle en utilisant les 
        attributs `major`, `minor` et `patch`. Si la version actuelle est supérieure, 
        un entier positif est retourné ; si elle est inférieure, un entier négatif est 
        retourné ; sinon, 0 est retourné.

        Args:
            other (Version): L'autre objet `Version` à comparer.

        Returns:
            int: Un entier représentant la différence entre les deux versions :
                 - > 0 si la version actuelle est supérieure.
                 - < 0 si la version actuelle est inférieure.
                 - 0 si les versions sont identiques.
        """
        if self.major != other.major:
            return self.major - other.major
        if self.minor != other.minor:
            return self.minor - other.minor
        return self.patch - other.patch

version_app = Version(0, 1, 0)
