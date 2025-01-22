from models.User import User
from flask import request, jsonify
from config import db  

    # FUNCION PARA OBTENER USUARIOS
def get_all_users():
    users = User.query.all()
    
    # LISTA DE USUARIOS
    return [{"id": user.id, "name": user.name, "email": user.email} for user in users]

    # FUNCION PARA BUSCAR USUARIO POR ID
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    
    # Verificar si el usuario existe
    if user:
        return {"id": user.id, "name": user.name, "email": user.email}
    else:
        return {"message": "Usuario no encontrado"}, 404

    # FUNCION PARA CREAR USUARIO
def create_user():
    # OBTENER DATOS
    data = request.get_json()

    # Validar que los campos requeridos estén presentes
    if not data.get('name') or not data.get('email'):
        return jsonify({"message": "Faltan datos requeridos: 'name' o 'email'"}), 400

    # Verificar si el correo electrónico ya está registrado
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "El correo electrónico ya está registrado."}), 400

    try:
        # NUEVA INSTANCIA PARA EL USUARIO
        new_user = User(name=data['name'], email=data['email'])

        # AGREGAR EL NUEVO USUARIO A LA BD
        db.session.add(new_user)
        db.session.commit()

        # MOSTRAR DATOS DEL USUARIO CREADO
        return jsonify({"id": new_user.id, "name": new_user.name, "email": new_user.email}), 201

    except Exception as e:
        # En caso de error, hacer rollback en la transacción
        db.session.rollback()
        return jsonify({"message": f"Error al crear el usuario: {str(e)}"}), 500

    # EDITAR USUARIO POR ID
def update_user(user_id):
    # OBTENER DATOS
    data = request.get_json()

    # VALIDAR DATOS
    if not data.get('name') and not data.get('email'):
        return jsonify({"message": "Faltan datos a actualizar: 'name' o 'email'"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "El correo electrónico ya está registrado."}), 400

    # BUSCAR AL USUARIO POR SU ID
    user = User.query.get(user_id)
    # SI NO SE ENCUENTRA QUE MANDE UN MENSAJE DE QUE NO SE ENCONTRO EL USUARIO
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    try:
        # ACTUALIZAR DATOS
        if data.get('name'):
            user.name = data['name']
        if data.get('email'):
            user.email = data['email']

        # GUARDAR CAMBIOS EN LA BD
        db.session.commit()

        # MOSTRAR DATOS ACTUALIZADOS
        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al actualizar el usuario: {str(e)}"}), 500

    # ELIMINAR USUARIO POR ID
def delete_user(user_id):
    # BUSCAR AL USUARIO POR ID
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    try:
        # ELIMINAR USUARIO DE LA BD
        db.session.delete(user)
        db.session.commit()

        # MOSTRAR MENSAJE DE CONFIRMACION 
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error al eliminar el usuario: {str(e)}"}), 500
