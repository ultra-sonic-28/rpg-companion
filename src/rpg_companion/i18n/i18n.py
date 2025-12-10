# src/rpg_companion/i18n/i18n.py
import builtins
from PySide6.QtCore import QCoreApplication, QObject

def _q(context: str, text: str) -> str:
    """Traduction Qt avec contexte explicite"""
    return QCoreApplication.translate(context, text)

# Installation globale de _() pour tous les modules
def install_global_translation():
    """Installe builtins._ comme wrapper qui utilise la classe appelante comme contexte"""
    import inspect

    def _auto(text: str) -> str:
        frame = inspect.currentframe()

        if frame is None:
            return text
        
        caller = frame.f_back
        if caller is None:
            return text
        
        # Contexte : nom de la classe si présent
        if "self" in caller.f_locals:
            context = caller.f_locals["self"].__class__.__name__
            # Si l'appelant est un QObject, on utilise QObject.tr()
            if isinstance(caller.f_locals["self"], QObject):
                return caller.f_locals["self"].tr(text)
        else:
            # sinon nom du module
            module = caller.f_globals.get("__name__", "")
            context = module.split(".")[-1]
        
        return _q(context, text)

    builtins._ = _auto
