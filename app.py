import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE CONEXIÓN A MYSQL (DOCKER) ---
USUARIO_DB = 'root'
PASSWORD_DB = 'Peter046'
HOST_DB = 'localhost'  
NOMBRE_DB = 'sistema'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USUARIO_DB}:{PASSWORD_DB}@{HOST_DB}/{NOMBRE_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- 2. MODELO DE LA BASE DE DATOS ---
class Persona(db.Model):
    __tablename__ = 'personas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100))
    cedula = db.Column(db.String(20), unique=True) 
    telefono = db.Column(db.String(20))
    fecha_nac = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    fecha_registro = db.Column(db.String(30))

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

    # Recolectamos los datos del formulario
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    correo = request.form['correo']

    try:
        # CORRECCIÓN: Inserción directa con SQL Nativo para evitar conflictos de refresco con el ORM
        query_insert = text("""
            INSERT INTO personas (nombre, cedula, telefono, fecha_nac, correo, fecha_registro) 
            VALUES (:nombre, :cedula, :telefono, :fecha_nac, :correo, :fecha_registro)
        """)
        
        db.session.execute(query_insert, {
            'nombre': nombre,
            'cedula': cedula,
            'telefono': telefono,
            'fecha_nac': fecha_nac,
            'correo': correo,
            'fecha_registro': ahora
        })
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return f"<div style='color:white; background:#121212; padding:20px;'><h2>⚠️ Error al guardar: {str(e)}</h2></div>"

    return f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #121212; font-family: 'Poppins', sans-serif;">
        <div style="background: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0px 10px 30px rgba(0,255,0,0.1); width: 350px;">
            <div style="font-size: 50px; margin-bottom: 20px;">✅</div>
            <h2 style="color: #28a745; margin-top: 0;">¡Registro Exitoso!</h2>
            <p style="color: #333; margin-bottom: 30px;">Tus datos han sido almacenados correctamente en el Portafolio</p>
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
        try:
            # Consulta SQL explícita mapeada por columnas
            query = text("SELECT id, nombre, cedula, telefono, fecha_nac, correo, fecha_registro FROM personas ORDER BY id DESC")
            resultado = db.session.execute(query)
            
            usuarios_validos = []
            for fila in resultado:
                usuarios_validos.append({
                    "id": fila.id,              
                    "nombre": fila.nombre,
                    "cedula": fila.cedula,
                    "telefono": fila.telefono,
                    "fecha_nac": fila.fecha_nac,
                    "correo": fila.correo,
                    "fecha_registro": fila.fecha_registro
                })

            return render_template('usuarios.html', lista=usuarios_validos)
            
        except Exception as e:
            return f"<div style='color:white; background:#121212; padding:20px;'><h2>⚠️ Error en consulta: {str(e)}</h2></div>"
    else:
        return """<div style='text-align:center; color:white; background:#121212; height:100vh; padding-top:20%;'><h2>⚠️ Clave Incorrecta</h2><a href='/login'>Volver</a></div>"""

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)