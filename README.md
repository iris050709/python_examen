

---

**Configuración de Aplicación Flask en Amazon Linux con Nginx y Gunicorn (Clonando desde Git)**

Este documento describe los pasos para configurar una aplicación Flask en una instancia de Amazon Linux utilizando Nginx como servidor web y Gunicorn como servidor WSGI, clonando el código desde un repositorio de Git.

---

**Instalar MySQL Client**

```bash
sudo dnf clean packages
sudo dnf install -y https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
sudo dnf install mysql-community-server --nogpgcheck -y
```

Para conectarte a la base de datos RDS:

```bash
sudo mysql -u admin -p -h database-1.c5ksy2okacbh.us-east-2.rds.amazonaws.com
```

## 3. Instalar Nginx

Instala Nginx y habilítalo para que se inicie automáticamente:

```bash
sudo dnf install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

## 4. Crear el directorio de la aplicación y clonar el repositorio

Crea el directorio para la aplicación Flask y clona el repositorio:

```bash
sudo mkdir -p /opt/flask_app
sudo chown ec2-user:ec2-user /opt/flask_app
cd /opt/flask_app
```

Clona tu repositorio desde GitHub o GitLab (reemplaza la URL con la de tu proyecto):

```bash
git clone https://github.com/usuario/repositorio.git .
```

Si tu repositorio es privado, debes configurar claves SSH o usar autenticación con token.

## 5. Instalar Python, PIP y dependencias

Instala Python 3 y PIP, luego instala las dependencias desde el archivo `requirements.txt` de tu repositorio:

```bash
sudo dnf install python3-pip -y
sudo pip3 install -r requirements.txt
```

Si el repositorio no tiene `requirements.txt`, instala Flask y Gunicorn manualmente:

```bash
sudo pip3 install Flask gunicorn flask-restful flask-swagger-ui
```

## 6. Verificar el punto de entrada de la aplicación

Abre el archivo principal de la aplicación (por ejemplo, `app.py`) y asegúrate de que contenga el siguiente código mínimo:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app running on EC2 with Nginx and Gunicorn!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

Si el nombre del archivo principal no es `app.py`, modifica el archivo del servicio de Gunicorn en el siguiente paso.

## 7. Configurar Gunicorn como servicio

Encuentra la ubicación de Gunicorn:

```bash
which gunicorn
```

Crea el archivo de servicio para Gunicorn:

```bash
sudo vi /etc/systemd/system/flask_app.service
```

Añade el siguiente contenido, ajustando `app:app` si el punto de entrada es diferente (por ejemplo, `main:app` si el archivo es `main.py`):

```ini
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/opt/flask_app
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

Recarga y habilita el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl start flask_app
sudo systemctl enable flask_app
sudo systemctl status flask_app
```

## 8. Configurar Nginx

Edita la configuración de Nginx:

```bash
sudo vi /etc/nginx/nginx.conf
```

Añade este bloque dentro de `http {}`:

```nginx
server {
    listen 80;
    server_name 54.224.134.84;  # Reemplaza con tu dirección IP pública

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Verifica que la configuración de Nginx sea válida:

```bash
sudo nginx -t
```

Si no hay errores, reinicia Nginx:

```bash
sudo systemctl restart nginx
```

## 9. Configurar HTTPS con un certificado autofirmado

Crea un directorio para los certificados SSL:

```bash
sudo mkdir -p /etc/nginx/ssl
```

Genera un certificado SSL autofirmado:

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/nginx-selfsigned.key \
  -out /etc/nginx/ssl/nginx-selfsigned.crt
```

Edita el archivo de configuración de Nginx para añadir SSL:

```bash
sudo vi /etc/nginx/nginx.conf
```

Añade este bloque además del anterior:

```nginx
server {
    listen 443 ssl;
    server_name 54.224.134.84;  # Reemplaza con tu IP pública

    ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Verifica la configuración:

```bash
sudo nginx -t
```

Si no hay errores, reinicia Nginx:

```bash
sudo systemctl restart nginx
```

## 10. Pruebas finales

1. Abre un navegador y accede a `http://<tu_IP_pública>`. Deberías ver el mensaje de la aplicación Flask.
2. Si configuraste SSL, accede a `https://<tu_IP_pública>`. Es posible que el navegador muestre una advertencia porque el certificado es autofirmado.
3. Verifica los servicios en ejecución:

```bash
sudo systemctl status flask_app
sudo systemctl status nginx
```

## 11. Actualización del código desde Git

Si necesitas actualizar la aplicación desde el repositorio, ejecuta:

```bash
cd /opt/flask_app
git pull origin main  # O la rama que uses
sudo systemctl restart flask_app
```

---

¡Listo! Tu aplicación Flask debería estar corriendo con Nginx y Gunicorn en tu instancia EC2.
```

Este archivo contiene todos los pasos detallados para configurar la aplicación Flask desde un repositorio Git y ponerla en funcionamiento en una instancia de Amazon EC2 con Nginx y Gunicorn.