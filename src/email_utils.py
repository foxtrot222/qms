import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME", "App")

def send_token_email(to_email: str,token: str):
    """
    Sends an email with the generated token to the user.
    """
    if not (SENDGRID_API_KEY and FROM_EMAIL and to_email):
        raise RuntimeError("Missing SendGrid config or recipient email")

    subject = "Your Token"
    plain_text = f"Your token is {token}"
    html_content = f"<p>Your token is <strong>{token}</strong></p>"

    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject=subject,
        plain_text_content=plain_text,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code  # 202 means accepted
    except Exception as e:
        raise RuntimeError(f"SendGrid Error: {str(e)}")

if __name__ == "__main__":
    send_token_email("krishnabhatiya211@gmail.com","A04")