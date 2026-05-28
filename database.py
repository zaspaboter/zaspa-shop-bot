import sqlite3
from config import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    coins INTEGER DEFAULT 0,
    invited_by INTEGER,
    invited_count INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_name TEXT,
    price INTEGER,
    status TEXT
)
""")

conn.commit()


def add_user(user_id, username, invited_by=None):

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:

        cursor.execute(
            """
            INSERT INTO users(
                user_id,
                username,
                invited_by
            )
            VALUES(?,?,?)
            """,
            (
                user_id,
                username,
                invited_by
            )
        )

        conn.commit()

        if invited_by:

            cursor.execute(
                """
                UPDATE users
                SET coins = coins + 1,
                invited_count = invited_count + 1
                WHERE user_id = ?
                """,
                (invited_by,)
            )

            conn.commit()


def get_user(user_id):

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    return cursor.fetchone()


def get_top_users():

    cursor.execute("""
    SELECT username, invited_count
    FROM users
    ORDER BY invited_count DESC
    LIMIT 10
    """)

    return cursor.fetchall()


def create_order(user_id, item_name, price):

    cursor.execute(
        """
        INSERT INTO orders(
            user_id,
            item_name,
            price,
            status
        )
        VALUES(?,?,?,?)
        """,
        (
            user_id,
            item_name,
            price,
            "pending"
        )
    )

    conn.commit()

    return cursor.lastrowid


def get_order(order_id):

    cursor.execute(
        "SELECT * FROM orders WHERE order_id = ?",
        (order_id,)
    )

    return cursor.fetchone()


def update_order_status(order_id, status):

    cursor.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE order_id = ?
        """,
        (
            status,
            order_id
        )
    )

    conn.commit()


def add_coins(user_id, amount):

    cursor.execute(
        """
        UPDATE users
        SET coins = coins + ?
        WHERE user_id = ?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()


def remove_coins(user_id, amount):

    cursor.execute(
        """
        UPDATE users
        SET coins = coins - ?
        WHERE user_id = ?
        """,
        (
            amount,
            user_id
        )
    )

    conn.commit()
