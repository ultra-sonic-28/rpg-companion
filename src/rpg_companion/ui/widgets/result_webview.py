from typing import Any
from PySide6.QtCore import Qt, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from rpg_companion.types.weapon_hands_type import WeaponHandsType

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class ResultWebView(QWebEngineView):
    # Signal pour notifier qu'un nouveau tirage doit être effectué
    request_new_roll = Signal()
    
    def __init__(self, title=None, parent=None, bridge_callback=None, initial_theme="light"):
        super().__init__(parent)
        self.parent = parent
        self.bridge_callback = bridge_callback

        self.title = title or _("Résultats")
        self.theme = initial_theme
        self.loaded = False
        self.pending_entries = []

        self.channel = None
        self.bridge = None

        html = self._create_base_html(self.theme)
        self.setHtml(html)

        self.loadFinished.connect(self._on_loaded)
        self.setAttribute(Qt.WA_DeleteOnClose)

    # ---------------------------------------------------------
    # CSS Light & Dark
    # ---------------------------------------------------------
    def _css_light(self):
        return """
        body { background: #fafafa; color: #222; }
        h1 { color: #444; border-bottom: 1px solid #ccc; }
        #clear-btn { background: #c62828; color: white; }
        #roll-btn { background: #2e7d32; color: white; }
        .entry { background: white; border: 1px solid #ccc; }
        """

    def _css_dark(self):
        return """
        body { background: #1e1e1e; color: #ddd; }
        h1 { color: #eee; border-bottom: 1px solid #555; }
        #clear-btn { background: #9d2525; color: white; }
        #roll-btn { background: #2e7d32; color: white; }
        .entry { background: #2b2b2b; border: 1px solid #555; }
        """

    def _get_css(self, theme):
        return self._css_dark() if theme == "dark" else self._css_light()

    # ---------------------------------------------------------
    # HTML de base
    # ---------------------------------------------------------
    def _create_base_html(self, theme):
        css = self._get_css(theme)
        color_scheme = "dark" if theme == "dark" else "light"
        strBtnNewRoll = _("Effectuer un nouveau tirage")
        strBtnClearHisto = _("Effacer l'historique")
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="color-scheme" content="{color_scheme}">
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <style>
            {css}

            .entry {{
                padding: 10px;
                margin-bottom: 15px;
                border-radius: 6px;
                box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
            }}

            .label {{ 
                width: 250px;
                font-weight: bold; 
            }}

            .data {{ 
                width: 200px;
            }}

            #clear-btn, #roll-btn {{
                border: none;
                padding: 8px 14px;
                border-radius: 4px;
                cursor: pointer;
                margin-bottom: 15px;
                margin-right: 5px;
            }}
            </style>
        </head>
        <body>
            <h1>{self.title}</h1>

            <button id="roll-btn"
                onclick="pyRequestNewRoll();">
                {strBtnNewRoll}
            </button>

            <button id="clear-btn"
                onclick="document.getElementById('entries').innerHTML = ''; window.scrollTo(0, 0);">
                {strBtnClearHisto}
            </button>

            <div id="entries"></div>

            <script>
                // Cette fonction sera connectée au signal Python
                function pyRequestNewRoll() {{
                    if (window.bridge) {{
                        window.bridge.request_new_roll();
                    }} else {{
                        console.error("Bridge not ready");
                    }}
                }}
            </script>
        </body>
        </html>
        """

    # ---------------------------------------------------------
    # Changement de thème dynamique
    # ---------------------------------------------------------
    def set_theme(self, theme):
        self.theme = theme
        css = self._get_css(theme)

        # Remplace seulement le CSS via JS, sans recharger toute la page
        js = f"""
        document.querySelector('style').innerHTML = `{css}`;
        """
        self.page().runJavaScript(js)

    # ---------------------------------------------------------
    # Page chargée → on vide les entrées en attente
    # ---------------------------------------------------------
    def _on_loaded(self, ok):
        self.loaded = ok

        # Crée le bridge seulement après le chargement complet
        from rpg_companion.ui.bridge import Bridge
        self.bridge = Bridge(callback=self.bridge_callback)  # callback = fonction Python pour le tirage
        self.channel = QWebChannel(self.page())
        self.channel.registerObject("bridge", self.bridge)
        self.page().setWebChannel(self.channel)
        
        init_js = """
            if (typeof QWebChannel !== 'undefined') {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.bridge = channel.objects.bridge;
                });
            } else {
                console.error("QWebChannel not defined!");
            }
        """

        self.page().runJavaScript(init_js)
        
        for entry in self.pending_entries:
            self._inject_html(entry)
        self.pending_entries.clear()

    # ---------------------------------------------------------
    # Ajout de résultats
    # ---------------------------------------------------------
    def append(self, result_dict: dict):
        html_entry = self._format_result(result_dict)

        if not self.loaded:
            self.pending_entries.insert(0, html_entry)
            return

        self._inject_html(html_entry)

    # ---------------------------------------------------------
    # HTML pour une entrée
    # ---------------------------------------------------------
    def _format_result(self, result):
        desc = result.get("description", "")
        strRoll = _("Jet")
        strRange = _("Intervalle")
        strName = _("Nom")
        strHandLibs = _("Main")
        strHands = (
            WeaponHandsType.ONE_HAND.label
            if result["hands"] == 1
            else WeaponHandsType.TWO_HANDS.label
        )
        strType = _("Type")
        strDamage = _("Dégats")
        strValue = _("Valeur")
        strFixCost= _("Réparation")
        strDescription = _("Description")

        return f"""
        <table class="entry">
            <tr>
                <td class="label">{strRoll}</td>
                <td class="data">{result['roll']}</td>
            </tr>
            <tr>
                <td class="label">{strRange}</td>
                <td class="data">{result['range']}</td>
            </tr>
            <tr>
                <td class="label">{strName}</td>
                <td class="data">{result['name']}</td>
            </tr>
            <tr>
                <td class="label">{strHandLibs}</td>
                <td class="data">{result['hands']}</td>
            </tr>
            <tr>
                <td class="label">{strType}</td>
                <td class="data">{result['type']}</td>
            </tr>
            <tr>
                <td class="label">{strDamage}</td>
                <td class="data">{result['damage']}</td>
            </tr>
            <tr>
                <td class="label">{strValue}</td>
                <td class="data">{result['value']}</td>
            </tr>
            <tr>
                <td class="label">{strFixCost}</td>
                <td class="data">{result['fix_cost']}</td>
            </tr>
            <tr>
                <td class="label">{strDescription}</td>
                <td class="data">{desc}</td>
            </tr>
        </table>
        """

    # ---------------------------------------------------------
    # Injection JS
    # ---------------------------------------------------------
    def _inject_html(self, html_entry):
        js = f"""
        document.getElementById("entries")
            .insertAdjacentHTML("afterbegin", `{html_entry}`);
        window.scrollTo(0, 0);
        """
        self.page().runJavaScript(js)

    # ---------------------------------------------------------
    # Vider l'historique
    # ---------------------------------------------------------
    def clear_history(self):
        self.pending_entries.clear()
        self.page().runJavaScript("""
            document.getElementById("entries").innerHTML = "";
            window.scrollTo(0, 0);
        """)
