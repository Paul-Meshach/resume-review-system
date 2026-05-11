# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |

---

## Reporting a Vulnerability

If you discover a security vulnerability, **do not open a public issue**.

Please report it privately:

1. Email the maintainer directly (see profile)
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fix

You will receive a response within 48 hours. If confirmed, a patch will be issued and you will be credited in the changelog.

---

## Security Practices in This Project

### Authentication
- JWT tokens signed with HS256 — secret key stored only in `.env`
- Tokens expire after 60 minutes (configurable)
- Passwords hashed using bcrypt via `passlib` — never stored in plaintext
- Same error message returned for invalid email or wrong password — prevents user enumeration

### File Uploads
- File type validated by extension on every upload
- UUID v4 used as filename — prevents path traversal attacks
- Files served via FastAPI `FileResponse` — not exposed as raw static files
- Upload directory is listed in `.gitignore`

### Magic Link Tokens
- UUID v4 tokens — cryptographically unpredictable
- Tokens expire after 72 hours
- Each token is single-use in the workflow context
- Expired tokens return `410 Gone`

### API Security
- CORS configured to allow only the specified frontend origin
- Admin-only endpoints protected via JWT dependency injection
- No sensitive user data included in JWT payload

### Environment Secrets
- All credentials stored in `.env`
- `.env` is listed in `.gitignore` and never committed
- `.env.example` provided with placeholder values only

---

## What Is NOT Covered

- MIME-type validation (extension-only check) — planned for v2
- Rate limiting on login endpoint — planned for v2
- JWT refresh token rotation — planned for v2
- Virus scanning on uploaded files — recommended for production deployments
