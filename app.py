from flask import Flask, render_template, request, jsonify
from utils import base64_convert, hash_convert, aes_convert

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main page of the application."""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """Handles the conversion requests from the frontend."""
    try:
        data = request.get_json()
        text = data.get('text')
        conversion_type = data.get('type')
        action = data.get('action')
        algorithm = data.get('algorithm')
        key = data.get('key')

        result = None

        if conversion_type == 'base64':
            result = base64_convert(text, action)
        elif conversion_type == 'hash':
            result = hash_convert(text, algorithm)
        elif conversion_type == 'aes':
            if not key:
                return jsonify({'error': 'AES key is required.'}), 400
            result = aes_convert(text, action, key)

        if result is None:
            return jsonify({'error': 'Invalid conversion type or action.'}), 400

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
