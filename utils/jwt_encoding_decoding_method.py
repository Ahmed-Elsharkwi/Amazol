import jwt
import uuid
# Define your secret key. This should be kept private.
SECRET_KEY = "What is the fuck"

# Create a JWT
def create_jwt(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Verify a JWT
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
