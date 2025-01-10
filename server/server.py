from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
from datetime import datetime

# IP fija para conexión directa por ethernet
SERVER_IP = "192.168.1.2"
SERVER_PORT = 5000

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = 'received_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', mode="SERVIDOR", ip=SERVER_IP, port=SERVER_PORT)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Archivo no encontrado", 404

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")

@socketio.on('file_transfer')
def handle_file_transfer(data):
    try:
        filename = data['filename']
        file_data = data['file_data']
        sender = data['sender']
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(file_path, 'wb') as f:
            if isinstance(file_data, str):
                f.write(file_data.encode())
            else:
                f.write(file_data)
        
        download_url = f"http://{SERVER_IP}:{SERVER_PORT}/download/{filename}"
        emit('file_received', {
            'filename': filename,
            'sender': sender,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'size': os.path.getsize(file_path),
            'download_url': download_url
        }, broadcast=True)
        
        print(f"Archivo recibido: {filename}")
    except Exception as e:
        print(f"Error al recibir archivo: {str(e)}")

if __name__ == '__main__':
    print(f"Servidor iniciado en {SERVER_IP}:{SERVER_PORT}")
    socketio.run(app, host=SERVER_IP, port=SERVER_PORT, debug=True, allow_unsafe_werkzeug=True)