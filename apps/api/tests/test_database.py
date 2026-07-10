from app.database import normalize_database_url


def test_normalizes_bare_postgresql_url_to_psycopg_driver():
    url = "postgresql://user:password@host:5432/db"

    normalized = normalize_database_url(url)

    assert normalized == "postgresql+psycopg://user:password@host:5432/db"


def test_leaves_explicit_psycopg_url_unchanged():
    url = "postgresql+psycopg://user:password@host:5432/db"

    normalized = normalize_database_url(url)

    assert normalized == url


def test_leaves_sqlite_url_unchanged():
    url = "sqlite:///./liquidationguard.db"

    normalized = normalize_database_url(url)

    assert normalized == url
