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
        query = """
        INSERT INTO misiones (nombre, fecha, voluntarios_necesarios, descripcion, usuarios_id)
        VALUES (%(nombre)s, %(fecha)s, %(voluntarios_necesarios)s, %(descripcion)s, %(usuarios_id)s)
        """
        return connectToMySQL("VoluntaMe").query_db(query, data)

    #Metodos para ver registros
    @classmethod
    def get_all(cls):
        query = """
            SELECT misiones.*, misiones.usuarios_id AS usuario_id,
                CONCAT(usuarios.nombre,' ') AS usuario_nombre
            FROM misiones
            JOIN usuarios ON misiones.usuarios_id = usuarios.id
        """


        results = connectToMySQL("VoluntaMe").query_db(query)

        return [cls(row) for row in results]

    @classmethod
    def update(cls, data):
        query="""UPDATE misiones SET 
        nombre=%(nombre)s,
        fecha=%(fecha)s,
        voluntarios_necesarios=%(voluntarios_necesarios)s,
        descripcion=%(descripcion)s,
        updated_at = NOW() WHERE id=%(id)s"""
        
        return connectToMySQL('VoluntaMe').query_db(query, data)    

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM misiones WHERE id = %(id)s;"
        resultados = connectToMySQL('VoluntaMe').query_db(query,data)

        if resultados:
            return cls(resultados[0])

        return None
