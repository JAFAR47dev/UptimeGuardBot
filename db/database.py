
#db/database.py
import sqlite3
import os
from config import DB_PATH

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            username    TEXT,
            plan        TEXT DEFAULT 'free',
            trial_expires TEXT,
            activated_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS monitors (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id               INTEGER NOT NULL,
            url                   TEXT NOT NULL,
            label                 TEXT,
            interval_minutes      INTEGER DEFAULT 5,
            active                INTEGER DEFAULT 1,
            last_status           TEXT DEFAULT 'unknown',
            last_checked          TEXT,
            response_threshold_ms INTEGER DEFAULT NULL,
            created_at            TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS incidents (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            monitor_id  INTEGER NOT NULL,
            status_code INTEGER,
            response_ms INTEGER,
            is_up       INTEGER,
            error_msg   TEXT,
            checked_at  TEXT DEFAULT (datetime('now')),
            resolved_at TEXT,
            FOREIGN KEY (monitor_id) REFERENCES monitors(id)
        );
    """)

    # Safe migrations for existing deployments
    migrations = [
        "ALTER TABLE monitors ADD COLUMN response_threshold_ms INTEGER DEFAULT NULL",
    ]
    for sql in migrations:
        try:
            c.execute(sql)
            conn.commit()
        except Exception:
            pass  # Column already exists — safe to skip

    conn.close()
    
# --- User helpers ---
def get_or_create_user(user_id: int, username: str = None):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    if not user:
        from datetime import datetime, timedelta
        trial_expires = (datetime.now() + timedelta(days=7)).isoformat()
        c.execute(
            "INSERT INTO users (user_id, username, plan, trial_expires) VALUES (?,?,?,?)",
            (user_id, username, 'trial', trial_expires)
        )
        conn.commit()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = c.fetchone()
    conn.close()
    return user

def get_user(user_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def upgrade_user(user_id: int, plan: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET plan = ? WHERE user_id = ?", (plan, user_id))
    conn.commit()
    conn.close()

def is_pro(user_id: int) -> bool:
    from datetime import datetime
    user = get_user(user_id)
    if not user:
        return False
    if user["plan"] == "pro":
        return True
    if user["plan"] == "trial":
        if user["trial_expires"] and datetime.now().isoformat() < user["trial_expires"]:
            return True
    return False

# --- Monitor helpers ---
def add_monitor(user_id: int, url: str, label: str, interval: int = 5) -> int:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO monitors (user_id, url, label, interval_minutes) VALUES (?,?,?,?)",
        (user_id, url, label, interval)
    )
    monitor_id = c.lastrowid
    conn.commit()
    conn.close()
    return monitor_id

def get_monitors(user_id: int) -> list:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM monitors WHERE user_id = ? AND active = 1", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_monitor(monitor_id: int) -> dict:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM monitors WHERE id = ?", (monitor_id,))
    row = c.fetchone()
    conn.close()
    return row

def count_monitors(user_id: int) -> int:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM monitors WHERE user_id = ? AND active = 1", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def delete_monitor(monitor_id: int, user_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE monitors SET active = 0 WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()

def update_monitor_status(monitor_id: int, status: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE monitors SET last_status = ?, last_checked = datetime('now') WHERE id = ?",
        (status, monitor_id)
    )
    conn.commit()
    conn.close()

# --- Incident helpers ---
def log_incident(monitor_id: int, status_code, response_ms, is_up: bool, error_msg=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO incidents (monitor_id, status_code, response_ms, is_up, error_msg)
           VALUES (?,?,?,?,?)""",
        (monitor_id, status_code, response_ms, int(is_up), error_msg)
    )
    conn.commit()
    conn.close()

def get_last_incident(monitor_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM incidents WHERE monitor_id = ? ORDER BY checked_at DESC LIMIT 1",
        (monitor_id,)
    )
    row = c.fetchone()
    conn.close()
    return row

