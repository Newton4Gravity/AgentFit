import json
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path("agentfit.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS device_profiles (
            device_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS calibration_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            request_data TEXT NOT NULL,
            response_data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback_events (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()


def upsert_user_profile(user_id: str, data: Dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO user_profiles (user_id, data)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            data = excluded.data,
            updated_at = CURRENT_TIMESTAMP
        """, (user_id, json.dumps(data, indent=2)))
        conn.commit()


def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT data FROM user_profiles WHERE user_id = ?",
            (user_id,)
        ).fetchone()

    return json.loads(row["data"]) if row else None


def upsert_device_profile(device_id: str, user_id: str, data: Dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO device_profiles (device_id, user_id, data)
        VALUES (?, ?, ?)
        ON CONFLICT(device_id) DO UPDATE SET
            user_id = excluded.user_id,
            data = excluded.data,
            updated_at = CURRENT_TIMESTAMP
        """, (device_id, user_id, json.dumps(data, indent=2)))
        conn.commit()


def get_device_profile(device_id: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT data FROM device_profiles WHERE device_id = ?",
            (device_id,)
        ).fetchone()

    return json.loads(row["data"]) if row else None


def list_user_devices(user_id: str) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT data FROM device_profiles WHERE user_id = ?",
            (user_id,)
        ).fetchall()

    return [json.loads(row["data"]) for row in rows]


def save_calibration_event(
    user_id: str,
    request_data: Dict[str, Any],
    response_data: Dict[str, Any]
) -> int:
    with get_connection() as conn:
        cursor = conn.execute("""
        INSERT INTO calibration_events (user_id, request_data, response_data)
        VALUES (?, ?, ?)
        """, (
            user_id,
            json.dumps(request_data, indent=2),
            json.dumps(response_data, indent=2),
        ))
        conn.commit()
        return int(cursor.lastrowid)


def save_feedback_event(event_id: str, user_id: str, data: Dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO feedback_events (event_id, user_id, data)
        VALUES (?, ?, ?)
        """, (event_id, user_id, json.dumps(data, indent=2)))
        conn.commit()
