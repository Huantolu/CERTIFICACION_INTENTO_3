from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Mision:

    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.fecha = data.get('fecha')
        self.voluntarios_necesarios = data.get('voluntarios_necesarios')
        self.descripcion = data.get('descripcion')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.usuarios_id = data.get('usuarios_id')

    #registrar usuario / CREAR
    @classmethod
    def save(cls, data):
        query= "INSERT INTO misiones (nombre, fecha, voluntarios_necesarios, descripcion, created_at, updated_at, usuarios_id) VALUES (%(nombre)s,%(fecha)s,%(voluntarios_necesarios)s,%(descripcion)s, NOW(), NOW(), %(usuarios_id)s);"
        return connectToMySQL('VoluntaMe').query_db(query, data)

    #Metodos para ver registros
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM misiones;"
        mision_en_db= connectToMySQL('VoluntaMe').query_db(query)
        misiones = []

        for elemento in mision_en_db:
            misiones.append(cls(elemento))

        return misiones

    @classmethod
    def update(cls, datos):
        
        query= "UPDATE misiones SET nombre=%(nombre)s, fecha=%(fecha)s, voluntarios_necesarios=%(voluntarios_necesarios)s, descripcion=%(descripcion)s, updated_at = NOW() WHERE id=%(id)s"

        return connectToMySQL('VoluntaMe').query_db(query, datos)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM misiones WHERE id = %(id)s;"
        resultados = connectToMySQL('VoluntaMe').query_db(query,data)

        if resultados:
            return cls(resultados[0])

        return None
