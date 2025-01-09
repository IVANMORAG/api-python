from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import socket
import base64

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

# Configura aquí la IP del servidor
SERVER_IP = "192.168.1.155"  # CAMBIA ESTO con la IP del servidor
SERVER_PORT = 5000

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, 
    cors_allowed_origins="*",
    ping_timeout=10000,
    ping_interval=5000
)

UPLOAD_FOLDER = 'cliente_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CLIENT_IP = get_local_ip()
CLIENT_PORT = 5001

@app.route('/')
def index():
    return render_template('index.html', mode="CLIENTE", ip=SERVER_IP, port=SERVER_PORT)

@app.route('/download/<filename>')
def download_file(filename):
    """Ruta para descargar un archivo recibido."""
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@socketio.on('connect')
def handle_connect():
    print("Conectado al servidor")

@socketio.on('file_received')
def handle_file_received(data):
    try:
        filename = data['filename']
        file_data = base64.b64decode(data['file_data'])  # Decodificar el archivo base64

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        print(f"Archivo recibido y guardado: {filename}")
        emit('file_saved', {
            'filename': filename,
            'download_link': f"/download/{filename}"
        })
    except Exception as e:
        print(f"Error al guardar archivo: {str(e)}")
        


if __name__ == '__main__':
    print(f"Cliente iniciado en {CLIENT_IP}:{CLIENT_PORT}")
    print(f"Conectando al servidor en {SERVER_IP}:{SERVER_PORT}")
    socketio.run(app, host=CLIENT_IP, port=CLIENT_PORT, debug=True, allow_unsafe_werkzeug=True)
