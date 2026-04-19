# db/database.py
import sqlite3
import secrets
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
            user_id        INTEGER PRIMARY KEY,
            username       TEXT,
            plan           TEXT DEFAULT 'free',
            trial_expires  TEXT,
            bonus_monitors INTEGER DEFAULT 0,
            activated_at   TEXT DEFAULT (datetime('now'))
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
            note                  TEXT DEFAULT NULL,
            webhook_url           TEXT DEFAULT NULL,
            keyword               TEXT DEFAULT NULL,
            keyword_case_sensitive INTEGER DEFAULT 0,
            confirm_count         INTEGER DEFAULT 1,
            consecutive_failures  INTEGER DEFAULT 0,
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

        CREATE TABLE IF NOT EXISTS status_pages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL UNIQUE,
            slug       TEXT NOT NULL UNIQUE,
            title      TEXT,
            active     INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS maintenance_windows (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            label        TEXT NOT NULL,
            start_time   TEXT NOT NULL,
            end_time     TEXT NOT NULL,
            days_of_week TEXT,
            active_until TEXT,
            created_at   TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS team_members (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id       INTEGER NOT NULL,
            member_user_id INTEGER NOT NULL,
            label          TEXT,
            created_at     TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (owner_id) REFERENCES users(user_id),
            UNIQUE (owner_id, member_user_id)
        );

        CREATE TABLE IF NOT EXISTS referrals (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id  INTEGER NOT NULL,
            referred_id  INTEGER NOT NULL UNIQUE,
            qualified    INTEGER DEFAULT 0,
            rewarded     INTEGER DEFAULT 0,
            created_at   TEXT DEFAULT (datetime('now'))
        );
    """)

    # Safe migrations — never remove, always append
    migrations = [
        "ALTER TABLE monitors ADD COLUMN response_threshold_ms INTEGER DEFAULT NULL",
        "ALTER TABLE monitors ADD COLUMN note TEXT DEFAULT NULL",
        "ALTER TABLE monitors ADD COLUMN webhook_url TEXT DEFAULT NULL",
        "ALTER TABLE monitors ADD COLUMN keyword TEXT DEFAULT NULL",
        "ALTER TABLE monitors ADD COLUMN keyword_case_sensitive INTEGER DEFAULT 0",
        "ALTER TABLE monitors ADD COLUMN confirm_count INTEGER DEFAULT 1",
        "ALTER TABLE monitors ADD COLUMN consecutive_failures INTEGER DEFAULT 0",
        "ALTER TABLE status_pages ADD COLUMN title TEXT",
        "ALTER TABLE users ADD COLUMN bonus_monitors INTEGER DEFAULT 0",
        "ALTER TABLE referrals ADD COLUMN rewarded INTEGER DEFAULT 0",
    ]
    for sql in migrations:
        try:
            c.execute(sql)
            conn.commit()
        except Exception:
            pass

    conn.close()


# ---------------------------------------------------------------------------
# User helpers
# ---------------------------------------------------------------------------
def get_or_create_user(user_id: int, username: str = None) -> tuple:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    if not user:
        from datetime import datetime, timedelta
        trial_expires = (datetime.now() + timedelta(days=7)).isoformat()
        c.execute(
            """INSERT INTO users (user_id, username, plan, trial_expires, bonus_monitors)
               VALUES (?,?,?,?,?)""",
            (user_id, username, 'trial', trial_expires, 0)
        )
        conn.commit()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user   = c.fetchone()
        is_new = True
    else:
        is_new = False
    conn.close()
    return dict(user) if user else None, is_new   # ← dict()


def get_user(user_id: int) -> dict | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None   # ← dict()


def upgrade_user(user_id: int, plan: str):
    conn = get_conn()
    c    = conn.cursor()
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


def get_monitor_limit(user_id: int) -> int:
    """
    Effective free monitor limit for a user, including any referral bonus slots.
    Pro users have no limit (returns a large sentinel).
    """
    from config import FREE_LIMIT
    if is_pro(user_id):
        return 999_999
    user  = get_user(user_id)
    bonus = (user["bonus_monitors"] or 0) if user else 0
    return FREE_LIMIT + bonus


# ---------------------------------------------------------------------------
# Monitor helpers
# ---------------------------------------------------------------------------

def add_monitor(user_id: int, url: str, label: str, interval: int = 5) -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "INSERT INTO monitors (user_id, url, label, interval_minutes) VALUES (?,?,?,?)",
        (user_id, url, label, interval)
    )
    monitor_id = c.lastrowid
    conn.commit()
    conn.close()
    return monitor_id


def get_monitors(user_id: int) -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM monitors WHERE user_id = ? AND active = 1", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()


def get_monitor(monitor_id: int) -> dict | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM monitors WHERE id = ?", (monitor_id,))
    row  = c.fetchone()
    conn.close()
    return dict(row) if row else None   # ← dict()



def count_monitors(user_id: int) -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM monitors WHERE user_id = ? AND active = 1",
        (user_id,)
    )
    count = c.fetchone()[0]
    conn.close()
    return count


def delete_monitor(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET active = 0 WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def update_monitor_status(monitor_id: int, status: str):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET last_status = ?, last_checked = datetime('now') WHERE id = ?",
        (status, monitor_id)
    )
    conn.commit()
    conn.close()


def url_exists(user_id: int, url: str) -> bool:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM monitors WHERE user_id = ? AND url = ? AND active = 1",
        (user_id, url)
    )
    count = c.fetchone()[0]
    conn.close()
    return count > 0


def get_all_monitors(user_id: int) -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM monitors WHERE user_id = ? AND active IN (1, 2)",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()


def pause_monitor(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET active = 2 WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def resume_monitor(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET active = 1 WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def set_response_threshold(monitor_id: int, user_id: int, threshold_ms: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET response_threshold_ms = ? WHERE id = ? AND user_id = ?",
        (threshold_ms, monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def clear_response_threshold(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET response_threshold_ms = NULL WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Monitor note helpers
# ---------------------------------------------------------------------------

def set_monitor_note(monitor_id: int, user_id: int, note: str):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET note = ? WHERE id = ? AND user_id = ?",
        (note.strip(), monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def clear_monitor_note(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET note = NULL WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Webhook helpers
# ---------------------------------------------------------------------------

def set_webhook_url(monitor_id: int, user_id: int, webhook_url: str):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET webhook_url = ? WHERE id = ? AND user_id = ?",
        (webhook_url.strip(), monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def clear_webhook_url(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET webhook_url = NULL WHERE id = ? AND user_id = ?",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Keyword helpers
# ---------------------------------------------------------------------------

def set_keyword(monitor_id: int, user_id: int, keyword: str, case_sensitive: bool = False):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        """UPDATE monitors SET keyword = ?, keyword_case_sensitive = ?
           WHERE id = ? AND user_id = ?""",
        (keyword.strip(), int(case_sensitive), monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def clear_keyword(monitor_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        """UPDATE monitors SET keyword = NULL, keyword_case_sensitive = 0
           WHERE id = ? AND user_id = ?""",
        (monitor_id, user_id)
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Confirmation count helpers
# ---------------------------------------------------------------------------

FREE_CONFIRM_LIMIT = 2
PRO_CONFIRM_LIMIT  = 5


def set_confirm_count(monitor_id: int, user_id: int, count: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET confirm_count = ? WHERE id = ? AND user_id = ?",
        (count, monitor_id, user_id)
    )
    conn.commit()
    conn.close()


def increment_failure_counter(monitor_id: int) -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET consecutive_failures = consecutive_failures + 1 WHERE id = ?",
        (monitor_id,)
    )
    conn.commit()
    c.execute("SELECT consecutive_failures FROM monitors WHERE id = ?", (monitor_id,))
    row = c.fetchone()
    conn.close()
    return row["consecutive_failures"] if row else 1


def reset_failure_counter(monitor_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE monitors SET consecutive_failures = 0 WHERE id = ?",
        (monitor_id,)
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Team member helpers
# ---------------------------------------------------------------------------

PRO_TEAM_LIMIT = 5


def add_team_member(owner_id: int, member_user_id: int, label: str = None) -> bool:
    if count_team_members(owner_id) >= PRO_TEAM_LIMIT:
        raise ValueError(f"Team limit of {PRO_TEAM_LIMIT} reached.")
    conn = get_conn()
    c    = conn.cursor()
    try:
        c.execute(
            "INSERT INTO team_members (owner_id, member_user_id, label) VALUES (?, ?, ?)",
            (owner_id, member_user_id, label)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False

def get_team_members(owner_id: int) -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM team_members WHERE owner_id = ? ORDER BY created_at",
        (owner_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()


def count_team_members(owner_id: int) -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT COUNT(*) FROM team_members WHERE owner_id = ?", (owner_id,))
    count = c.fetchone()[0]
    conn.close()
    return count


def remove_team_member(row_id: int, owner_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "DELETE FROM team_members WHERE id = ? AND owner_id = ?",
        (row_id, owner_id)
    )
    conn.commit()
    conn.close()


def get_alert_recipients(owner_id: int) -> list:
    members = get_team_members(owner_id)
    return [owner_id] + [m["member_user_id"] for m in members]


# ---------------------------------------------------------------------------
# Referral helpers
# ---------------------------------------------------------------------------

def record_referral(referrer_id: int, new_user_id: int):
    """Record that new_user_id signed up via referrer_id's link."""
    conn = get_conn()
    c    = conn.cursor()
    try:
        c.execute(
            """INSERT OR IGNORE INTO referrals (referrer_id, referred_id)
               VALUES (?, ?)""",
            (referrer_id, new_user_id)
        )
        conn.commit()
    except Exception:
        pass
    conn.close()


def get_referral_count(user_id: int) -> int:
    """Return number of qualified referrals (referred user has added ≥1 monitor)."""
    conn = get_conn()
    c    = conn.cursor()
    try:
        c.execute(
            """SELECT COUNT(*) FROM referrals r
               INNER JOIN monitors m ON m.user_id = r.referred_id
               WHERE r.referrer_id = ? AND m.active IN (1, 2)""",
            (user_id,)
        )
        count = c.fetchone()[0]
    except Exception:
        count = 0
    conn.close()
    return count

def mark_referral_qualified(referred_id: int) -> int | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT referrer_id FROM referrals WHERE referred_id = ? AND qualified = 0",
        (referred_id,)
    )
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    referrer_id = row["referrer_id"]   # sqlite3.Row bracket access is fine here
    c.execute(
        "UPDATE referrals SET qualified = 1 WHERE referred_id = ?",
        (referred_id,)
    )
    conn.commit()
    conn.close()
    return referrer_id


