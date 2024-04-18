from flask import Flask, request, jsonify
from hdfs import InsecureClient
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = Flask(__name__)
client = InsecureClient("http://<namenode>:<port>", user="<username>")
BLOCK_SIZE = 16

# Encrypts data using AES encryption
def encrypt_data(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(data.ljust(BLOCK_SIZE * (len(data) // BLOCK_SIZE + 1)))
    return ciphertext

# Decrypts data using AES decryption
def decrypt_data(key, data):
    iv = data[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(data[BLOCK_SIZE:]).rstrip(b'\0')
    return plaintext

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        key = get_random_bytes(16)  # Generate a random 16 bytes key
        segments = []

        # Read file in chunks and encrypt each chunk
        with client.write(request.form['path'], overwrite=True) as writer:
            while True:
                chunk = file.read(BLOCK_SIZE * 1024)  # Read 1 MB at a time
                if not chunk:
                    break
                encrypted_chunk = encrypt_data(key, chunk)
                segments.append(encrypted_chunk)
            for segment in segments:
                writer.write(segment)

        return jsonify({'message': 'File uploaded successfully', 'key': key.hex()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['GET'])
def download_file():
    path = request.args.get('path')
    key_hex = request.args.get('key')
    if not path or not key_hex:
        return jsonify({'error': 'Path or key parameter missing'}), 400

    try:
        key = bytes.fromhex(key_hex)
        file_content = b''

        with client.read(path) as reader:
            while True:
                encrypted_chunk = reader.read(BLOCK_SIZE * 1024)
                if not encrypted_chunk:
                    break
                decrypted_chunk = decrypt_data(key, encrypted_chunk)
                file_content += decrypted_chunk

        return file_content, 200, {'Content-Type': 'application/octet-stream'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete', methods=['DELETE'])
def delete_file():
    path = request.args.get('path')
    if not path:
        return jsonify({'error': 'Path parameter missing'}), 400

    try:
        client.delete(path)
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
