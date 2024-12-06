from flask_app import app, bcrypt
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models.user import User

@app.route('/')
def index():
    print (session)
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "confirm_password": request.form['confirm_password']
    }

    if not User.validar(data):
        flash('Error en el registro. Por favor, revise los campos.', 'register')
        return redirect(url_for('index'))

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    print("Datos a insertar:", data['first_name'], data['last_name'], data['email'], hashed_password) 
    User.create(data['first_name'], data['last_name'], data['email'], hashed_password)

    flash('Usuario registrado exitosamente', 'register')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.get_by_email(email)

    if user and bcrypt.check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Correo o contraseña incorrecta', 'login')
        return redirect(url_for('index'))
    

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))