def get_qualified_referral_count(referrer_id: int) -> int:
    """Number of referrals that have been marked qualified."""
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND qualified = 1",
        (referrer_id,)
    )
    count = c.fetchone()[0]
    conn.close()
    return count

def check_and_apply_referral_reward(referrer_id: int) -> dict | None:
    from config import REFERRAL_GOAL, REFERRAL_BONUS_SLOTS, REFERRAL_TRIAL_DAYS
    from datetime import datetime, timedelta

    conn = get_conn()
    c    = conn.cursor()

    c.execute(
        """SELECT COUNT(*) FROM referrals
           WHERE referrer_id = ? AND qualified = 1 AND rewarded = 0""",
        (referrer_id,)
    )
    unrewarded = c.fetchone()[0]

    if unrewarded < REFERRAL_GOAL:
        conn.close()
        return None

    c.execute(
        """UPDATE referrals SET rewarded = 1
           WHERE referrer_id = ? AND qualified = 1 AND rewarded = 0
           AND id IN (
               SELECT id FROM referrals
               WHERE referrer_id = ? AND qualified = 1 AND rewarded = 0
               ORDER BY created_at ASC
               LIMIT ?
           )""",
        (referrer_id, referrer_id, REFERRAL_GOAL)
    )
    conn.commit()

    c.execute("SELECT * FROM users WHERE user_id = ?", (referrer_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        return None

    user = dict(user)   # ← dict() before accessing fields

    reward_type = None
    if user["plan"] == "free":
        conn2 = get_conn()
        c2    = conn2.cursor()
        c2.execute(
            "UPDATE users SET bonus_monitors = bonus_monitors + ? WHERE user_id = ?",
            (REFERRAL_BONUS_SLOTS, referrer_id)
        )
        conn2.commit()
        conn2.close()
        reward_type = "slots"
    else:
        conn2 = get_conn()
        c2    = conn2.cursor()
        c2.execute(
            "SELECT trial_expires FROM users WHERE user_id = ?",
            (referrer_id,)
        )
        row     = c2.fetchone()
        current = row["trial_expires"] if row and row["trial_expires"] else None
        base    = datetime.fromisoformat(current) if current else datetime.now()
        if base < datetime.now():
            base = datetime.now()
        new_expiry = (base + timedelta(days=REFERRAL_TRIAL_DAYS)).isoformat()
        c2.execute(
            "UPDATE users SET trial_expires = ? WHERE user_id = ?",
            (new_expiry, referrer_id)
        )
        conn2.commit()
        conn2.close()
        reward_type = "trial"

    return {
        "type":        reward_type,
        "bonus_slots": REFERRAL_BONUS_SLOTS if reward_type == "slots" else 0,
        "trial_days":  REFERRAL_TRIAL_DAYS  if reward_type == "trial" else 0,
    }
    

# ---------------------------------------------------------------------------
# Incident helpers
# ---------------------------------------------------------------------------

def log_incident(monitor_id: int, status_code, response_ms, is_up: bool, error_msg=None):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        """INSERT INTO incidents (monitor_id, status_code, response_ms, is_up, error_msg)
           VALUES (?,?,?,?,?)""",
        (monitor_id, status_code, response_ms, int(is_up), error_msg)
    )
    conn.commit()
    conn.close()


def get_last_incident(monitor_id: int) -> dict | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM incidents WHERE monitor_id = ? ORDER BY checked_at DESC LIMIT 1",
        (monitor_id,)
    )
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None   # ← dict()


