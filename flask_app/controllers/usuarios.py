from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision

bcrypt= Bcrypt(app)

#ruta inico
@app.route('/')
def inicio():
    if "usuario_id" in session:
        return redirect('/dashboard')
    return render_template('index.html')

#ruta para procesar registro
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    #1 validar la informacion
    if not Usuario.validar_registro(request.form):
        return redirect('/')
    #2. encriptar contraseña
    password_hash= bcrypt.generate_password_hash(request.form['password'])

    datos={
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': password_hash,
    }

    #guardar nuevo dato e iniciar sesión
    id_nuevo= Usuario.save(datos)
    session['usuario_id']= id_nuevo
    session['nombre']= request.form['nombre']

    return redirect('/dashboard')

#inicio sesión 
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    #buscamos al usuario por su email
    usuario = Usuario.get_by_email({'email': request.form['email_inicio_sesion']})

    #si no existe o la contraseña no coincide, mostramos el mismo mensaje
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password_inicio_sesion']):
        flash("E-mail o contraseña incorrectos", "inicio_sesion")
        return redirect('/')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/dashboard')

#ruta para procesar login

#lugar donde entramos cuando logeamos
@app.route('/dashboard')
def index():
    if 'usuario_id' not in session:
        return redirect('/')
    misiones = Mision.get_all()
    lideres= []
    for elemento in misiones:
        datos={
            "id": elemento.usuarios_id
        }
        lideres.append(Usuario.get_by_id(datos))
    return render_template('dashboard.html', misiones=Mision.get_all(), usuario=session['nombre'], lideres=lideres)

#cerrar sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect('/')