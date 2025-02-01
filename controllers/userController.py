from models.User import User
from flask import request, jsonify
from config import db  

    # FUNCION PARA OBTENER USUARIOS
def get_all_users():
    users = User.query.all()
    try: 
    # LISTA DE USUARIOS
        return [ user.to_dict() for user in users]
    except Exception as error:
        print(f"ERROR {error}")
        #return jsonify({ "Error" : error}) 

    # FUNCION PARA BUSCAR USUARIO POR ID
def get_user_by_id(user_id):
    try:
        # Buscar el usuario por ID
        user = User.query.get(user_id)
        
        # Verificar si el usuario existe
        if user:
            return jsonify(user.to_dict())
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404

    except Exception as error:
        print(f"ERROR: {error}")

# FUNCION PARA CREAR USUARIO
def create_user(name, email):
    try:
        # Verificar si el email ya está registrado
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "El correo electrónico ya está registrado"}, 400

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        return new_user.to_dict()

    except Exception as e:
        print(f"ERROR: {e}")

    # EDITAR USUARIO POR ID
def update_user(user_id, name, email):
    try:
        # BUSCAR EL USUARIO EXISTENTE POR ID
        user = User.query.get(user_id)

        # Verificar si el usuario existe
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar si ya existe un usuario con el mismo correo (excluyendo el usuario actual)
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"message": "El correo electrónico ya está registrado"}), 400

        # ACTUALIZAR LOS DATOS DEL USUARIO
        user.name = name
        user.email = email

        # GUARDAR LOS CAMBIOS EN LA BASE DE DATOS
        db.session.commit()

        # DEVOLVER LOS DATOS ACTUALIZADOS DEL USUARIO
        return user.to_dict()

    except Exception as e:
        print(f"ERROR: {e}")

    # ELIMINAR USUARIO POR ID
def delete_user(user_id):
    try:
        # Buscar el usuario por ID
        user = User.query.get(user_id)
        
        # Si no existe el usuario, devolver error
        if not user:
            return {"message": "Usuario no encontrado"}, 404
        
        # Eliminar el usuario
        db.session.delete(user)
        db.session.commit()

        return {"message": "Usuario eliminado exitosamente"}

    except Exception as e:
        print(f"ERROR: {e}")
