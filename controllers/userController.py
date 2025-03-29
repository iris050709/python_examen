import os
from flask import request, jsonify
from config import db  
from models.User import User
from flask_jwt_extended import create_access_token

# FUNCION PARA OBTENER USUARIOS
def get_all_users():
    users = User.query.all()
    try: 
        return [user.to_dict() for user in users]
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({"message": "Error al obtener usuarios"}), 500

# FUNCION PARA BUSCAR USUARIO POR ID
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return user.to_dict()  # Solo devolver los datos del usuario en formato diccionario
        else:
            return {"message": "Usuario no encontrado"}  # No hacer jsonify aquí
    except Exception as error:
        print(f"ERROR: {error}")
        return {"message": "Error al buscar el usuario"}  # No hacer jsonify aquí


# FUNCION PARA VERIFICAR SI UN EMAIL EXISTE
def email_exists(email, user_id=None):
    try:
        query = User.query.filter(User.email == email)
        if user_id:
            query = query.filter(User.id != user_id)
        existing_user = query.first()
        if existing_user:
            return {"exists": True, "message": "El correo electrónico ya está registrado."}
        return {"exists": False, "message": "El correo electrónico no está registrado."}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"exists": False, "message": "Error al verificar el correo."}

# FUNCION PARA CREAR USUARIO
def create_user(name, email, password):
    try:
        email_check = email_exists(email)
        if email_check["exists"]:
            return {"message": email_check["message"]}, 400

        new_user = User(
            name=name,
            email=email,
            password=password  # Se encripta en el modelo
        )

        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    except Exception as e:
        print(f"ERROR: {e}")
        return {"message": "Error al crear el usuario"}, 500

def update_user(user_id, name, email):
    try:
        user = User.query.get(user_id)
        if not user:
            return {"message": "Usuario no encontrado"}, 404

        email_check = email_exists(email, user_id)
        if email_check["exists"]:
            return {"message": email_check["message"]}, 400

        user.name = name
        user.email = email
        # No actualizar la contraseña

        db.session.commit()
        return user.to_dict()
    except Exception as e:
        print(f"ERROR: {e}")
        return {"message": "Error al actualizar el usuario"}, 500

# ELIMINAR USUARIO POR ID
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return {"message": "Usuario no encontrado"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"message": "Error al eliminar el usuario"}, 500
    
# INICIAR SESIÓN
def login_user(email, password):
    user = User.query.filter_by(email=email).first() 
    
    if user and user.check_password(password):  # Verificar la contraseña
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }), 200
    
    return jsonify({"msg": "CREDENCIALES INVÁLIDAS"}), 401
