from utils.jwt_encoding_decoding_method import create_jwt
from datetime import datetime, timedelta


token = create_jwt({"data_1": "da3f8c13-74bb-477f-9452-7b3c2de24082", 'exp': datetime.utcnow() + timedelta(seconds=3600)})
print(token)
