from flask import Blueprint, jsonify, request
from controllers.userController import get_all_users, get_user_by_id, create_user, update_user, delete_user

##EL PAYLOAD SON DATOS QUE SE ENVIAN

# Creación del Blueprint / ruta definida para usuarios
user_bp = Blueprint('users', __name__)

# RUTA DE LISTA DE USUARIOS
@user_bp.route('/', methods=['GET'])
def index():
    users = get_all_users()
    return jsonify({"users": users})  # Devuelve la lista de usuarios en formato JSON

# VER UN USUARIO EN ESPECIFICO
@user_bp.route('/<int:user_id>', methods=['GET'])
def show(user_id):
    user = get_user_by_id(user_id)
    return jsonify(user)  # Devuelve la información del usuario específico

# CREAR UN USUARIO
@user_bp.route('/', methods=['POST']) #EL ARROBA ES UN DECORADOR
def user_Store():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    print(f"NAME {name} --- EMAIL {email}")
    new_user = create_user(name, email)
    return jsonify(new_user)

# ACTUALIZAR USUARIO POR ID
@user_bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    return update_user(user_id)  

# ELIMINAR UN USUARIO POR ID
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    return delete_user(user_id) 