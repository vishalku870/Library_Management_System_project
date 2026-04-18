"""
Library Management System
BCA Final Year Project
Backend: Flask (Python)
Database: SQLite3
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime, date
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "library_secret_key_2024"  # Secret key for sessions

# Configuration for photo uploads
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Fine rate: Rs. 2 per day after due date (7 days issue period)
FINE_PER_DAY = 2
ISSUE_DAYS = 7  # Default issue period in days


# ─────────────────────────────────────────────
#  DATABASE SETUP
# ─────────────────────────────────────────────

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """Create all tables if they don't exist and insert default admin."""
    conn = get_db()
    cursor = conn.cursor()

    # --- Users Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT    NOT NULL,
            phone    TEXT    NOT NULL UNIQUE,
            photo    TEXT    DEFAULT 'default.png',
            password TEXT    NOT NULL,
            role     TEXT    NOT NULL DEFAULT 'user'
        )
    """)

    # --- Books Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            author    TEXT    NOT NULL,
            price     REAL    NOT NULL,
            quantity  INTEGER NOT NULL,
            available INTEGER NOT NULL
        )
    """)

    # --- Issued Books Table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            book_id     INTEGER NOT NULL,
            issue_date  TEXT    NOT NULL,
            return_date TEXT,
            due_date    TEXT    NOT NULL,
            fine        REAL    DEFAULT 0,
            status      TEXT    DEFAULT 'issued',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    # --- Insert default admin if not exists ---
    cursor.execute("SELECT * FROM users WHERE role = 'admin'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (name, phone, password, role)
            VALUES ('Administrator', '9999999999', 'admin123', 'admin')
        """)

    conn.commit()
    conn.close()


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_fine(due_date_str, return_date_str=None):
    """
    Calculate fine based on delay.
    Fine = FINE_PER_DAY * (days beyond due date)
    """
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    check_date = date.today() if return_date_str is None else datetime.strptime(return_date_str, "%Y-%m-%d").date()
    delay = (check_date - due_date).days
    if delay > 0:
        return delay * FINE_PER_DAY
    return 0


# ─────────────────────────────────────────────
#  HOME / LOGIN ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def home():
    """Redirect to login page."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle login for both admin and users."""
    if request.method == "POST":
        phone    = request.form.get("phone", "").strip()
        password = request.form.get("password", "").strip()

        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = ? AND password = ?", (phone, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            session["role"]      = user["role"]
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        else:
            flash("Invalid phone number or password!", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Clear session and redirect to login."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ─────────────────────────────────────────────
#  ADMIN ROUTES
# ─────────────────────────────────────────────

@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard with summary statistics."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()

    # Total books (sum of all quantities)
    cursor.execute("SELECT SUM(quantity) as total FROM books")
    total_books = cursor.fetchone()["total"] or 0

    # Currently issued books count
    cursor.execute("SELECT COUNT(*) as cnt FROM issued_books WHERE status = 'issued'")
    total_issued = cursor.fetchone()["cnt"]

    # Total registered users (excluding admin)
    cursor.execute("SELECT COUNT(*) as cnt FROM users WHERE role = 'user'")
    total_users = cursor.fetchone()["cnt"]

    # Books with stock info
    cursor.execute("SELECT * FROM books ORDER BY title")
    books = cursor.fetchall()

    conn.close()
    return render_template("admin_dashboard.html",
                           total_books=total_books,
                           total_issued=total_issued,
                           total_users=total_users,
                           books=books)


# ── BOOK MANAGEMENT ──────────────────────────

@app.route("/admin/books")
def admin_books():
    """View all books."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY title")
    books = cursor.fetchall()
    conn.close()
    return render_template("admin_books.html", books=books)


@app.route("/admin/books/add", methods=["GET", "POST"])
def add_book():
    """Add a new book to the library."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        author   = request.form.get("author", "").strip()
        price    = request.form.get("price", 0)
        quantity = request.form.get("quantity", 1)

        if not title or not author:
            flash("Title and Author are required!", "error")
            return render_template("add_book.html")

        try:
            price    = float(price)
            quantity = int(quantity)
        except ValueError:
            flash("Price and Quantity must be valid numbers!", "error")
            return render_template("add_book.html")

        conn   = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, price, quantity, available) VALUES (?, ?, ?, ?, ?)",
            (title, author, price, quantity, quantity)
        )
        conn.commit()
        conn.close()
        flash(f"Book '{title}' added successfully!", "success")
        return redirect(url_for("admin_books"))

    return render_template("add_book.html")


@app.route("/admin/books/delete/<int:book_id>")
def delete_book(book_id):
    """Delete a book (only if no copies are currently issued)."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()

    # Check if the book is currently issued
    cursor.execute("SELECT COUNT(*) as cnt FROM issued_books WHERE book_id = ? AND status = 'issued'", (book_id,))
    if cursor.fetchone()["cnt"] > 0:
        flash("Cannot delete — this book has active issues!", "error")
        conn.close()
        return redirect(url_for("admin_books"))

    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    flash("Book deleted successfully!", "success")
    return redirect(url_for("admin_books"))


# ── USER MANAGEMENT ──────────────────────────

@app.route("/admin/users")
def admin_users():
    """View all registered users."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE role = 'user' ORDER BY name")
    users = cursor.fetchall()
    conn.close()
    return render_template("admin_users.html", users=users)


