from flask import Blueprint, jsonify, request
from controllers.userController import get_all_users, get_user_by_id, create_user, update_user, delete_user, login_user, email_exists

##EL PAYLOAD SON DATOS QUE SE ENVIAN

# Creación del Blueprint / ruta definida para usuarios
user_bp = Blueprint('users', __name__)

# RUTA DE LISTA DE USUARIOS
@user_bp.route('/', methods=['GET'])
def index():
    user = get_all_users()
    return jsonify(user)  # Devuelve la lista de usuarios en formato JSON

# VER UN USUARIO EN ESPECIFICO
@user_bp.route('/<int:user_id>', methods=['GET'])
def show(user_id):
    user_response = get_user_by_id(user_id)
    return user_response  # Devuelve la información del usuario específico

@user_bp.route('/', methods=['POST'])  # EL ARROBA ES UN DECORADOR
def user_store():
    data = request.get_json()

    # Obtener datos del JSON
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    # Validar que todos los campos obligatorios estén presentes
    if not email or not name or not password:
        return jsonify({"message": "Todos los campos son obligatorios"}), 400

    # Verificar si el correo ya está registrado
    if email_exists(email)['exists']:
        return jsonify({"message": "Este correo ya está registrado. Usa otro."}), 400

    # Crear usuario en la base de datos
    new_user = create_user(name, email, password)

    return jsonify(new_user), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "Datos no proporcionados"}), 400

    name = data.get('name')
    email = data.get('email')  # Obtén el correo de los datos enviados

    if not name:
        return jsonify({"message": "El nombre es obligatorio"}), 400

    # Obtener el usuario actual
    user = get_user_by_id(user_id)
    if isinstance(user, dict) and "message" in user:  # Si es un diccionario con un mensaje de error
        return jsonify(user), 404  # Retornar el error

    # Si el correo es diferente al correo actual y es necesario verificar si está en uso
    if email and email != user['email'] and email_exists(email):
        return jsonify({"message": "Este correo ya está en uso por otro usuario."}), 400

    # Actualizar el nombre y el correo solo si se proporciona un correo nuevo
    updated_user = update_user(user_id, name, email if email else user['email'])

    return jsonify(updated_user), 200  # Retorna la respuesta JSON correcta


# ELIMINAR UN USUARIO POR ID
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):
    try:
        # Llamar a la función delete_user
        result = delete_user(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": f"Error al eliminar el usuario: {str(e)}"}), 500
    
@user_bp.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    if 'email' not in data:
        return jsonify({"message": "El campo email es obligatorio"}), 400
    email_check = email_exists(data['email'])
    return jsonify(email_check), 200

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Verifica si los datos están presentes
    if 'email' not in data or 'password' not in data:
        return jsonify({"msg": "El correo y la contraseña son obligatorios"}), 400

    return login_user(data['email'], data['password'])
