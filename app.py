from flask import Flask, render_template, jsonify
import os
from ecdsa import SigningKey, SECP256k1
import base58
from flask_cors import CORS
from Crypto.Hash import keccak
import logging

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def keccak256(data):
    try:
        k = keccak.new(digest_bits=256)
        k.update(data)
        return k.hexdigest()
    except Exception as e:
        logger.error(f"Keccak hash hatası: {str(e)}")
        raise

def generate_tron_address():
    try:
        # Generate a random 32-byte private key
        private_key = os.urandom(32).hex()

        # Generate public key using ECDSA
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        public_key = sk.verifying_key.to_string().hex()

        # Hash the public key with Keccak-256
        hash_value = keccak256(bytes.fromhex(public_key))

        # Add '41' prefix and take last 40 characters
        tron_address_hex = '41' + hash_value[-40:]

        # Encode address with Base58Check
        tron_address = base58.b58encode_check(bytes.fromhex(tron_address_hex)).decode()

        return {
            "private_key": private_key,
            "public_key": public_key,
            "tron_address": tron_address
        }
    except Exception as e:
        logger.error(f"Adres oluşturma hatası: {str(e)}")
        raise

def verify_tron_address(private_key, tron_address):
    try:
        # Generate public key from private key
        sk = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        public_key = sk.verifying_key.to_string().hex()

        # Hash public key with Keccak-256
        hash_value = keccak256(bytes.fromhex(public_key))

        # Recreate TRON address
        tron_address_hex = '41' + hash_value[-40:]
        generated_address = base58.b58encode_check(bytes.fromhex(tron_address_hex)).decode()

        # Compare addresses
        return generated_address == tron_address
    except Exception as e:
        logger.error(f"Adres doğrulama hatası: {str(e)}")
        return False

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Ana sayfa hatası: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    try:
        wallet = generate_tron_address()
        return jsonify({
            'success': True,
            'data': wallet
        })
    except Exception as e:
        logger.error(f"Generate API hatası: {str(e)}")
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
        logger.error(f"Verify API hatası: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Vercel için WSGI uygulaması
app.debug = False

# Lokal geliştirme için
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)