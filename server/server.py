from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
from datetime import datetime
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'

# Configuración explícita de CORS para Socket.IO
socketio = SocketIO(app, 
    cors_allowed_origins="*",
    ping_timeout=10000,
    ping_interval=5000
)

UPLOAD_FOLDER = 'received_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

SERVER_IP = get_local_ip()
SERVER_PORT = 5000

@app.route('/')
def index():
    return render_template('index.html', mode="SERVIDOR", ip=SERVER_IP, port=SERVER_PORT)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
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
            f.write(file_data.encode() if isinstance(file_data, str) else file_data)
        
        emit('file_received', {
            'filename': filename,
            'sender': sender,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'size': len(file_data),
            'download_url': f"http://{SERVER_IP}:{SERVER_PORT}/download/{filename}"
        }, broadcast=True)
        print(f"Archivo recibido: {filename}")
    except Exception as e:
        print(f"Error al recibir archivo: {str(e)}")

if __name__ == '__main__':
    print(f"Servidor iniciado en {SERVER_IP}:{SERVER_PORT}")
    socketio.run(app, host=SERVER_IP, port=SERVER_PORT, debug=True, allow_unsafe_werkzeug=True)
