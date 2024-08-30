from utils.jwt_encoding_decoding_method import create_jwt
from datetime import datetime, timedelta


token = create_jwt({"data_1": "7156dec4-2ca3-4e31-988b-2ac92f982266",'type': 'seller', 'exp': datetime.utcnow() + timedelta(seconds=3600)})
print(token)
