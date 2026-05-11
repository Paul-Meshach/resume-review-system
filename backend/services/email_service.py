# services/email_service.py — UPDATED with detailed error logging

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

EMAIL_HOST     = os.getenv("EMAIL_HOST",    "smtp.gmail.com")
EMAIL_PORT     = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER     = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
FRONTEND_URL   = os.getenv("FRONTEND_URL",  "http://localhost:5173")


def _validate_email_config():
    """Called before every send — raises immediately if .env is misconfigured."""
    if not EMAIL_USER:
        raise ValueError("EMAIL_USER is not set in .env")
    if not EMAIL_PASSWORD:
        raise ValueError("EMAIL_PASSWORD is not set in .env")
    if "@" not in EMAIL_USER:
        raise ValueError(f"EMAIL_USER looks invalid: '{EMAIL_USER}'")


def send_email(to: str, subject: str, html_body: str, attachment_path: str = None):
    """
    Core SMTP sender.
    Raises exception with clear message on any failure.
    """
    _validate_email_config()

    print(f"\n[EMAIL] Attempting to send to: {to}")
    print(f"[EMAIL] Subject: {subject}")
    print(f"[EMAIL] From: {EMAIL_USER}")

    msg = MIMEMultipart("alternative")
    msg["From"]    = EMAIL_USER
    msg["To"]      = to
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    # Attach resume file if provided
    if attachment_path:
        if not os.path.exists(attachment_path):
            print(f"[EMAIL WARNING] Attachment not found: {attachment_path}")
        else:
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(part)
            print(f"[EMAIL] Attachment added: {filename}")

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=15) as server:
            server.set_debuglevel(0)   # set to 1 to see full SMTP handshake logs
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to, msg.as_string())

        print(f"[EMAIL] ✅ Successfully sent to {to}")

    except smtplib.SMTPAuthenticationError:
        raise RuntimeError(
            "Gmail authentication failed.\n"
            "Fix: Go to Google Account → Security → App Passwords\n"
            "Generate a new App Password and paste it in .env as EMAIL_PASSWORD.\n"
            "Do NOT use your regular Gmail password."
        )
    except smtplib.SMTPRecipientsRefused:
        raise RuntimeError(
            f"Gmail refused recipient address: {to}\n"
            "Check that the TL/admin email address in the DB is a valid email."
        )
    except smtplib.SMTPException as e:
        raise RuntimeError(f"SMTP error while sending email: {str(e)}")
    except TimeoutError:
        raise RuntimeError(
            "Connection to Gmail SMTP timed out.\n"
            "Check your internet connection and firewall settings."
        )


def send_review_request_email(
    tl_email: str,
    tl_name: str,
    candidate: dict,
    review_token: str,
    resume_path: str
):
    review_link = f"{FRONTEND_URL}/tl-review?token={review_token}"

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;
                padding:20px;border:1px solid #ddd;border-radius:8px;">
        <h2 style="color:#2563EB;">📋 Resume Review Request</h2>
        <p>Hello <strong>{tl_name}</strong>,</p>
        <p>You have been assigned a candidate resume for review:</p>

        <div style="background:#F8FAFC;padding:15px;border-radius:6px;margin:15px 0;">
            <h3 style="color:#1E3A5F;margin-top:0;">Candidate Details</h3>
            <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:6px 0;color:#666;width:140px;">Name</td>
                    <td><strong>{candidate.get('name','N/A')}</strong></td></tr>
                <tr><td style="padding:6px 0;color:#666;">Email</td>
                    <td>{candidate.get('email','N/A')}</td></tr>
                <tr><td style="padding:6px 0;color:#666;">Phone</td>
                    <td>{candidate.get('phone','N/A')}</td></tr>
                <tr><td style="padding:6px 0;color:#666;">Qualification</td>
                    <td>{candidate.get('qualification','N/A')}</td></tr>
                <tr><td style="padding:6px 0;color:#666;">Experience</td>
                    <td>{candidate.get('years_of_experience','N/A')}</td></tr>
                <tr><td style="padding:6px 0;color:#666;">Domain</td>
                    <td>{candidate.get('domain','N/A')}</td></tr>
                <tr><td style="padding:6px 0;color:#666;">Skills</td>
                    <td>{candidate.get('skills','N/A')}</td></tr>
            </table>
        </div>

        <p>The original resume is attached. Please click below to submit your decision:</p>

        <div style="text-align:center;margin:25px 0;">
            <a href="{review_link}"
               style="background:#2563EB;color:white;padding:12px 30px;
                      text-decoration:none;border-radius:6px;font-weight:bold;
                      display:inline-block;">
                📝 Review Candidate
            </a>
        </div>

        <p style="color:#999;font-size:12px;">
            Link expires in 72 hours. If button doesn't work, paste this in your browser:<br>
            <a href="{review_link}">{review_link}</a>
        </p>
    </div>
    """

    send_email(tl_email, "📋 Resume Review Request", html, resume_path)


def send_admin_notification_email(
    admin_email: str,
    admin_name: str,
    candidate_name: str,
    tl_name: str,
    status: str,
    comments: str = None
):
    color = "#16A34A" if status == "shortlisted" else "#DC2626"
    icon  = "✅"      if status == "shortlisted" else "❌"

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;
                padding:20px;border:1px solid #ddd;border-radius:8px;">
        <h2 style="color:#2563EB;">🔔 Review Decision Received</h2>
        <p>Hello <strong>{admin_name}</strong>,</p>
        <p>A Team Lead has completed reviewing a candidate.</p>

        <div style="background:#F8FAFC;padding:15px;border-radius:6px;margin:15px 0;">
            <p><strong>Candidate:</strong> {candidate_name}</p>
            <p><strong>Reviewed by:</strong> {tl_name}</p>
            <p><strong>Decision:</strong>
                <span style="color:{color};font-weight:bold;">
                    {icon} {status.upper()}
                </span>
            </p>
            {f'<p><strong>Comments:</strong> {comments}</p>' if comments else ''}
        </div>

        <p>Log in to the dashboard to view full details.</p>
    </div>
    """

    send_email(admin_email, f"🔔 Review Complete: {candidate_name}", html)