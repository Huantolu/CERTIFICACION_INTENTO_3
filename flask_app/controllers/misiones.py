from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.mision import Mision
from flask_app.models.usuario import Usuario

bcrypt= Bcrypt(app)

@app.route("/formulario_mision")
def ver_pagina():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para crear una misión", "error")
        return redirect("/")
    
    datos_usuario = {
    'id': session.get('usuario_id')
    }
    usuario_sesion = Usuario.get_by_id(datos_usuario)

    return render_template('crear_mision.html',usuario_sesion=usuario_sesion)


#ruta para procesar registro de la mision
@app.route('/crear_mision', methods=['POST'])
def crear_mision():
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para crear una misión", "error")
        return redirect("/")
    
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    voluntarios_necesarios = request.form['voluntarios_necesarios']
    descripcion = request.form['descripcion']
    
    datos = {
        'nombre': nombre,
        'fecha': fecha,
        'voluntarios_necesarios': voluntarios_necesarios,
        'descripcion': descripcion,
        'usuarios_id': session.get('usuario_id')
    }

    #guardar nuevo dato e iniciar sesión
    Mision.save(datos)

    return redirect('/dashboard')
#aqui podemos editar los datos antes registrados
@app.route("/editar/<int:mision_id>")
def editar(mision_id):

    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para editar", "error")
        return redirect("/")

    data = {
        "id": mision_id
    }
    mision = Mision.get_by_id(data)
    datos_sesion = {
        "id": session['usuario_id']
    }
    lider = Usuario.get_by_id(datos_sesion)

    usuario_sesion = Usuario.get_by_id({'id':session['usuario_id']})
    return render_template("editar_mision.html", mision=mision, lider=lider, usuario_sesion=usuario_sesion)

@app.route("/editar_mision", methods=['POST'])
def editar_mision():


    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para editar", "error")
        return redirect("/")

    id = request.form.get("id")

    print(id)
    nombre = request.form.get("nombre")
    fecha = request.form.get('fecha')
    voluntarios_necesarios = request.form.get('voluntarios_necesarios')
    descripcion = request.form.get('descripcion')


    data = {
        'id': id,
        "nombre": nombre,
        "fecha": fecha,
        "voluntarios_necesarios": voluntarios_necesarios,
        'descripcion': descripcion,

    }
    print(data)
    Mision.update(data)

    return redirect("/dashboard")

@app.route('/ver/<int:mision_id>', methods=['GET'])
def ver_mision(mision_id):
    if 'usuario_id' not in session:
        flash("Debes iniciar sesión para ver la misión", "error")
        return redirect("/")

    mision = Mision.get_by_id(mision_id)

    if not mision:
        flash("Misión no encontrada.", "error")
        return redirect('/dashboard')

    return render_template('mision.html', mision=mision)