from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os

# IPs fijas para conexión directa por ethernet
CLIENT_IP = "192.168.1.1"
CLIENT_PORT = 5001
SERVER_IP = "192.168.1.2"
SERVER_PORT = 5000

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = 'cliente_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', mode="CLIENTE", ip=SERVER_IP, port=SERVER_PORT)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@socketio.on('connect')
def handle_connect():
    print("Conectado al servidor")

@socketio.on('file_received')
def handle_file_received(data):
    print(f"Notificación de archivo recibido: {data}")

if __name__ == '__main__':
    print(f"Cliente iniciado en {CLIENT_IP}:{CLIENT_PORT}")
    print(f"Conectando al servidor en {SERVER_IP}:{SERVER_PORT}")
    socketio.run(app, host=CLIENT_IP, port=CLIENT_PORT, debug=True, allow_unsafe_werkzeug=True)