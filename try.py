from utils.jwt_encoding_decoding_method import create_jwt
from datetime import datetime, timedelta


token = create_jwt({"data_1": "943e4374-36c9-4b36-a214-4229d32aafb2",'type': 'seller', 'exp': datetime.utcnow() + timedelta(seconds=3600)})
print(token)
