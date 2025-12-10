from typing import Dict, Any

from rpg_companion.types.weapon_hands_type import WeaponHandsType
from rpg_companion.ui.views.result_webview import ResultWebView


# Pour éviter le warning Pylance sur "_" utilisé pour la localisation
_: Any


class WeaponsResultWebView(ResultWebView):
    """
    Vue web affichant les résultats de tirages pour les armes.
    Surcharge uniquement la méthode `_format_result`.
    """

    def _format_result(self, result: Dict[str, Any]) -> str:
        """Retourne un bloc HTML affichant les infos d'une arme."""

        # Localisation
        strRoll       = _("Jet")
        strRange      = _("Intervalle")
        strName       = _("Nom")
        strHandsLabel = _("Main")
        strType       = _("Type")
        strDamage     = _("Dégâts")
        strValue      = _("Valeur")
        strFixCost    = _("Réparation")
        strDescription = _("Description")

        # Conversion 1 main / 2 mains
        hands_str = (
            WeaponHandsType.ONE_HAND.label
            if result.get("hands") == 1
            else WeaponHandsType.TWO_HANDS.label
        )

        desc = result.get("description", "")

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
                <td class="label">{strHandsLabel}</td>
                <td class="data">{hands_str}</td>
            </tr>
            <tr>
                <td class="label">{strType}</td>
                <td class="data">{result.get('type')}</td>
            </tr>
            <tr>
                <td class="label">{strDamage}</td>
                <td class="data">{result.get('damage')}</td>
            </tr>
            <tr>
                <td class="label">{strValue}</td>
                <td class="data">{result.get('value')}</td>
            </tr>
            <tr>
                <td class="label">{strFixCost}</td>
                <td class="data">{result.get('fix_cost')}</td>
            </tr>
            <tr>
                <td class="label">{strDescription}</td>
                <td class="data">{desc}</td>
            </tr>
        </table>
        """
