from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
)

NOMBRE_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$')



class Usuario:

    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    #registrar usuario / CREAR
    @classmethod
    def save(cls, data):
        query= "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s,%(apellido)s,%(email)s,%(password)s, NOW(), NOW());"
        return connectToMySQL('VoluntaMe').query_db(query, data)

    #Metodos para ver registros
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        usuario_en_db= connectToMySQL('VoluntaMe').query_db(query)
        usuarios = []

        for elemento in usuario_en_db:
            usuarios.append(cls(elemento))

        return usuarios

    @classmethod
    def get_by_id(cls, datos):
        query= "SELECT * FROM usuarios WHERE id = %(id)s;"
        usuario_en_db= connectToMySQL('VoluntaMe').query_db(query, datos)
        if not usuario_en_db:
            return None
        return cls(usuario_en_db[0])


    #método lo usamos en validaciones, en inicio de sesión
    @classmethod
    def get_by_email(cls, datos):
        query= "SELECT * FROM usuarios WHERE email = %(email)s;"
        usuario_en_db= connectToMySQL('VoluntaMe').query_db(query, datos)
        if not usuario_en_db:
            return None
        return cls(usuario_en_db[0])

    @classmethod
    def update(cls, datos):
        
        query= "UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, password=%(password)s, updated_at = NOW() WHERE id=%(id)s"

        return connectToMySQL('VoluntaMe').query_db(query, datos)

    @classmethod
    def delete(cls, datos):
        
        query= "DELETE FROM usuarios WHERE id=%(id)s"

        return connectToMySQL('VoluntaMe').query_db(query, datos)

    @staticmethod
    def validar_registro(formulario):
        es_valido=True

        # Validaciones y campos
        # Nombre: solo letras, al menos 2 caracteres y que no esté vacía
        if not formulario.get('nombre'):
            flash('El nombre es obligatorio', 'registro')
            es_valido=False
        elif len(formulario.get('nombre'))<2:
            flash("El nombre debe tener al menos 2 caracteres", "registro")
            es_valido = False
        elif not NOMBRE_REGEX.fullmatch(formulario.get('nombre')):
            flash("El nombre sólo contener letras y espacios", "registro")
            es_valido=False
        
        # Apellido: solo letras, al menos 2 caracteres y que no esté vacía
        if not formulario.get('apellido'):
            flash('El apellido es obligatorio', 'registro')
            es_valido=False
        elif len(formulario.get('apellido'))<2:
            flash("El apellido debe tener al menos 2 caracteres", "registro")
            es_valido = False
        elif not NOMBRE_REGEX.fullmatch(formulario.get('apellido')):
            flash("El apellido sólo contener letras y espacios", "registro")
            es_valido=False

        # E-mail: formato correcto de correo, que no exista previamente en la base de datos y que no esté vacía
        if not formulario.get('email'):
            flash("El email es obligatorio", "registro")
            es_valido=False
        elif not EMAIL_REGEX.fullmatch(formulario.get('email')):
            flash("El email no tiene formato valido", "registro")
            es_valido = False
        elif Usuario.get_by_email({'email': formulario.get('email')}):
            flash("Este email ya se encuentra ocupado", "registro")
            es_valido = False
        
        # Contraseña: al menos 8 caracteres y que no esté vacía
        if not formulario.get('password'):
            flash("La contraseña es obligatoria", "registro")
            es_valido = False
        elif len(formulario.get('password'))<8:
            flash("La contraseña debe tener al menos 8 caracteres", "registro")
            es_valido = False
        # Confirmación de contraseña: que coincida con la contraseña
        if not formulario.get('password'):
            flash("Debes confirmar tu contraseña", "registro")
            es_valido = False
        elif formulario.get('password') != formulario.get('password'):
            flash("Las contraseñas no coinciden", "registro")
            es_valido=False

        return es_valido