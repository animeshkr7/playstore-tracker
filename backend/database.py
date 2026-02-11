import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def insert_app(app_data: dict):
    conn = get_connection()
    cur = conn.cursor()
    today = datetime.now().date().isoformat()
    
    cur.execute("""
        INSERT INTO apps (app_id, title, developer, category, score, installs, icon_url, first_seen, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (app_id) DO UPDATE SET last_updated = %s
    """, (
        app_data.get("appId"),
        app_data.get("title"),
        app_data.get("developer"),
        app_data.get("genre"),
        app_data.get("score"),
        app_data.get("installs"),
        app_data.get("icon"),
        today,
        today,
        today
    ))
    conn.commit()
    cur.close()
    conn.close()

def get_apps_by_month(year: int, month: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM apps 
        WHERE EXTRACT(YEAR FROM first_seen) = %s AND EXTRACT(MONTH FROM first_seen) = %s
        ORDER BY first_seen DESC
    """, (year, month))
    apps = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in apps]

def get_all_months():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT TO_CHAR(first_seen, 'YYYY-MM') as month, COUNT(*) as count
        FROM apps GROUP BY month ORDER BY month DESC
    """)
    months = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in months]

def get_stats():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) as total FROM apps")
    total = cur.fetchone()["total"]
    
    cur.execute("""
        SELECT category, COUNT(*) as count FROM apps 
        GROUP BY category ORDER BY count DESC LIMIT 10
    """)
    by_category = [dict(row) for row in cur.fetchall()]
    
    cur.execute("SELECT MIN(first_seen) as oldest, MAX(first_seen) as newest FROM apps")
    dates = dict(cur.fetchone())
    
    cur.close()
    conn.close()
    return {"total_apps": total, "by_category": by_category, "date_range": dates}