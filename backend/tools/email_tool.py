"""
email_tool.py — sends real emails via Gmail SMTP using an App Password.

Setup:
  1. Enable 2-Step Verification on the Gmail account
  2. Go to https://myaccount.google.com/apppasswords
  3. Create an app password named "RM Copilot"
  4. Add to .env:
       EMAIL_PROVIDER=gmail
       GMAIL_ADDRESS=sara@gmail.com
       GMAIL_APP_PASSWORD=abcdefghijklmnop   <- no spaces
"""
import os
import smtplib
import ssl
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from .base import ProposedAction, ToolResult
from infrastructure.audit_log import log_human_action

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for candidate in [Path.cwd() / ".env", PROJECT_ROOT / ".env", Path(__file__).resolve().parents[1] / ".env"]:
    if candidate.exists():
        load_dotenv(candidate, override=False)
        break


# -- Propose (no side effects) ------------------------------------------------

def send_email(
    to_name: str,
    to_email: str,
    subject: str,
    body: str,
    rm_id: str,
    customer_id: str,
) -> ProposedAction:
    """
    Build a ProposedAction for sending a follow-up email.
    Nothing is sent until the RM clicks Approve.
    """
    return ProposedAction(
        tool    = "send_email",
        label   = "Approve & Send Email",
        summary = f'Send follow-up email to {to_name} <{to_email}> — "{subject}"',
        payload = {
            "to_name":     to_name,
            "to_email":    to_email,
            "subject":     subject,
            "body":        body,
            "rm_id":       rm_id,
            "customer_id": customer_id,
        },
    )


# -- Execute (RM approved — email is actually sent here) ----------------------

async def execute_email(payload: dict, rm_id: str) -> ToolResult:
    """Called only after RM clicks Approve."""
    try:
        result = _send_via_gmail(
            to_email = payload["to_email"],
            to_name  = payload["to_name"],
            subject  = payload["subject"],
            body     = payload["body"],
        )
        log_human_action(
            rm_id       = rm_id,
            customer_id = payload["customer_id"],
            action      = "approved",
            context     = f"Email sent to {payload['to_email']}: {payload['subject']}",
        )
        return result
    except Exception as exc:
        return ToolResult(
            success = False,
            message = "Email failed to send",
            error   = str(exc),
        )


# -- Gmail SMTP sender --------------------------------------------------------

def _send_via_gmail(
    to_email: str,
    to_name: str,
    subject: str,
    body: str,
) -> ToolResult:
    gmail_address = (
        os.getenv("GMAIL_ADDRESS", "").strip()
        or os.getenv("GAMIL_ADDRESS", "").strip()
    )
    app_password  = os.getenv("GMAIL_APP_PASSWORD", "").strip().replace(" ", "")

    # Validation
    if not gmail_address:
        raise ValueError("GMAIL_ADDRESS is not set in .env")
    if not app_password:
        raise ValueError(
            "GMAIL_APP_PASSWORD is not set in .env. "
            "Get one at https://myaccount.google.com/apppasswords"
        )
    if len(app_password) != 16:
        raise ValueError(
            f"GMAIL_APP_PASSWORD looks wrong — expected 16 chars, got {len(app_password)}. "
            "Remove any spaces when pasting."
        )

    # Build message
    sender_name = os.getenv("EMAIL_SENDER_NAME", "Esraa").strip() or "Esraa"
    msg = MIMEMultipart("alternative")
    msg["From"]    = f"{sender_name} <{gmail_address}>"
    msg["To"]      = f"{to_name} <{to_email}>"
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(_to_html(body), "html"))

    # Send
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(gmail_address, app_password)
        server.sendmail(gmail_address, to_email, msg.as_string())

    print(f"[Email] Sent to {to_email}: {subject}")
    return ToolResult(
        success = True,
        message = f"Email sent to {to_name} <{to_email}>",
        data    = {"from": gmail_address, "to": to_email, "subject": subject},
    )


def _to_html(plain_body: str) -> str:
    paragraphs = "".join(
        f"<p style='margin:0 0 12px 0;'>{line}</p>"
        for line in plain_body.split("\n")
        if line.strip()
    )
    return f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#1a1a1a;
             max-width:600px;margin:0 auto;padding:24px;">
  {paragraphs}
  <hr style="border:none;border-top:1px solid #e5e7eb;margin:24px 0;" />
  <p style="font-size:12px;color:#6b7280;margin:0;">
    Sent via RM Copilot &middot; Finaira
  </p>
</body>
</html>"""