from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]+$')
NUMERO_REGEX = re.compile(r'^[0-9]*$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,})(?=.*[a-z])(?=.*[0-9])(?=.*[A-Z])(?=.*[@#$%^&+=.]).*$')

class User:
    db = 'events'

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id': user_id}
        result = connectToMySQL(User.db).query_db(query, data)
        if result:
            return result[0]
        return None

    @staticmethod
    def get_by_email(email):
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {'email': email}
        result = connectToMySQL(User.db).query_db(query, data)
        if result:
            return result[0]
        return None

    @staticmethod
    def create(first_name, last_name, email, password):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password
        }
        result = connectToMySQL(User.db).query_db(query, data)
        if result:
            print("User created with ID:", result)  # Mensaje de depuración
        else:
            print("User creation failed")  # Mensaje de error
        return result

    @staticmethod
    def validar(data):
        is_valid = True
        
        if len(data['first_name']) < 2:
            flash('Nombre debe tener al menos 2 caracteres y solo letras', 'register')
            is_valid = False
        if not NAME_REGEX.match(data['first_name']):
            flash("El nombre no puede tener numeros o caracteres especiales","register")
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Apellido debe tener al menos 2 caracteres y solo letras', 'register')
            is_valid = False
        if not NAME_REGEX.match(data['last_name']):
            flash("El apellido no puede tener numeros ocaracters especiales","register")
        if not EMAIL_REGEX.match(data['email']):
            flash("El email no cumple con las caracteristicas minimas solicitadas","register")
            is_valid = False
        if not data['email']:
            flash('Correo electrónico no válido', 'register')
            is_valid = False
        if len(data['password']) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Las contraseñas no coinciden', 'register')
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("La contraseña no cumple con las caracterisitas minimas","register")
            is_valid = False
        if User.get_by_email(data['email']):
            flash('El correo electrónico ya está registrado', 'register')
            is_valid = False
        return is_valid
    
