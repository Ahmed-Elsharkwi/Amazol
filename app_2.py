from flask import Flask, request, jsonify
import base64
import os

from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_data = data['image']
    image_data = base64.b64decode(image_data)
    with open('uploaded_image.png', 'wb') as f:
        f.write(image_data)
    return jsonify({'message': 'Image received and saved successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
