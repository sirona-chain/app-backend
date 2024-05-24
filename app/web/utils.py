import jwt
import datetime
import requests
from flask import current_app


def generate_confirmation_token(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def send_email(to, subject, html):
    api_key = current_app.config.get('MAILGUN_API_KEY')
    domain = current_app.config.get('MAILGUN_DOMAIN')
    sender = current_app.config.get('MAILGUN_DEFAULT_SENDER')

    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": sender,
              "to": [to],
              "subject": subject,
              "html": html})

    return response


# example of sending an email
# response = send_email('recipient@example.com', 'subject', 'email body')
# print(f"Status: {response.status_code}")
# print(f"Body: {response.text}")
