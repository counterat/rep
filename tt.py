import jwt

token = jwt.encode({'user_id': 1}, 'secret_key', algorithm='HS256')

# Валидация токена
decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])
print(decoded_token)