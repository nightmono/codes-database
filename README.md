# Code Database

Database system that stores [pass]codes with a limited amount of uses, made using Python and SQLite.

Test the system with codes: `test-code`, `last-code`, and `expired-code`.

Expired codes are codes with <1 uses. They are not deleted upon expiration.

## TODO

- [ ] Code metadata
- [ ] Unlimited use codes (could set uses to a very big number)
- [ ] Time expiration

## Docs

> [!WARNING]
> No functions have any validation and may error if provided code does not exist.

---

Code tuple: `(code, remaining uses, total uses)`

---

```py
def connect_to_database(file: str) -> sqlite3.Connection
```

Connects to the provided database file and creates the codes table if it doesn't exist.

Codes table structure:

```sql
id INTEGER PRIMARY KEY,
code TEXT NOT NULL,
remaining_uses INT,
total_uses INT
```

Database file should a SQLite database.

---

```py
def add_code(cur: sqlite3.Cursor, code: str, total_uses: int, remaining_uses: int = -1) -> None
```

Adds a code to the database, reminaing uses is set to total uses if left as -1.

---

```py
def get_codes(cur: sqlite3.Cursor) -> list[tuple]
```

Returns a list of every code with their remaining and total uses `(code, remaining uses, total uses)`.

---

```py
def get_code(cur: sqlite3.Cursor, code: str) -> tuple | None
```

Returns a tuple with the code, remaining uses, and total uses, or None if the code does not exist.

---

```py
def delete_code(cur: sqlite3.Cursor, code: str) -> None
```

Deletes a code from the database.

---

```py
def update_code(cur: sqlite3.Cursor, code: str, change: int) -> tuple
```

Adds the given change onto the remaining uses of code and returns the updated code tuple.

---

```py
def set_code(cur: sqlite3.Cursor, code: str, new_value: int) -> tuple
```

Sets the code remaining uses to the given new value, increases the total uses if new value is greater, and returns the updated code tuple.

---

```py
def format_code(code: tuple) -> str
```

Returns a formmated, human-friendly code tuple.

Example: `test-code (4/5 uses left)`

---

```py
def formatted_get_codes(cur: sqlite3.Cursor) -> str
```

Returns a formmated string list of all codes.

Example:

```
test-code (4/5 uses left)
last-code (1/5 uses left)
expired-code (0/0 uses left)
```

---

```py
def formatted_get_code(cur: sqlite3.Cursor, code: str) -> str
```

Returns a formmated code tuple.

Calls `get_code` and passes the return value into `format_code` so it has the same string format.

> [!WARNING]
> Errors if code does not exist.



