from typing import Dict, Any

from rpg_companion.ui.views.result_webview import ResultWebView


# Pour éviter le warning Pylance sur "_" utilisé pour la localisation
_: Any


class ItemResultWebView(ResultWebView):
    """
    Vue web affichant les résultats de tirage pour les objets (item).
    Surcharge uniquement la méthode `_format_result`.
    Elle correspond exactement au modèle Item.to_dict().
    """

    def _format_result(self, result: Dict[str, Any]) -> str:
        """Retourne un bloc HTML décrivant un objet."""

        # Libellés localisés
        strRoll        = _("Jet")
        strRange       = _("Intervalle")
        strDetails     = _("Détails")
        strValue       = _("Valeur")

        return f"""
        <table class="entry">
            <tr>
                <td class="label">{strRoll}</td>
                <td class="data">{result.get('roll')}</td>
            </tr>
            <tr>
                <td class="label">{strRange}</td>
                <td class="data">{result.get('range')}</td>
            </tr>
            <tr>
                <td class="label">{strDetails}</td>
                <td class="data">{result.get('details')}</td>
            </tr>
            <tr>
                <td class="label">{strValue}</td>
                <td class="data">{result.get('value')}</td>
            </tr>
        </table>
        """
