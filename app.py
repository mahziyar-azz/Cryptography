from flask import Flask, render_template, request, jsonify
from utils import base64_convert, hash_convert, aes_convert
from utils import base64_convert, hash_convert, aes_convert, aes_rsa_convert

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main page of the application."""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        text = data.get('text')
        conversion_type = data.get('type')
        action = data.get('action')
        algorithm = data.get('algorithm')
        key = data.get('key')

        # new (for aes_rsa)
        public_key = data.get('public_key')
        private_key = data.get('private_key')

        result = None

        if conversion_type == 'base64':
            result = base64_convert(text, action)
        elif conversion_type == 'hash':
            result = hash_convert(text, algorithm)
        elif conversion_type == 'aes':
            if not key:
                return jsonify({'error': 'AES key is required.'}), 400
            result = aes_convert(text, action, key)
        elif conversion_type == 'aes_rsa':
            # validate required key by action
            if action == 'encrypt' and not public_key:
                return jsonify({'error': 'RSA public_key is required for AES-RSA encrypt.'}), 400
            if action == 'decrypt' and not private_key:
                return jsonify({'error': 'RSA private_key is required for AES-RSA decrypt.'}), 400
            result = aes_rsa_convert(text, action, public_key, private_key)

        if result is None:
            return jsonify({'error': 'Invalid conversion type or action.'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
