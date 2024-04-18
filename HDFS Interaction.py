from flask import Flask, request, jsonify
from hdfs import InsecureClient

app = Flask(__name__)
client = InsecureClient("http://<namenode>:<port>", user="<username>")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        with client.write(request.form['path'], overwrite=True) as writer:
            writer.write(file.read())
        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['GET'])
def download_file():
    path = request.args.get('path')
    if not path:
        return jsonify({'error': 'Path parameter missing'}), 400

    try:
        with client.read(path) as reader:
            file_content = reader.read()
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
