# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-05-10

### Added
- Admin login with JWT authentication and role-based access control
- Drag-and-drop resume upload supporting PDF, DOC, and DOCX formats
- Intelligent resume parsing service extracting name, email, phone, qualification, skills, experience, and domain
- Extracted data display screen with download option
- Team Lead selection UI with radio button interface
- Email notification to TL with full candidate details and resume attachment
- Magic link review system — TL accesses review page without login
- TL review portal with Shortlisted / Not Shortlisted decision
- Optional TL comments on review submission
- In-app admin notification center with unread badge
- Admin email notification on TL review completion
- Notification read/unread state management
- Auto-generated Swagger API documentation at `/docs`
- CORS configuration for frontend-backend separation
- SQL Server integration via SQLAlchemy ORM with PyODBC
- UPSERT-based user seed endpoint for flexible user management
- Detailed SMTP error logging in email service
- UUID-based file naming for upload security
- Token expiry (72 hours) on all review magic links
- Protected React routes with automatic redirect to login
- Axios interceptors for automatic JWT header injection and 401 auto-logout
- Responsive UI with Tailwind CSS

### Infrastructure
- FastAPI backend with modular router architecture
- React + Vite frontend
- SQL Server Express database
- Gmail SMTP email delivery
- Local file storage in `/uploads/`
- Python virtual environment setup
- Environment variable management with `python-dotenv`

---

## [Unreleased]

### Planned
- Bulk resume upload via ZIP
- AI-powered resume scoring
- Celery + Redis async email queue
- AWS S3 cloud file storage
- Docker containerisation
- CI/CD with GitHub Actions
- JWT refresh token rotation
- Rate limiting on authentication endpoints
- Alembic database migrations
