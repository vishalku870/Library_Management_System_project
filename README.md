# 📚 Library Management System  
## Professional BCA Final Year Project

---

# 🚀 Project Overview

A modern and professional web-based **Library Management System** developed using:

- **Backend:** Python + Flask  
- **Database:** SQLite3  
- **Frontend:** HTML5 + CSS3  
- **Templating Engine:** Jinja2  

The system helps librarians manage books, users, issuing records, returns, and fine calculations efficiently through a clean and responsive interface.

---

# 🎯 Objectives

- Digitize library operations
- Maintain accurate book records
- Track issued and returned books
- Automate fine calculation
- Provide role-based access (Admin/User)
- Improve efficiency and user experience

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Flask | Web Framework |
| SQLite3 | Database |
| HTML5 | Structure |
| CSS3 | Styling |
| Jinja2 | Dynamic Templates |

---

# 📁 Project Structure

```plaintext
library_management/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── admin_books.html
│   ├── add_book.html
│   ├── admin_users.html
│   ├── add_user.html
│   ├── issue_book.html
│   ├── admin_issued.html
│   ├── return_book.html
│   └── user_dashboard.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── uploads/
```

---

# 🔐 Authentication System

The system uses a secure login mechanism with role-based access.

## Roles

### 👨‍💼 Admin
Admin has full control over the system.

### 👤 User
Users can only view their issued books and related information.

---

# 🗄️ Database Design

## 📌 Table: users

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary Key |
| name | TEXT | User full name |
| phone | TEXT | Login ID |
| photo | TEXT | User image |
| password | TEXT | User password |
| role | TEXT | admin/user |

---

## 📌 Table: books

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary Key |
| title | TEXT | Book title |
| author | TEXT | Author name |
| price | REAL | Book price |
| quantity | INTEGER | Total copies |
| available | INTEGER | Available copies |

---

## 📌 Table: issued_books

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Linked user |
| book_id | INTEGER | Linked book |
| issue_date | TEXT | Date issued |
| due_date | TEXT | Last return date |
| return_date | TEXT | Actual return |
| fine | REAL | Fine amount |
| status | TEXT | issued/returned |

---

# ✨ Main Features

---

# 👨‍💼 Admin Features

## 🔹 Admin Dashboard
Dashboard provides quick statistics including:

- Total books
- Total users
- Issued books
- Returned books
- Pending returns

---

## 🔹 Book Management

Admin can:

- Add new books
- Delete books
- View all books
- Manage availability

---

## 🔹 User Management

Admin can:

- Create users
- Upload user photos
- Manage user accounts

---

## 🔹 Issue Book System

Admin can issue books to users with:

- Automatic due date generation
- Availability checking
- Issue tracking

---

## 🔹 Return Book System

Admin can:

- Return books
- Calculate late fine automatically
- Update stock availability

---

## 🔹 Issued Records

Admin can monitor:

- Currently issued books
- Returned books
- Fine details
- Issue history

---

# 👤 User Features

Users can:

- Login securely
- View issued books
- Check due dates
- View return status
- Check pending fines

---

# 💰 Professional Fine Calculation System

## Fine Rules

| Condition | Fine |
|---|---|
| Returned within 7 days | ₹0 |
| Returned after due date | ₹2/day |

---

## Fine Calculation Logic

```python
late_days = (return_date - due_date).days

if late_days > 0:
    fine = late_days * 2
else:
    fine = 0
```

---

# 🔥 Professional Enhancements

## ✅ Responsive UI
- Mobile-friendly layout
- Clean dashboard cards
- Modern navigation bar

---

## ✅ Flash Messages
Interactive success/error alerts for:

- Login success
- Book added
- Book issued
- Return completed

---

## ✅ Image Upload System
Users can upload profile photos stored inside:

```plaintext
static/uploads/
```

---

## ✅ Session Management
Flask sessions are used for:

- Login persistence
- Role verification
- Secure logout

---

# 🔒 Recommended Professional Improvements

## ✅ Password Hashing

```python
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
```

### Benefits
- Better security
- Professional development practice

---

## ✅ Search Functionality

Add:

- Search books by title
- Search by author
- Search users

---

## ✅ Pagination

Useful when database records become large.

---

## ✅ Book Cover Images

Add cover image uploads for books.

---

## ✅ Email Notifications

Send reminders for due books.

---

## ✅ Dashboard Charts

Use charts for:

- Issued books
- Monthly activity
- Fine collection

---

## ✅ Export Reports

Generate PDF/Excel reports.

---

# 🎨 Suggested UI Design Improvements

## Modern Color Palette

| Element | Color |
|---|---|
| Primary | #2563eb |
| Background | #f8fafc |
| Success | #16a34a |
| Danger | #dc2626 |

---

## Recommended UI Components

- Sidebar navigation
- Statistic cards
- Table hover effects
- Responsive forms
- Modal confirmations

---

# ⚙️ Installation Guide

## Step 1: Install Python

Download Python from:

https://www.python.org/downloads/

---

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3: Run Project

```bash
python app.py
```

---

## Step 4: Open Browser

```plaintext
http://127.0.0.1:5000
```

---

# 🔑 Default Admin Credentials

| Field | Value |
|---|---|
| Phone | 9999999999 |
| Password | admin123 |

---

# 📈 Future Scope

The project can be upgraded into a complete enterprise-level system by adding:

- Barcode scanning
- QR code integration
- Online book reservation
- Multi-admin support
- Cloud database
- REST APIs
- React frontend
- JWT Authentication

---

# ✅ Conclusion

The Library Management System is a complete and practical web application that demonstrates:

- Database management
- CRUD operations
- Authentication
- File handling
- Session management
- Business logic implementation

This project is highly suitable for:

- BCA Final Year Project
- Portfolio Project
- Internship Demonstration
- Resume Showcase

It reflects strong understanding of full-stack web development using Python Flask and SQLite.

---

# 👨‍💻 Developed By

## Vishal Kumar

📧 Email: vishal2123@gmail.com  

For suggestions, improvements, collaboration, or project-related queries, feel free to reach out anytime.

---
