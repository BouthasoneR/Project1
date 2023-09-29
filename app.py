# Bouthasone Rajasombat
# 11552013

from flask import Flask, request, jsonify
import jwt
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Create Flask app instance
app = Flask(__name__)
# Dictionary to store generated keys
keys = {}


# Function to generate a new RSA key pair and store it in the keys dictionary
def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    kid = str(datetime.datetime.timestamp(datetime.datetime.now()))
    # Store the generated private, public key, and expiration time in the keys dictionary
    keys[kid] = {
        "private_key": private_key,
        "public_key": public_key,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return kid, private_key, public_key


# Define route for authentication to generate JWT
@app.route('/auth', methods=['POST'])
def authenticate():
    # Get expired parameter from the request
    expired = request.args.get('expired')

    if expired:
        # Find an expired key or create a new one if none exists
        kid, private_key, _ = next(
            (
                (k, key['private_key'], key['public_key'])
                for k, key in keys.items()
                if key['exp'] < datetime.datetime.utcnow()
            ),
            generate_key_pair(),
        )
        # Set expiration time in the past for an expired token
        expiration = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    else:
        # Generate a new key pair for a valid token
        kid, private_key, _ = generate_key_pair()
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    # Encode the JWT and return it in the response
    token = jwt.encode({"kid": kid, "exp": expiration}, private_key, algorithm='RS256')
    return jsonify({"token": token})


# Define route to return JSON Web Key Set (JWKS)
@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    valid_keys = []
    for kid, key_info in keys.items():
        # Check if the key is still valid
        if key_info['exp'] > datetime.datetime.utcnow():
            public_key = key_info['public_key'].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode('utf-8')
            valid_keys.append({
                "alg": "RS256",
                "e": "AQAB",
                "kid": kid,
                "kty": "RSA",
                "n": public_key.split('\n')[1],
                "use": "sig",
            })

    return jsonify({"keys": valid_keys})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8080)

