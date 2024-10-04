import sqlite3

def connect_to_database(file: str) -> sqlite3.Connection:
    """
    Connects to the provided database file and creates the codes table if
    it doesn't exist
    """

    con = sqlite3.connect(file)

    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY,
            code TEXT NOT NULL,
            remaining_uses INT,
            total_uses INT
        )
    """)

    con.commit()
    cur.close()

    return con

def add_code(cur: sqlite3.Cursor, code: str, total_uses: int, remaining_uses: int = -1) -> None:
    """
    Adds a code to the database, reminaing uses is set to total uses if
    left as -1
    """

    if remaining_uses == -1:
        remaining_uses = total_uses

    cur.execute("""
        INSERT INTO codes (code, remaining_uses, total_uses)
        VALUES (?, ?, ?)
    """, (code, remaining_uses, total_uses))

    cur.connection.commit()

def get_codes(cur: sqlite3.Cursor) -> list[tuple]:
    """Returns a list of every code with their remaining and total uses"""

    cur.execute("SELECT code, remaining_uses, total_uses FROM codes")
    return cur.fetchall()

def get_code(cur: sqlite3.Cursor, code: str) -> tuple | None:
    """
    Returns a tuple with the code, remaining uses, and total uses, or None
    if the code does not exist
    """

    cur.execute("""
        SELECT code, remaining_uses, total_uses FROM codes
        WHERE code = ?
    """, (code,))

    return cur.fetchone()

def delete_code(cur: sqlite3.Cursor, code: str) -> None:
    """Deletes a code from the database"""

    cur.execute("DELETE FROM codes WHERE code = ?", (code,))
    cur.connection.commit()

def update_code(cur: sqlite3.Cursor, code: str, change: int) -> tuple:
    """
    Adds the given change onto the remaining uses of code and returns the
    updated code tuple
    """

    _, remaining_uses, _ = get_code(cur, code)
    updated_uses = remaining_uses + change

    cur.execute("UPDATE codes SET remaining_uses = ? WHERE code = ?",
                (updated_uses, code))

    cur.connection.commit()

    return get_code(cur, code)

def set_code(cur: sqlite3.Cursor, code: str, new_value: int) -> tuple:
    """
    Sets the code remaining uses to the given new value, increases the
    total uses if new value is greater, and returns the updated code tuple
    """

    _, _, total_uses = get_code(cur, code)

    cur.execute("UPDATE codes SET remaining_uses = ? WHERE code = ?",
                (new_value, code))

    if new_value > total_uses:
        cur.execute("UPDATE codes SET total_uses = ? WHERE code = ?",
                    (new_value, code))

    cur.connection.commit()

    return get_code(cur, code)

def format_code(code: tuple) -> str:
    """Returns a formmated, human-friendly code tuple"""

    return f"{code[0]}, ({code[1]}/{code[2]} uses left)"

def formatted_get_codes(cur: sqlite3.Cursor) -> str:
    """Returns a formmated string list of all codes"""

    return "\n".join(format_code(code) for code in get_codes(cur))

def formatted_get_code(cur: sqlite3.Cursor, code: str) -> str:
    """Returns a formmated code tuple"""

    return format_code(get_code(cur, code))

if __name__ == "__main__":
    con = connect_to_database("codes-database.db")
    cur = con.cursor()

    add_code(cur, "test-code", 3)
    add_code(cur, "last-code", 5, 1)
    add_code(cur, "expired-code", 0)

    set_code(cur, "test-code", 5)

    user = input("Code: ")

    code_tuple = get_code(cur, user)

    if code_tuple is None:
        print("Sorry, this is not a valid code")

    elif code_tuple[1] <= 0:
        print("Sorry, this code is expired")

    else:
        update_code(cur, user, -1)
        print(f"You're in! Used the code: {formatted_get_code(cur, user)}")
        print(formatted_get_codes(cur))

    for code, _, _ in get_codes(cur):
        delete_code(cur, code)
