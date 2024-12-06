from flask import Flask, render_template
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'super_secret_key'

bcrypt = Bcrypt(app)

# Manejo de error 404 - Página no encontrada
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
