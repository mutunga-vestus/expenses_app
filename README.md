# Expenses App

A full-stack personal finance web application built with **Django**. Track expenses and income, set your preferred currency, view statistics, and export your data to CSV, Excel, or PDF.

---

## Features

- **User authentication**
  - Registration with email verification
  - Login / logout
  - Password reset via email
  - Username & email validation (AJAX)

- **Expense management**
  - Add, edit, and delete expenses
  - Categorize expenses
  - Search expenses
  - Paginated expense list
  - Category summary & statistics charts

- **Income management**
  - Add, edit, and delete income records
  - Source-based tracking
  - Search income
  - Income summary & statistics

- **User preferences**
  - Choose preferred currency (from a large list of world currencies)

- **Data export**
  - Export expenses and income as **CSV**, **Excel**, or **PDF**

- **Docker support**
  - Ready-to-run with Docker Compose (PostgreSQL + Gunicorn)

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Django 6.0                          |
| Database     | PostgreSQL                          |
| Frontend     | Bootstrap, vanilla JavaScript       |
| Auth / Email | Django auth + SMTP (Gmail-ready)    |
| Exports      | `openpyxl`, `reportlab`, CSV        |
| Deployment   | Docker, Gunicorn, WhiteNoise        |

---

## Project Structure

```
expensesapp/
├── authentication/     # Login, register, password reset, email activation
├── expenses/           # Expense models, views, URLs
├── userincome/         # Income models, views, URLs
├── userpreferences/    # Currency preference
├── expensesapp/        # Project settings, main URLs, WSGI/ASGI
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── currencies.json     # List of supported currencies
├── docker-compose.yml
├── dockerfile
├── manage.py
├── requirements.txt
└── .env.example
```

---

## Prerequisites

- Python 3.12+
- PostgreSQL 16 (or use Docker)
- Git

---

## Quick Start (Local Development)

### 1. Clone / extract the project

```bash
cd expensesapp
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and edit it:

```bash
cp .env.example .env
```

Example `.env`:

```env
DB_NAME=expensesdb
DB_USER=postgres
DB_PASSWORD=changeme
DB_HOST=localhost

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

> **Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) (not your regular account password).

### 5. Create the PostgreSQL database

```sql
CREATE DATABASE expensesdb;
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Running with Docker

The project includes a complete Docker setup (PostgreSQL + web app).

### 1. Configure environment

```bash
cp .env.example .env
# Edit DB_PASSWORD and email settings if desired
```

### 2. Build and start

```bash
docker compose up --build
```

- Web app: [http://localhost:8000](http://localhost:8000)
- PostgreSQL: `localhost:5432`

Migrations run automatically on container start.

### Useful Docker commands

```bash
# Stop services
docker compose down

# View logs
docker compose logs -f web

# Create a superuser inside the container
docker compose exec web python manage.py createsuperuser
```

---

## Main Routes

| Path                         | Description                    |
|------------------------------|--------------------------------|
| `/`                          | Expenses dashboard             |
| `/add_expense`               | Add a new expense              |
| `/stats`                     | Expense statistics             |
| `/income/`                   | Income dashboard               |
| `/income/add_income`         | Add a new income               |
| `/income/statitics`          | Income statistics              |
| `/preferences/`              | Currency preference            |
| `/authentication/login/`     | Login                          |
| `/authentication/register/`  | Register                       |
| `/authentication/logout/`    | Logout                         |
| `/admin/`                    | Django admin                   |

---

## Environment Variables

| Variable             | Description                          | Default / Example          |
|----------------------|--------------------------------------|----------------------------|
| `DB_NAME`            | PostgreSQL database name             | `expensesdb`               |
| `DB_USER`            | Database user                        | `postgres`                 |
| `DB_PASSWORD`        | Database password                    | `changeme`                 |
| `DB_HOST`            | Database host                        | `localhost` / `db` (Docker)|
| `EMAIL_HOST`         | SMTP host                            | `smtp.gmail.com`           |
| `EMAIL_HOST_USER`    | SMTP username (email)                | your Gmail address         |
| `EMAIL_HOST_PASSWORD`| SMTP password / app password         | your app password          |

---

## Development Notes

- Static files are collected with WhiteNoise for production.
- The Dockerfile installs `gunicorn` and `whitenoise` and runs migrations on start.
- Currency list is loaded from `currencies.json`.
- Debug mode is enabled by default (`DEBUG = True`). Turn it off for production and set a proper `SECRET_KEY`.

---

## License

This project is provided as-is for personal / educational use.
