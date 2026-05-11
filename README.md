<div align="center">

# 📋 Resume Review Workflow System

### Enterprise-Grade Recruitment Workflow Management Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-Express-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.x-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> A full-stack enterprise workflow system that automates the entire resume screening process —
> from upload and intelligent parsing to Team Lead assignment, email delivery, and real-time review notifications.

<br/>

[API Docs](http://localhost:8000/docs) · [Report Bug](../../issues) · [Request Feature](../../issues)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-system-architecture)
- [Workflow](#-workflow)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Email Setup](#-gmail-smtp-setup)
- [Security](#-security)
- [Future Roadmap](#-future-roadmap)
- [Deployment](#-deployment)
- [Known Limitations](#-known-limitations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧭 Overview

The **Resume Review Workflow System** is a modular, production-oriented recruitment platform built for internal HR operations. It eliminates manual resume routing by providing a complete digital workflow — from upload to Team Lead review decision — with automated email notifications at every stage.

### Business Problem Solved

| Before | After |
|--------|-------|
| Manual PDF forwarding via email chains | Automated email with parsed candidate data + attachment |
| No structured review tracking | Full workflow state tracked in SQL Server |
| Resume data manually re-typed | Auto-extracted via intelligent regex parsing |
| No notification system | Real-time in-app + email notifications |
| Untracked TL decisions | Auditable review records with timestamps |

---

## ✨ Features

### Admin Panel
- 🔐 Secure JWT-authenticated login
- 📤 Drag-and-drop resume upload (PDF / DOC / DOCX)
- 🤖 Automatic candidate data extraction
- 👥 Team Lead selection with radio button UI
- 📧 One-click resume forwarding via HTML email
- 🔔 Real-time notification center with unread badge
- 📥 Resume download from the platform

### Team Lead Portal
- 🔗 Magic link access via email — no login required
- 👁️ Full candidate profile view
- ✅ One-click Shortlist / Reject decision
- 💬 Optional review comments
- ⏱️ 72-hour token expiry for security

### System Features
- 🏗️ Modular router-based FastAPI backend
- 🗃️ SQLAlchemy ORM with SQL Server
- 📨 HTML email with resume attachment via Gmail SMTP
- 📝 Auto-generated Swagger API docs at `/docs`
- 🔒 Role-based access control (Admin / TL)
- 🌐 CORS-configured for frontend-backend separation

---

## 🛠️ Tech Stack

### Frontend

| Technology | Version | Purpose |
|-----------|---------|---------|
| React.js | 18.x | UI component framework |
| Vite | 5.x | Lightning-fast build tool |
| Tailwind CSS | 3.x | Utility-first styling |
| Axios | 1.x | HTTP client with JWT interceptors |
| React Router DOM | 6.x | Client-side routing |
| React Hook Form | 7.x | Performant form management |
| React Toastify | 10.x | User-facing notification toasts |

### Backend

| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104+ | High-performance async API framework |
| Python | 3.10+ | Core backend language |
| SQLAlchemy | 2.x | ORM for database abstraction |
| PyODBC | 4.x | SQL Server ODBC connection driver |
| python-jose + cryptography | Latest | JWT token creation and verification |
| Passlib + bcrypt | Latest | Password hashing |
| pdfplumber | Latest | PDF text layer extraction |
| python-docx | Latest | DOCX document parsing |
| python-multipart | Latest | Multipart file upload handling |
| python-dotenv | Latest | Secure environment variable loading |
| smtplib | Built-in | Gmail SMTP email delivery |

### Infrastructure

| Component | Technology |
|----------|-----------|
| Database | Microsoft SQL Server Express |
| Auth Strategy | Stateless JWT with role-based access |
| Email Provider | Gmail SMTP (TLS port 587) |
| File Storage | Local filesystem (`/uploads/`) |
| API Documentation | Swagger UI — auto-generated by FastAPI |

---

## 🏛️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       BROWSER CLIENT                             │
│                   React + Vite  :5173                            │
│                                                                  │
│   Login → Dashboard → Upload → Extract → TL Select → Notifs    │
└──────────────────────────┬───────────────────────────────────────┘
                           │  Axios + JWT Bearer Token
┌──────────────────────────▼───────────────────────────────────────┐
│                  FASTAPI BACKEND  :8000                          │
│                                                                  │
│  /auth      /resumes      /tls      /reviews    /notifications   │
│                                                                  │
│  AuthService ── JWTService ── ParserService ── EmailService      │
└──────────────────────────┬───────────────────────────────────────┘
                           │  SQLAlchemy ORM
┌──────────────────────────▼───────────────────────────────────────┐
│             SQL SERVER EXPRESS (SQLEXPRESS)                      │
│        users │ candidates │ reviews │ notifications              │
└──────────────────────────┬───────────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                  Gmail SMTP (TLS :587)                           │
│        TL Review Email + Admin Notification Email                │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Workflow

```
  [Admin] Login
      │
      ▼
  [Admin] Upload Resume (PDF / DOC / DOCX)
      │
      ▼
  [System] Auto-Parse → Extract Name, Email, Phone,
           Skills, Experience, Qualification, Domain
      │
      ▼
  [Admin] Review Extracted Data + Download Resume
      │
      ▼
  [Admin] Select Team Lead (radio button)
      │
      ▼
  [System] Send Email to TL
           └── HTML email + resume attachment + magic link
      │
      ▼
  [TL] Open Magic Link → View Candidate Profile
      │
      ├── Shortlisted ──┐
      └── Rejected ─────┤
                        ▼
               [System] Update DB + Create Notification
                        │
                        ▼
               [Admin] In-App Notification + Email Alert
                        │
                        ▼
                  Workflow Complete ✅
```

---

## 📁 Project Structure

```
resume-review-system/
│
├── backend/
│   ├── main.py                   # App entry point, CORS, router registration
│   ├── database.py               # Engine, SessionLocal, get_db dependency
│   ├── .env                      # Secrets (git-ignored)
│   ├── requirements.txt
│   │
│   ├── models/                   # SQLAlchemy ORM table definitions
│   │   ├── user.py               # users table — Admin + TL roles
│   │   ├── candidate.py          # candidates table — extracted resume data
│   │   ├── review.py             # reviews table — workflow + magic tokens
│   │   └── notification.py       # notifications table — admin alerts
│   │
│   ├── schemas/                  # Pydantic request/response models
│   │   ├── auth.py
│   │   ├── candidate.py
│   │   └── review.py
│   │
│   ├── routers/                  # Route handlers — one file per domain
│   │   ├── auth.py               # /auth/*
│   │   ├── resumes.py            # /resumes/*
│   │   ├── tls.py                # /tls/*
│   │   ├── reviews.py            # /reviews/*
│   │   └── notifications.py      # /notifications/*
│   │
│   ├── services/                 # Business logic layer
│   │   ├── auth_service.py       # JWT + bcrypt
│   │   ├── parser.py             # PDF + DOCX extraction + regex parsing
│   │   └── email_service.py      # SMTP composition + delivery
│   │
│   └── uploads/                  # Resume storage (auto-created, git-ignored)
│
├── frontend/
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx               # Routes + layout
│       ├── index.css             # Tailwind directives
│       │
│       ├── api/
│       │   └── axios.js          # Axios instance + JWT interceptors
│       │
│       ├── context/
│       │   └── AuthContext.jsx   # Global auth state
│       │
│       ├── components/
│       │   ├── Navbar.jsx
│       │   └── ProtectedRoute.jsx
│       │
│       └── pages/
│           ├── Login.jsx
│           ├── ResumeUpload.jsx
│           ├── ExtractedDetails.jsx
│           ├── TLSelection.jsx
│           ├── TLReview.jsx      # Token-based, no login needed
│           └── Notifications.jsx
│
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

---

## 🗄️ Database Schema

### `users`
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK | Auto-increment |
| name | VARCHAR(100) | |
| email | VARCHAR(150) UNIQUE | Login identifier |
| password_hash | VARCHAR(255) | bcrypt hashed |
| role | ENUM(admin, tl) | Access control |
| is_active | BIT | Soft disable flag |
| created_at | DATETIME | |

### `candidates`
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK | |
| name | VARCHAR(150) | Extracted |
| email | VARCHAR(150) | Extracted |
| phone | VARCHAR(20) | Extracted |
| qualification | VARCHAR(255) | Extracted |
| skills | TEXT | Comma-separated |
| years_of_experience | VARCHAR(50) | Extracted |
| domain | VARCHAR(150) | Detected |
| resume_file_path | VARCHAR(500) | Server path only |
| original_filename | VARCHAR(255) | |
| uploaded_at | DATETIME | |
| uploaded_by | INT FK→users.id | |

### `reviews`
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK | |
| candidate_id | INT FK→candidates.id | |
| assigned_tl_id | INT FK→users.id | |
| status | ENUM(pending, shortlisted, rejected) | |
| review_token | VARCHAR(255) UNIQUE | UUID magic link |
| token_expiry | DATETIME | +72h from creation |
| comments | TEXT | Optional TL notes |
| assigned_at | DATETIME | |
| reviewed_at | DATETIME | Set on submission |

### `notifications`
| Column | Type | Notes |
|--------|------|-------|
| id | INT PK | |
| admin_id | INT FK→users.id | |
| review_id | INT FK→reviews.id | |
| message | TEXT | Display text |
| is_read | BIT | Read status |
| created_at | DATETIME | |

---

## 📡 API Reference

**Base URL:** `http://localhost:8000`

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/login` | None | Login → JWT token |
| `GET` | `/auth/me` | JWT | Current user info |
| `POST` | `/auth/seed-users` | None | Upsert default users |
| `GET` | `/auth/users-list` | None | List all users |
| `POST` | `/auth/reset-password` | None | Reset a user password |

### Resumes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/resumes/upload` | Admin JWT | Upload + parse resume |
| `GET` | `/resumes/{id}` | Admin JWT | Get extracted data |
| `GET` | `/resumes/{id}/download` | Admin JWT | Download original file |

### Team Leads

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/tls/` | Admin JWT | List all TLs |

### Reviews

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/reviews/send` | Admin JWT | Assign + email TL |
| `GET` | `/reviews/by-token/{token}` | Token | TL get review details |
| `POST` | `/reviews/submit` | Token | TL submit decision |

### Notifications

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/notifications/` | Admin JWT | All notifications |
| `PATCH` | `/notifications/{id}/read` | Admin JWT | Mark as read |
| `GET` | `/notifications/unread-count` | Admin JWT | Unread count |

> 📖 Full interactive API documentation available at `http://localhost:8000/docs`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ LTS
- SQL Server Express + SSMS
- ODBC Driver 17 for SQL Server
- Git

### 1 — Clone

```bash
git clone https://github.com/yourusername/resume-review-system.git
cd resume-review-system
```

### 2 — Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your DB credentials and Gmail App Password
uvicorn main:app --reload --port 8000
```

### 3 — Database

Open SSMS and run:
```sql
CREATE DATABASE ResumeReviewDB;
```
Tables are auto-created on first backend startup.

Seed users via Swagger:
```
http://localhost:8000/docs → POST /auth/seed-users → Execute
```

### 4 — Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: `http://localhost:5173`

---

## ⚙️ Environment Variables

```env
# Database
DATABASE_URL=mssql+pyodbc://sa:Password@HOST\SQLEXPRESS/ResumeReviewDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes

# JWT
SECRET_KEY=your-minimum-32-char-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=youremail@gmail.com
EMAIL_PASSWORD=your16charapppassword

# App
FRONTEND_URL=http://localhost:5173
```

See `.env.example` for a full template with descriptions.

---

## 📧 Gmail SMTP Setup

1. Enable **2-Step Verification** on your Google account
2. Go to **Security → App Passwords**
3. Generate a password for "Mail"
4. Paste the 16-character code as `EMAIL_PASSWORD` in `.env`

> ⚠️ Use the App Password — not your Gmail login password.

---

## 🔐 Security

- JWT stateless authentication with role-based access control
- bcrypt password hashing with timing-safe comparison
- UUID v4 magic link tokens with 72-hour expiry
- UUID-based filenames prevent path traversal
- CORS restricted to frontend origin
- No sensitive data in JWT payload
- All secrets in `.env` — never hardcoded

---

## 🔭 Future Roadmap

- [ ] AI resume scoring via LLM API
- [ ] Bulk upload with ZIP support
- [ ] Celery + Redis for async email queue
- [ ] AWS S3 / Azure Blob for file storage
- [ ] Docker containerisation
- [ ] CI/CD with GitHub Actions
- [ ] Alembic database migrations
- [ ] Interview scheduling workflow
- [ ] Analytics dashboard

---

## 🌐 Deployment

### Backend
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
Recommended: AWS EC2, Azure App Service, Railway, Render

### Frontend
```bash
npm run build   # outputs to dist/
```
Recommended: Vercel, Netlify, AWS S3

### Database
Migrate to Azure SQL or Amazon RDS for SQL Server in production.

---

## ⚠️ Known Limitations

- Resume parsing accuracy varies with non-standard formatting
- Gmail SMTP limited to ~500 emails/day
- Local file storage — not suited for multi-server deployments
- No JWT refresh token — users re-login after expiry
- SQL Server Express capped at 10GB

---

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

```bash
git checkout -b feature/your-feature
git commit -m "feat: describe your change"
git push origin feature/your-feature
# Open a Pull Request
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Paul Meshach**

[![GitHub](https://img.shields.io/badge/GitHub-yourhandle-181717?style=flat&logo=github)](https://github.com/Paul-Meshach)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/paul-meshach-s-8951a3341/)

---

<div align="center">

Built with precision · Engineered for real workflows · Designed to scale

⭐ Star this repository if you found it useful

</div>
