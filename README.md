# Library Management System
**BCA Final Year Project**

---

## Project Description
A complete Library Management System built with:
- **Backend**: Python (Flask)
- **Database**: SQLite3
- **Frontend**: HTML + CSS (no frameworks)

---

## Project Structure
```
library_management/
├── app.py                  ← Main Flask application (all routes & logic)
├── database.db             ← Auto-created SQLite database
├── requirements.txt        ← Python dependencies
│
├── templates/              ← HTML pages (Jinja2 templates)
│   ├── base.html           ← Shared layout (navbar, flash messages)
│   ├── login.html          ← Login page
│   ├── admin_dashboard.html← Admin home with stats
│   ├── admin_books.html    ← View all books
│   ├── add_book.html       ← Add new book form
│   ├── admin_users.html    ← View all users
│   ├── add_user.html       ← Create new user form
│   ├── issue_book.html     ← Issue book to user
│   ├── admin_issued.html   ← All issued books record
│   ├── return_book.html    ← Return book + fine calculation
│   └── user_dashboard.html ← User's personal book list
│
└── static/
    ├── css/
    │   └── style.css       ← Main stylesheet
    └── uploads/            ← User photo uploads (auto-created)
```

---

## Database Tables

### users
| Column   | Type    | Description                   |
|----------|---------|-------------------------------|
| id       | INTEGER | Primary Key (auto)            |
| name     | TEXT    | Full name                     |
| phone    | TEXT    | Phone / Login ID (unique)     |
| photo    | TEXT    | Photo filename                |
| password | TEXT    | Plain text password           |
| role     | TEXT    | 'admin' or 'user'             |

### books
| Column    | Type    | Description            |
|-----------|---------|------------------------|
| id        | INTEGER | Primary Key            |
| title     | TEXT    | Book title             |
| author    | TEXT    | Author name            |
| price     | REAL    | Price in ₹             |
| quantity  | INTEGER | Total copies           |
| available | INTEGER | Currently available    |

### issued_books
| Column      | Type    | Description                |
|-------------|---------|----------------------------|
| id          | INTEGER | Primary Key                |
| user_id     | INTEGER | FK → users.id              |
| book_id     | INTEGER | FK → books.id              |
| issue_date  | TEXT    | Date issued (YYYY-MM-DD)   |
| due_date    | TEXT    | Return deadline            |
| return_date | TEXT    | Actual return date         |
| fine        | REAL    | Fine amount (₹)            |
| status      | TEXT    | 'issued' or 'returned'     |

---

## Setup & Run

### Step 1: Install Python 3 (if not installed)
Download from https://www.python.org/downloads/

### Step 2: Install Flask
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
python app.py
```

### Step 4: Open in browser
```
http://127.0.0.1:5000
```

---

## Default Admin Credentials
| Field    | Value       |
|----------|-------------|
| Phone    | 9999999999  |
| Password | admin123    |

---

## Features
### Admin
- Login / Logout
- Dashboard (stats: total books, issued, users)
- Add / Delete books
- Create users with photo upload
- Issue book to user
- Return book with fine calculation (₹2/day after 7 days)
- View all issued/returned records

### User
- Login / Logout
- View own issued books
- See issue date, due date, return date, fine

---

## Fine Calculation
- Issue period: **7 days**
- Fine: **₹2 per extra day** beyond due date
- Fine is calculated automatically on the return screen
