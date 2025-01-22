from flask import Flask
from config import db, migrate
from routes.user import user_bp

app = Flask(__name__)

# Configuración de conexión a MySQL 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de base de datos y migraciones
db.init_app(app)
migrate.init_app(app, db)

# Registro de Blueprints / rutas
app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)
