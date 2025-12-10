import re
from datetime import datetime
from rpg_companion.build_info import BUILD_DATE


def test_build_date_is_string():
    """Vérifie que BUILD_DATE est bien une chaîne."""
    assert isinstance(BUILD_DATE, str)


def test_build_date_format():
    """
    Vérifie que BUILD_DATE respecte le format :
    YYYY-MM-DD HH:MM:SS
    """
    date_str = BUILD_DATE

    # Format attendu via datetime
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        assert False, f"BUILD_DATE n'est pas au bon format : {e}"

    # Vérification supplémentaire via regex (optionnelle mais stricte)
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    assert re.match(pattern, date_str), "Le format ne correspond pas strictement à YYYY-MM-DD HH:MM:SS"
