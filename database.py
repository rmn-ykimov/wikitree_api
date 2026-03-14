import sqlite3
from typing import Optional

DB_NAME = "profiles.db"


def init_db():
    """Создает таблицу профилей, если она не существует."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                page_name TEXT PRIMARY KEY,
                first_name TEXT,
                lnab TEXT,
                birth_year INTEGER,
                death_year INTEGER
            )
        """)
        conn.commit()

def save_profile(
        page_name: str,
        first_name: Optional[str],
        lnab: str,
        birth_year: Optional[int],
        death_year: Optional[int]
        ):
    """Сохраняет или обновляет профиль в базе данных."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO profiles (page_name, first_name, lnab, birth_year, death_year)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(page_name) DO UPDATE SET
                first_name=excluded.first_name,
                lnab=excluded.lnab,
                birth_year=excluded.birth_year,
                death_year=excluded.death_year
        """, (page_name, first_name, lnab, birth_year, death_year))
        conn.commit()
