import pytest

from rpg_companion.version.version import Version

def test_version_str():
    version = Version(1, 2, 3)
    assert str(version) == "1.2.3"

def test_increment_major():
    version = Version(1, 2, 3)
    version.increment_major()
    assert (version.major, version.minor, version.patch) == (2, 0, 0)

def test_increment_minor():
    version = Version(1, 2, 3)
    version.increment_minor()
    assert (version.major, version.minor, version.patch) == (1, 3, 0)

def test_increment_patch():
    version = Version(1, 2, 3)
    version.increment_patch()
    assert (version.major, version.minor, version.patch) == (1, 2, 4)

@pytest.mark.parametrize("v1, v2, expected", [
    (Version(1, 0, 0), Version(1, 0, 0), 0),       # égales
    (Version(2, 0, 0), Version(1, 0, 0), 1),       # major > major
    (Version(1, 1, 0), Version(1, 0, 5), 1),       # minor > minor
    (Version(1, 0, 2), Version(1, 0, 1), 1),       # patch > patch
    (Version(1, 0, 0), Version(2, 0, 0), -1),      # major < major
    (Version(1, 0, 4), Version(1, 1, 0), -1),      # minor < minor
    (Version(1, 0, 1), Version(1, 0, 2), -1),      # patch < patch
])
def test_compare_versions(v1, v2, expected):
    if expected == 0:
        assert v1.compare(v2) == 0
    elif expected > 0:
        assert v1.compare(v2) > 0
    else:
        assert v1.compare(v2) < 0

def test_chained_increments():
    version = Version(1, 2, 3)
    version.increment_patch().increment_minor().increment_major()
    assert str(version) == "2.0.0"
