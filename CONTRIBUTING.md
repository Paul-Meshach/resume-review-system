# Contributing to Resume Review Workflow System

Thank you for your interest in contributing. This document outlines the process for contributing to this project.

---

## Code of Conduct

Be respectful, constructive, and professional in all interactions.

---

## How to Contribute

### Reporting Bugs

1. Check existing [Issues](../../issues) first
2. Open a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behaviour
   - Environment details (OS, Python version, Node version)
   - Screenshots or logs if applicable

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe the problem it solves
3. Describe the proposed solution
4. Note any alternatives considered

### Submitting Code

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/yourusername/resume-review-system.git
   ```
3. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```
4. **Make your changes** following the code style guidelines below
5. **Test your changes** manually
6. **Commit** following the commit convention:
   ```bash
   git commit -m "feat: add bulk resume upload support"
   git commit -m "fix: resolve SMTP timeout on slow connections"
   git commit -m "docs: update API reference for /reviews endpoint"
   ```
7. **Push** your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a **Pull Request** against `main`

---

## Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

| Prefix | Use For |
|--------|---------|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation change |
| `style:` | Formatting, no logic change |
| `refactor:` | Code restructure, no feature/fix |
| `test:` | Adding or fixing tests |
| `chore:` | Build process, tooling changes |

---

## Branch Naming Convention

| Pattern | Use For |
|---------|---------|
| `feature/description` | New features |
| `fix/description` | Bug fixes |
| `docs/description` | Documentation |
| `refactor/description` | Refactoring |

---

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8
- Use type hints on function signatures
- Docstrings on all public functions
- Keep route handlers thin — business logic belongs in `services/`
- Use `get_db` dependency injection for all database access

### JavaScript/React (Frontend)
- Functional components with hooks only
- One component per file
- Props should be explicitly typed where possible
- Keep API calls in the `api/` layer — not in components directly
- Handle loading and error states in every async component

---

## Pull Request Guidelines

- PRs should address a single concern
- Include a clear description of what changed and why
- Reference related issues using `Closes #issue_number`
- Keep PRs small and focused — easier to review
- Do not include `.env` files, `venv/`, `node_modules/`, or `uploads/`

---

## Development Setup

See [README.md](README.md) for full local setup instructions.

Quick start:
```bash
# Backend
cd backend && python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

---

## Questions?

Open a [GitHub Discussion](../../discussions) or create an issue with the `question` label.
