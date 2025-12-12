from typing import Dict, Any

from rpg_companion.ui.views.result_webview import ResultWebView


# Pour éviter le warning Pylance sur "_" utilisé pour la localisation
_: Any


class ArmorResultWebView(ResultWebView):
    """
    Vue web affichant les résultats de tirage pour les armures.
    Surcharge uniquement la méthode `_format_result`.
    Elle correspond exactement au modèle Armor.to_dict().
    """

    def _format_result(self, result: Dict[str, Any]) -> str:
        """Retourne un bloc HTML décrivant une armure."""

        # Libellés localisés
        strRoll        = _("Jet")
        strRange       = _("Intervalle")
        strName        = _("Nom")
        strSlot        = _("Emplacement")
        strType        = _("Type")
        strASModifier  = _("Modificateur AS")
        strValue       = _("Valeur")
        strFixCost     = _("Réparation")

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
                <td class="label">{strName}</td>
                <td class="data">{result.get('name')}</td>
            </tr>
            <tr>
                <td class="label">{strSlot}</td>
                <td class="data">{result.get('slot')}</td>
            </tr>
            <tr>
                <td class="label">{strType}</td>
                <td class="data">{result.get('type')}</td>
            </tr>
            <tr>
                <td class="label">{strASModifier}</td>
                <td class="data">{result.get('as_modifier')}</td>
            </tr>
            <tr>
                <td class="label">{strValue}</td>
                <td class="data">{result.get('value')}</td>
            </tr>
            <tr>
                <td class="label">{strFixCost}</td>
                <td class="data">{result.get('fix_cost')}</td>
            </tr>
        </table>
        """
