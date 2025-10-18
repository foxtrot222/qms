import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_token_email(to_email: str,token: str):
    """
    Sends an email with the generated token to the user.
    """
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    FROM_NAME = os.getenv("FROM_NAME", "App")

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
        return response.status_code
    except Exception as e:
        raise RuntimeError(f"SendGrid Error: {str(e)}")

def send_otp_email(to_email: str, otp: str):
    """
    Sends an email with the generated OTP to the user.
    """
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    FROM_NAME = os.getenv("FROM_NAME", "App")

    if not (SENDGRID_API_KEY and FROM_EMAIL and to_email):
        raise RuntimeError("Missing SendGrid config or recipient email")

    subject = "Your OTP"
    plain_text = f"Your OTP is {otp}"
    html_content = f"<p>Your OTP is <strong>{otp}</strong></p>"

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
        return response.status_code
    except Exception as e:
        raise RuntimeError(f"SendGrid Error: {str(e)}")

def send_completion_email(to_email: str, service_time: str):
    """
    Sends an email with the service completion details to the user.
    """
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
    FROM_NAME = os.getenv("FROM_NAME", "App")

    if not (SENDGRID_API_KEY and FROM_EMAIL and to_email):
        raise RuntimeError("Missing SendGrid config or recipient email")

    subject = "Service Completed Successfully"
    html_content = f"""
    <h3>Service Completed</h3>
    <p>Your service has been completed successfully.</p>
    <p><strong>Service Time:</strong> {service_time}</p>
    <p>Thank you for choosing our service!</p>
    """

    message = Mail(
        from_email=(FROM_EMAIL, FROM_NAME),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        raise RuntimeError(f"SendGrid Error: {str(e)}")

if __name__ == "__main__":
    # This requires .env to be in the same directory for direct execution
    from dotenv import load_dotenv
    load_dotenv()
    send_token_email("test@example.com","A04")