from flask import Flask, render_template, jsonify
import os
from ecdsa import SigningKey, SECP256k1
from eth_hash.auto import keccak
import base58
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_tron_address():
    # Generate a random 32-byte private key
    private_key = os.urandom(32).hex()

    # Generate public key using ECDSA
    sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
    public_key = sk.verifying_key.to_string().hex()

    # Hash the public key with Keccak-256
    hash_value = keccak(bytes.fromhex(public_key)).hex()

    # Add '41' prefix and take last 40 characters
    tron_address_hex = '41' + hash_value[-40:]

    # Encode address with Base58Check
    tron_address = base58.b58encode_check(bytes.fromhex(tron_address_hex)).decode()

    return {
        "private_key": private_key,
        "public_key": public_key,
        "tron_address": tron_address
    }

def verify_tron_address(private_key, tron_address):
    try:
        # Generate public key from private key
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        public_key = sk.verifying_key.to_string().hex()

        # Hash public key with Keccak-256
        hash_value = keccak(bytes.fromhex(public_key)).hex()

        # Recreate TRON address
        tron_address_hex = '41' + hash_value[-40:]
        generated_address = base58.b58encode_check(bytes.fromhex(tron_address_hex)).decode()

        # Compare addresses
        return generated_address == tron_address
    except Exception:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    try:
        wallet = generate_tron_address()
        return jsonify({
            'success': True,
            'data': wallet
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/verify/<private_key>/<tron_address>')
def verify(private_key, tron_address):
    try:
        is_valid = verify_tron_address(private_key, tron_address)
        return jsonify({
            'success': True,
            'is_valid': is_valid
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)