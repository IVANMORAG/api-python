# Manual de Configuración - Sistema de Transferencia de Archivos

## Configuración del Cliente (Windows)

### 1. Preparación del Sistema
1. Instalar Python (si no está instalado):
   - Descargar Python desde https://www.python.org/downloads/
   - Durante la instalación, marcar "Add Python to PATH"
   
2. Crear directorio del proyecto:
```bash
mkdir cliente
cd cliente
```

### 2. Configuración del Entorno Virtual
1. Abrir PowerShell como administrador
2. Crear el entorno virtual:
```bash
python -m venv env
```
3. Activar el entorno virtual:
```bash
.\env\Scripts\activate
```

### 3. Instalación de Dependencias
```bash
pip install flask
pip install flask-socketio
pip install flask-cors
pip install python-engineio==4.8.0
pip install python-socketio==5.9.0
pip install eventlet
```

### 4. Estructura de Directorios
```
cliente/
├── cliente.py
├── templates/
│   └── index.html
└── cliente_files/
```

Crear los directorios necesarios:
```bash
mkdir templates
mkdir cliente_files
```

### 5. Configuración de Red
1. Abrir Panel de Control > Redes e Internet > Conexiones de red
2. Click derecho en el adaptador Ethernet > Propiedades
3. Seleccionar "Protocolo de Internet versión 4 (TCP/IPv4)"
4. Click en Propiedades
5. Configurar:
   - Dirección IP: 192.168.1.1
   - Máscara de subred: 255.255.255.0
   - Puerta de enlace predeterminada: dejar vacío

### 6. Archivos del Proyecto
1. Crear `cliente.py` con el código proporcionado en el proyecto
2. Crear `templates/index.html` con el código de la interfaz

### 7. Ejecución
1. Activar el entorno virtual (si no está activado):
```bash
.\env\Scripts\activate
```
2. Ejecutar el cliente:
```bash
python cliente.py
```

## Configuración del Servidor (Ubuntu)

### 1. Preparación del Sistema
1. Actualizar el sistema:
```bash
sudo apt update
sudo apt upgrade
```

2. Instalar Python y pip si no están instalados:
```bash
sudo apt install python3
sudo apt install python3-pip
```

### 2. Configuración del Entorno Virtual
1. Instalar venv si no está instalado:
```bash
sudo apt install python3-venv
```

2. Crear y acceder al directorio del proyecto:
```bash
mkdir servidor
cd servidor
```

3. Crear el entorno virtual:
```bash
python3 -m venv env
```

4. Activar el entorno virtual:
```bash
source env/bin/activate
```

### 3. Instalación de Dependencias
```bash
pip install flask
pip install flask-socketio
pip install flask-cors
pip install python-engineio==4.8.0
pip install python-socketio==5.9.0
pip install eventlet
```

### 4. Estructura de Directorios
```
servidor/
├── servidor.py
├── templates/
│   └── index.html
└── received_files/
```

Crear los directorios necesarios:
```bash
mkdir templates
mkdir received_files
```

### 5. Configuración de Red
1. Editar la configuración de red:
```bash
sudo nano /etc/netplan/01-network-manager-all.yaml
```

2. Agregar la configuración:
```yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eth0:
      addresses:
        - 192.168.1.2/24
      dhcp4: no
```

3. Aplicar la configuración:
```bash
sudo netplan apply
```

### 6. Archivos del Proyecto
1. Crear `servidor.py` con el código de servidor
2. Crear `templates/index.html` con el código de la interfaz

### 7. Ejecución
1. Activar el entorno virtual (si no está activado):
```bash
source env/bin/activate
```

2. Ejecutar el servidor:
```bash
python servidor.py
```

## Verificación de la Conexión

1. Conectar ambas computadoras con un cable Ethernet

2. Verificar la conexión:
   - Desde Windows (cliente):
   ```bash
   ping 192.168.1.2
   ```
   - Desde Ubuntu (servidor):
   ```bash
   ping 192.168.1.1
   ```

3. Acceder a las interfaces web:
   - Cliente: http://192.168.1.1:5001
   - Servidor: http://192.168.1.2:5000

## Consideraciones Importantes

1. Los firewalls de ambos sistemas deben permitir las conexiones en los puertos 5000 y 5001
2. Asegurarse de que ambos sistemas estén en la misma subred
3. El cable Ethernet debe estar correctamente conectado
4. Los entornos virtuales deben estar activados antes de ejecutar los scripts
5. Los permisos de los directorios deben estar correctamente configurados

## Solución de Problemas Comunes

1. Si la conexión falla:
   - Verificar la configuración IP en ambos sistemas
   - Comprobar el cable Ethernet
   - Verificar que los puertos no estén bloqueados

2. Si los archivos no se transfieren:
   - Verificar los permisos de los directorios
   - Comprobar que los entornos virtuales estén activados
   - Revisar los logs en busca de errores

3. Si la interfaz web no carga:
   - Verificar que el archivo index.html esté en la carpeta templates
   - Comprobar que todas las dependencias estén instaladas
   - Revisar los logs del servidor/cliente