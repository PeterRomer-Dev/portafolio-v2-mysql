import os
import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE RUTAS ABSOLUTAS ---
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'sistema.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 2. CORRECCIÓN EN CREACIÓN DE DB (Faltaba una coma) ---
def crear_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cedula TEXT,
            telefono TEXT,
            fecha_nac TEXT,
            correo TEXT,
            fecha_registro TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- RUTAS PÚBLICAS ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    ahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    datos = (
        request.form['nombre'],
        request.form['cedula'],
        request.form['telefono'],
        request.form['fecha_nac'],
        request.form['correo'],
        ahora
    )

    # USAR db_path PARA EVITAR QUE SE CREE OTRO ARCHIVO VACÍO
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO personas (nombre, cedula, telefono, fecha_nac, correo, fecha_registro)
        VALUES (?,?,?,?,?,?)
    ''', datos)
    conn.commit()
    conn.close()

    return f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #121212; font-family: 'Poppins', sans-serif;">
        <div style="background: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0px 10px 30px rgba(0,255,0,0.1); width: 350px;">
            <div style="font-size: 50px; margin-bottom: 20px;">✅</div>
            <h2 style="color: #28a745; margin-top: 0;">¡Registro Exitoso!</h2>
            <p style="color: #333; margin-bottom: 30px;">Tus datos han sido almacenados correctamente en el sistema.</p>
            <a href="/" style="color: #28a745; text-decoration: none; font-weight: bold; border: 2px solid #28a745; padding: 10px 25px; border-radius: 8px;">Continuar</a>
        </div>
    </div>
    """

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    clave_correcta = "Peter046"
    clave_ingresada = request.form['password']

    if clave_ingresada == clave_correcta:
        # USAR db_path AQUÍ TAMBIÉN
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personas ORDER BY id DESC')
        usuarios_registrados = cursor.fetchall()
        conn.close()
        return render_template('usuarios.html', lista=usuarios_registrados)
    else:
        return """<div style='text-align:center; color:white; background:#121212; height:100vh; padding-top:20%;'><h2>⚠️ Clave Incorrecta</h2><a href='/login'>Volver</a></div>"""

if __name__ == '__main__':
    crear_db()
    app.run(debug=True)