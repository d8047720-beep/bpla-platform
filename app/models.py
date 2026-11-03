import os
import json
import sqlite3
from contextlib import contextmanager
from app.config import DATABASE


SCHEMA = """
CREATE TABLE IF NOT EXISTS drones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    speed INTEGER,
    range_km INTEGER,
    endurance_min INTEGER,
    payload_kg REAL,
    ceiling_m INTEGER,
    description TEXT,
    image TEXT,
    price INTEGER,
    featured INTEGER DEFAULT 0,
    stock TEXT DEFAULT 'in_stock',
    rating REAL DEFAULT 0,
    reviews INTEGER DEFAULT 0,
    warranty TEXT,
    shipping TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    icon TEXT
);
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def get_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db():
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with db() as conn:
        conn.executescript(SCHEMA)
    seed()


def seed():
    seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "seed.json")
    if not os.path.exists(seed_path):
        return
    with open(seed_path, encoding="utf-8") as f:
        data = json.load(f)
    with db() as conn:
        for d in data.get("drones", []):
            conn.execute(
                """INSERT OR IGNORE INTO drones
                (slug,name,type,speed,range_km,endurance_min,payload_kg,ceiling_m,description,image,price,featured,stock,rating,reviews,warranty,shipping)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (d["slug"], d["name"], d["type"], d["speed"], d["range_km"],
                 d["endurance_min"], d["payload_kg"], d["ceiling_m"], d["description"], d.get("image"),
                 d.get("price"), 1 if d.get("featured") else 0,
                 d.get("stock", "in_stock"), d.get("rating", 0), d.get("reviews", 0),
                 d.get("warranty"), d.get("shipping")),
            )
        for a in data.get("applications", []):
            conn.execute(
                "INSERT OR IGNORE INTO applications (slug,title,summary,icon) VALUES (?,?,?,?)",
                (a["slug"], a["title"], a["summary"], a["icon"]),
            )
        for n in data.get("news", []):
            conn.execute("INSERT OR IGNORE INTO news (title,body) VALUES (?,?)", (n["title"], n["body"]))


def all_drones():
    with db() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM drones ORDER BY id").fetchall()]


def get_drone(slug):
    with db() as conn:
        r = conn.execute("SELECT * FROM drones WHERE slug=?", (slug,)).fetchone()
        return dict(r) if r else None


def all_applications():
    with db() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM applications ORDER BY id").fetchall()]


def latest_news(limit=5):
    with db() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM news ORDER BY published_at DESC LIMIT ?", (limit,)).fetchall()]


def all_news():
    with db() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM news ORDER BY published_at DESC").fetchall()]


USE_CASES = {
    "фото": ["quad-450"],
    "видео": ["quad-450"],
    "съёмка": ["quad-450"],
    "фотосъёмка": ["quad-450"],
    "видеосъёмка": ["quad-450"],
    "аэрофото": ["quad-450"],
    "доставка": ["hex-900", "heavy-lift"],
    "груз": ["hex-900", "heavy-lift", "hybrid-vt"],
    "логистика": ["hex-900", "heavy-lift"],
    "разведка": ["fw-recon", "strato"],
    "мониторинг": ["fw-recon", "strato"],
    "сельское": ["hex-900"],
    "фермер": ["hex-900"],
    "агро": ["hex-900"],
    "опрыскивание": ["hex-900"],
    "гибрид": ["hybrid-vt"],
    "вертикальн": ["hybrid-vt"],
    "взлёт": ["hybrid-vt"],
    "взлет": ["hybrid-vt"],
    "тяжёл": ["heavy-lift"],
    "тяжел": ["heavy-lift"],
    "грузоподъём": ["heavy-lift"],
    "грузоподъем": ["heavy-lift"],
    "стратосферн": ["strato"],
    "высот": ["strato"],
    "высота": ["strato"],
    "дальност": ["fw-recon"],
    "даль": ["fw-recon"],
}


def search_drones(query):
    q = (query or "").lower()
    if not q:
        return []
    slugs = []
    for key, vals in USE_CASES.items():
        if key in q:
            slugs.extend(vals)
    seen = []
    for s in slugs:
        if s not in seen:
            seen.append(s)
    drones = {d["slug"]: d for d in all_drones()}
    return [drones[s] for s in seen if s in drones]
