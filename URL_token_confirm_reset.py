import os
from dotenv import load_dotenv
load_dotenv()

from itsdangerous import URLSafeTimedSerializer



def generate_email_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('GENERAL_SECRET'))
    
    return serializer.dumps(email, salt=os.getenv('EMAIL_CONFIRM_SALT'))


def confirm_email_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('GENERAL_SECRET'))
    try:
        email = serializer.loads(
            token, salt=os.getenv('EMAIL_CONFIRM_SALT'), max_age=expiration
        )
        return email
    except Exception:
        return False


def generate_password_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('GENERAL_SECRET'))
    
    return serializer.dumps(email, salt=os.getenv('PASSWORD_RESET_SALT'))


def confirm_password_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('GENERAL_SECRET'))
    try:
        email = serializer.loads(
            token, salt=os.getenv('PASSWORD_RESET_SALT'), max_age=expiration
        )
        return email
    except Exception:
        return False


'''
def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False
'''