def get_uptime_percent(monitor_id: int, days: int = 7) -> float:
    conn = get_conn()
    c    = conn.cursor()
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


def get_incident_rows(monitor_id: int, days: int) -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        """SELECT is_up, error_msg, status_code, checked_at
           FROM incidents
           WHERE monitor_id = ?
             AND checked_at >= datetime('now', ?)
           ORDER BY checked_at ASC""",
        (monitor_id, f"-{days} days")
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()


def get_expired_trials() -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE plan = 'trial' AND trial_expires < datetime('now')"
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()



def downgrade_user(user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute("UPDATE users SET plan = 'free' WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_all_active_users() -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        """SELECT DISTINCT u.* FROM users u
           INNER JOIN monitors m ON m.user_id = u.user_id
           WHERE m.active = 1"""
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()



def get_weekly_stats(monitor_id: int) -> dict:
    conn = get_conn()
    c    = conn.cursor()
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
        return {"uptime_pct": 100.0, "avg_ms": None, "down_count": 0, "total_checks": 0}

    uptime_pct = round((row["up_count"] / row["total"]) * 100, 2)
    avg_ms     = round(row["avg_ms"]) if row["avg_ms"] else None
    return {
        "uptime_pct":   uptime_pct,
        "avg_ms":       avg_ms,
        "down_count":   row["down_count"] or 0,
        "total_checks": row["total"],
    }


# ---------------------------------------------------------------------------
# Status page helpers
# ---------------------------------------------------------------------------

def create_status_page(user_id: int, title: str = None) -> str:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM status_pages WHERE user_id = ?", (user_id,))
    existing = c.fetchone()

    if existing:
        existing = dict(existing)   # ← dict() before accessing .get()
        if existing["active"] == 1:
            conn.close()
            return existing["slug"]
        c.execute(
            "UPDATE status_pages SET active = 1, title = ? WHERE user_id = ?",
            (title or existing["title"], user_id)
        )
        conn.commit()
        slug = existing["slug"]
        conn.close()
        return slug

    slug = secrets.token_urlsafe(8)
    c.execute(
        "INSERT INTO status_pages (user_id, slug, title) VALUES (?,?,?)",
        (user_id, slug, title)
    )
    conn.commit()
    conn.close()
    return slug


def get_status_page_by_slug(slug: str) -> dict | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM status_pages WHERE slug = ? AND active = 1", (slug,))
    row  = c.fetchone()
    conn.close()
    return dict(row) if row else None   # ← dict()


def get_status_page_by_user(user_id: int) -> dict | None:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT * FROM status_pages WHERE user_id = ? AND active = 1", (user_id,))
    row  = c.fetchone()
    conn.close()
    return dict(row) if row else None   # ← dict()



def delete_status_page(user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute("UPDATE status_pages SET active = 0 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def update_status_page_title(user_id: int, title: str):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "UPDATE status_pages SET title = ? WHERE user_id = ? AND active = 1",
        (title, user_id)
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Maintenance window helpers
# ---------------------------------------------------------------------------

FREE_MAINTENANCE_LIMIT = 1


def add_maintenance_window(
    user_id: int, label: str, start_time: str, end_time: str,
    days_of_week: str = None, active_until: str = None,
) -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        """INSERT INTO maintenance_windows
               (user_id, label, start_time, end_time, days_of_week, active_until)
           VALUES (?,?,?,?,?,?)""",
        (user_id, label, start_time, end_time, days_of_week, active_until)
    )
    win_id = c.lastrowid
    conn.commit()
    conn.close()
    return win_id

def get_maintenance_windows(user_id: int) -> list[dict]:
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "SELECT * FROM maintenance_windows WHERE user_id = ? ORDER BY created_at",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]   # ← dict()


def count_maintenance_windows(user_id: int) -> int:
    conn = get_conn()
    c    = conn.cursor()
    c.execute("SELECT COUNT(*) FROM maintenance_windows WHERE user_id = ?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count


def delete_maintenance_window(win_id: int, user_id: int):
    conn = get_conn()
    c    = conn.cursor()
    c.execute(
        "DELETE FROM maintenance_windows WHERE id = ? AND user_id = ?",
        (win_id, user_id)
    )
    conn.commit()
    conn.close()


def is_in_maintenance(user_id: int) -> bool:
    from datetime import datetime
    now      = datetime.now()
    now_time = now.strftime("%H:%M")
    today_wd = now.weekday()
    today    = now.date().isoformat()
    windows  = get_maintenance_windows(user_id)

    for w in windows:
        start   = w["start_time"]
        end     = w["end_time"]
        in_band = (start <= now_time < end) if start <= end else (now_time >= start or now_time < end)
        if not in_band:
            continue
        if w["days_of_week"]:
            if today_wd in [int(d) for d in w["days_of_week"].split(",")]:
                return True
            continue
        if w["active_until"] and today <= w["active_until"]:
            return True
    return False
