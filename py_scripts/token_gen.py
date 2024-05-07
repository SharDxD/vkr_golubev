import secrets

def gen(user_type):
    token = secrets.token_urlsafe(16)
    body = {
        "user_type": user_type,
        "token": token 
    }
    return body