def get_uptime_percent(monitor_id: int, days: int = 7) -> float:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """SELECT COUNT(*) as total,
           SUM(CASE WHEN is_up = 1 THEN 1 ELSE 0 END) as up_count
           FROM incidents
           WHERE monitor_id = ?
           AND checked_at >= datetime('now', ?)""",
        (monitor_id, f'-{days} days')
    )
    row = c.fetchone()
    conn.close()
    if not row or not row["total"]:
        return 100.0
    return round((row["up_count"] / row["total"]) * 100, 2)

def get_expired_trials() -> list:
    """Return all users whose trial has expired but plan is still 'trial'."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """SELECT * FROM users
           WHERE plan = 'trial'
           AND trial_expires < datetime('now')"""
    )
    rows = c.fetchall()
    conn.close()
    return rows

def downgrade_user(user_id: int):
    """Set user back to free plan."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE users SET plan = 'free' WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()
    
def url_exists(user_id: int, url: str) -> bool:
    """Check if user already has an active monitor for this URL."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """SELECT COUNT(*) FROM monitors
           WHERE user_id = ? AND url = ? AND active = 1""",
        (user_id, url)
    )
    count = c.fetchone()[0]
    conn.close()
    return count > 0
    
def get_all_active_users() -> list:
    """Return all users who have at least one active monitor."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """SELECT DISTINCT u.* FROM users u
           INNER JOIN monitors m ON m.user_id = u.user_id
           WHERE m.active = 1"""
    )
    rows = c.fetchall()
    conn.close()
    return rows

def get_weekly_stats(monitor_id: int) -> dict:
    """Return uptime %, avg response ms, and incident count for last 7 days."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """SELECT
               COUNT(*) as total,
               SUM(CASE WHEN is_up = 1 THEN 1 ELSE 0 END) as up_count,
               AVG(CASE WHEN is_up = 1 THEN response_ms END) as avg_ms,
               SUM(CASE WHEN is_up = 0 THEN 1 ELSE 0 END) as down_count
           FROM incidents
           WHERE monitor_id = ?
           AND checked_at >= datetime('now', '-7 days')""",
        (monitor_id,)
    )
    row = c.fetchone()
    conn.close()

    if not row or not row["total"]:
        return {
            "uptime_pct": 100.0,
            "avg_ms": None,
            "down_count": 0,
            "total_checks": 0
        }

    uptime_pct = round((row["up_count"] / row["total"]) * 100, 2)
    avg_ms     = round(row["avg_ms"]) if row["avg_ms"] else None
    return {
        "uptime_pct": uptime_pct,
        "avg_ms": avg_ms,
        "down_count": row["down_count"] or 0,
        "total_checks": row["total"]
    }
    
def pause_monitor(monitor_id: int, user_id: int):
    """Pause a monitor without deleting it or its history."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """UPDATE monitors SET active = 2
           WHERE id = ? AND user_id = ?""",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()

def resume_monitor(monitor_id: int, user_id: int):
    """Resume a paused monitor."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """UPDATE monitors SET active = 1
           WHERE id = ? AND user_id = ?""",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()

def get_all_monitors(user_id: int) -> list:
    """Return active (1) and paused (2) monitors — excludes deleted (0)."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """SELECT * FROM monitors
           WHERE user_id = ? AND active IN (1, 2)""",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def set_response_threshold(monitor_id: int, user_id: int, threshold_ms: int):
    """Set slowness alert threshold in ms for a monitor."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """UPDATE monitors SET response_threshold_ms = ?
           WHERE id = ? AND user_id = ?""",
        (threshold_ms, monitor_id, user_id)
    )
    conn.commit()
    conn.close()

def clear_response_threshold(monitor_id: int, user_id: int):
    """Remove slowness threshold from a monitor."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """UPDATE monitors SET response_threshold_ms = NULL
           WHERE id = ? AND user_id = ?""",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()
    