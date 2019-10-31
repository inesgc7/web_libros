from flask import Flask
from flask import request
from flask import make_response
from flask import url_for
from flask import jsonify
from flask import redirect
import sqlite3

app = Flask(__name__)

#Verificar si el libro ya existe en el sistema
def existeLibro(codigo_libro):
    conn = sqlite3.connect('libros.db')
    c = conn.cursor()
    codigo_libro = (codigo_libro,)
    c.execute('SELECT * FROM fichero WHERE codigo=?', codigo_libro)
    respuesta = c.fetchone()
    c.close()
    conn.close()
    if respuesta:
        return True
    else:
        return False


@app.route("/hola")
def hola():
    return "Hola mundo!"

@app.route("/libro", methods=['POST', 'GET', 'DELETE'])
def procesarLibro():
    url_for('static', filename='libros.html')
    url_for('static', filename='bootstrap.css')
    url_for('static', filename='jquery.js')

    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        fecha_publicacion = request.form['fecha_publicacion']
        autor = request.form['autor']
        ubicacion = request.form['ubicacion']

        if existeLibro(codigo):
            #ACTUALIZAR DATOS DEL LIBRO
            conn = sqlite3.connect('libros.db')
            c = conn.cursor()
            c.execute("""UPDATE fichero SET nombre='%s', fecha_publicacion='%s', autor='%s', ubicacion='%s' WHERE codigo='%s'""" % (nombre, fecha_publicacion, autor, ubicacion, codigo))
            conn.commit()
        else:    
            #GUARDAR NUEVO LIBRO
            conn = sqlite3.connect('libros.db')
            c = conn.cursor()
            c.execute("""INSERT INTO fichero VALUES (%s, '%s', '%s', '%s', '%s')""" % (codigo, nombre, fecha_publicacion, autor, ubicacion))
            conn.commit()
        c.close()
        conn.close()

        return redirect("http://127.0.0.1:8080/static/libros.html", code=302) 


    if request.method == 'GET':
        conn = sqlite3.connect('libros.db')
        c = conn.cursor()
        
        if 'codigo' in request.args:
            codigo = request.args.get('codigo')
            c.execute("""SELECT * FROM fichero WHERE codigo = %s""" % codigo)
        elif 'autor' in request.args:
            autor = request.args.get('autor')
            c.execute("""SELECT * FROM fichero WHERE autor = %s""" % autor)
        else:
            c.execute("""SELECT * FROM fichero""")

        libros = c.fetchall()

        respuesta = []
        for libro in libros:
            # libro es un diccionario en python
            libro = {'codigo':libro[0],
                    'nombre':libro[1],
                    'fecha_publicacion':libro[2],
                    'autor':libro[3],
                    'ubicacion':libro[4]}
            respuesta.append(libro)
        return jsonify({"data":respuesta})


    #Borra un libro del sistema
    if request.method == 'DELETE':
        codigo = request.args.get('codigo')
        conn = sqlite3.connect('libros.db')
        c = conn.cursor()
        c.execute("""DELETE FROM fichero WHERE codigo = %s""" % codigo)
        conn.commit()
        c.close()
        conn.close()
        return make_response(jsonify({'respuesta':'ok'}), 200)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