@app.route("/admin/users/add", methods=["GET", "POST"])
def add_user():
    """Create a new library user."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        phone    = request.form.get("phone", "").strip()
        password = request.form.get("password", "").strip()
        photo    = "default.png"

        # Handle photo upload
        if "photo" in request.files:
            file = request.files["photo"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{phone}_{file.filename}")
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                photo = filename

        if not name or not phone or not password:
            flash("All fields are required!", "error")
            return render_template("add_user.html")

        conn   = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, phone, password, photo, role) VALUES (?, ?, ?, ?, 'user')",
                (name, phone, password, photo)
            )
            conn.commit()
            flash(f"User '{name}' created successfully!", "success")
        except sqlite3.IntegrityError:
            flash("Phone number already registered!", "error")
        finally:
            conn.close()

        return redirect(url_for("admin_users"))

    return render_template("add_user.html")


# ── ISSUE / RETURN BOOKS ─────────────────────

@app.route("/admin/issue", methods=["GET", "POST"])
def issue_book():
    """Issue a book to a user."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        book_id = request.form.get("book_id")

        # Check book availability
        cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        if not book or book["available"] < 1:
            flash("Book is not available!", "error")
            conn.close()
            return redirect(url_for("issue_book"))

        # Check if user already has this book
        cursor.execute(
            "SELECT id FROM issued_books WHERE user_id = ? AND book_id = ? AND status = 'issued'",
            (user_id, book_id)
        )
        if cursor.fetchone():
            flash("This user already has this book issued!", "error")
            conn.close()
            return redirect(url_for("issue_book"))

        today    = date.today().strftime("%Y-%m-%d")
        due_date = date.today().replace(day=date.today().day)  # calculate properly below
        from datetime import timedelta
        due_str  = (date.today() + timedelta(days=ISSUE_DAYS)).strftime("%Y-%m-%d")

        cursor.execute(
            "INSERT INTO issued_books (user_id, book_id, issue_date, due_date, status) VALUES (?, ?, ?, ?, 'issued')",
            (user_id, book_id, today, due_str)
        )
        # Reduce available count
        cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (book_id,))
        conn.commit()
        flash("Book issued successfully!", "success")
        conn.close()
        return redirect(url_for("admin_issued"))

    # GET — load users and available books
    cursor.execute("SELECT id, name, phone FROM users WHERE role = 'user' ORDER BY name")
    users = cursor.fetchall()
    cursor.execute("SELECT id, title, author, available FROM books WHERE available > 0 ORDER BY title")
    books = cursor.fetchall()
    conn.close()
    return render_template("issue_book.html", users=users, books=books)


@app.route("/admin/issued")
def admin_issued():
    """View all currently issued books."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ib.id, u.name AS user_name, u.phone, b.title, b.author,
               ib.issue_date, ib.due_date, ib.return_date, ib.fine, ib.status
        FROM issued_books ib
        JOIN users  u ON ib.user_id = u.id
        JOIN books  b ON ib.book_id = b.id
        ORDER BY ib.issue_date DESC
    """)
    records = cursor.fetchall()
    conn.close()

    # Calculate live fine for still-issued books
    records_with_fine = []
    for r in records:
        row = dict(r)
        if row["status"] == "issued":
            row["live_fine"] = calculate_fine(row["due_date"])
        else:
            row["live_fine"] = row["fine"]
        records_with_fine.append(row)

    return render_template("admin_issued.html", records=records_with_fine)


@app.route("/admin/return/<int:issue_id>", methods=["GET", "POST"])
def return_book(issue_id):
    """Process a book return and calculate fine."""
    if session.get("role") != "admin":
        return redirect(url_for("login"))

    conn   = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ib.*, u.name AS user_name, b.title, b.author
        FROM issued_books ib
        JOIN users u ON ib.user_id = u.id
        JOIN books b ON ib.book_id = b.id
        WHERE ib.id = ?
    """, (issue_id,))
    record = cursor.fetchone()

    if not record:
        flash("Record not found!", "error")
        conn.close()
        return redirect(url_for("admin_issued"))

    if record["status"] == "returned":
        flash("This book has already been returned!", "info")
        conn.close()
        return redirect(url_for("admin_issued"))

    today         = date.today().strftime("%Y-%m-%d")
    issue_date    = datetime.strptime(record["issue_date"], "%Y-%m-%d").date()
    due_date_obj  = datetime.strptime(record["due_date"], "%Y-%m-%d").date()
    return_date   = date.today()
    days_issued   = (return_date - issue_date).days
    fine          = calculate_fine(record["due_date"])

    if request.method == "POST":
        # Mark as returned
        cursor.execute("""
            UPDATE issued_books
            SET return_date = ?, fine = ?, status = 'returned'
            WHERE id = ?
        """, (today, fine, issue_id))
        # Increase available count
        cursor.execute("UPDATE books SET available = available + 1 WHERE id = ?", (record["book_id"],))
        conn.commit()
        conn.close()
        flash(f"Book returned! Fine collected: ₹{fine}", "success")
        return redirect(url_for("admin_issued"))

    conn.close()
    return render_template("return_book.html",
                           record=record,
                           days_issued=days_issued,
                           fine=fine,
                           today=today)


# ─────────────────────────────────────────────
#  USER ROUTES
# ─────────────────────────────────────────────

@app.route("/user/dashboard")
def user_dashboard():
    """User dashboard — shows their issued books."""
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn    = get_db()
    cursor  = conn.cursor()

    cursor.execute("""
        SELECT ib.id, b.title, b.author, ib.issue_date, ib.due_date,
               ib.return_date, ib.fine, ib.status
        FROM issued_books ib
        JOIN books b ON ib.book_id = b.id
        WHERE ib.user_id = ?
        ORDER BY ib.issue_date DESC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()

    records_with_fine = []
    for r in records:
        row = dict(r)
        if row["status"] == "issued":
            row["live_fine"] = calculate_fine(row["due_date"])
        else:
            row["live_fine"] = row["fine"]
        records_with_fine.append(row)

    return render_template("user_dashboard.html", records=records_with_fine)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db()  # Initialize database on first run
    app.run(debug=True)
