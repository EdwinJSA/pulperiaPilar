from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pyodbc

app = Flask(__name__)

db = sessionmaker(bind=create_engine('sqlite:///database.db'))()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credito')
def credito():
    return render_template('credito.html')

@app.route('/actCredito')
def actCredito():
    return render_template('actCredito.html')

@app.route('/contado')
def contado():
    return render_template('contado.html')

@app.route('/abonarCredito')
def abonarCredito():
    return render_template('abonarCredito.html')
@app.route('/agregarCliente', methods=['POST', 'GET'])
def agregarCliente():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            celular = request.form['celular']

            # Insertar en la base de datos
            query_insert = text("INSERT INTO Cliente (nombres, apellidos, telefono) VALUES (:nombre, :apellido, :celular)")
            db.execute(query_insert, {'nombre': nombre, 'apellido': apellido, 'celular': celular})
            db.commit()

            # Obtener el último cliente agregado
            query_select = text("SELECT * FROM Cliente ORDER BY id DESC LIMIT 1")
            result = db.execute(query_select).fetchone()  # Trae solo una fila como diccionario

            # Mostrar datos del cliente agregado
            return render_template('agregarCliente.html', boucher=True, datos=result)

        except Exception as e:
            print("Error al agregar cliente:", e)
            return render_template('agregarCliente.html', boucher=False, error="Error al guardar el cliente.")
    else:
        return render_template('agregarCliente.html')


@app.route('/productos')
def productos():
    try:
        query = text("SELECT * FROM Producto")
        result = db.execute(query)
        productos = result.fetchall()
        return render_template('productos.html', productos=productos)
    except Exception as e:
        traceback.print_exc()
    return render_template('productos.html')

@app.route('/compras')
def compras():        
    return render_template('compras.html')

@app.route('/verCredito')
def verCredito():
    return render_template('verCredito.html')

@app.route('/guardarVenta', methods=['POST'])
def guardar_producto():
    try:
        data = json.loads(request.data)
        print("====================================")
        total = float(data['total'])
        print(total)
        # print(data['productos'])
        query = text("INSERT INTO Contado (total) VALUES (:total)")
        db.execute(query, {'total': total})
        db.commit()
        
        query = text("SELECT id FROM Contado ORDER BY id DESC LIMIT 1")
        result = db.execute(query)
        id_venta = result.fetchone()[0]
        print(id_venta)
        producto = data['productos'][0]
        print(producto.keys())

        #dict_keys(['name', 'quantity', 'price'])
        for producto in data['productos']:
            query = text("INSERT INTO DetalleContado(cantidad, codigo_producto, id_contado) VALUES (:cantidad, :codigo_producto, :id_contado)")
            db.execute(query, {'cantidad': producto['quantity'], 'codigo_producto': producto['name'], 'id_contado': id_venta})
            db.commit()


        return jsonify({'message': 'Producto guardado correctamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/actualizar_producto', methods=['POST'])
def editar_producto():
    try:
        data = json.loads(request.data)
        print(data.keys())
        codigo = data['codigo']
        nombre = data['nombre']
        precio_unitario = data['precio']
        cantidad = data['cantidad']
        categoria = data['categoria']
        descripcion = data['descripcion']
        
        print(codigo, nombre, precio_unitario, cantidad, categoria, descripcion)

        query = text("UPDATE Producto SET nombre = :nombre, precio_unitario = :precio_unitario, cantidad = :cantidad, categoria = :categoria, descripcion = :descripcion WHERE codigo = :codigo")
        db.execute(query, {'codigo': codigo, 'nombre': nombre, 'precio_unitario': precio_unitario, 'cantidad': cantidad, 'categoria': categoria, 'descripcion': descripcion})
        db.commit()
        return jsonify({'message': 'Producto actualizado correctamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
@app.route('/eliminar_producto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        print(f"Eliminando producto con ID: {id}")
        query = text("DELETE FROM Producto WHERE codigo = :id")
        db.execute(query, {'id': id})
        db.commit()
        return jsonify({'message': 'Producto eliminado correctamente'}), 200
    except Exception as e:
        print(f"Error al eliminar: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/cargarClientes')
def cargarClientes():
    busqueda = request.args.get('busqueda', '')  # Obtener el parámetro de búsqueda
    query = text("SELECT * FROM Cliente WHERE nombres LIKE :busqueda")  # Corregir la consulta
    result = db.execute(query, {'busqueda': f'%{busqueda}%'})  # Incluir comodines
    clientes = [dict(row) for row in result.fetchall()]  # Convertir resultados a diccionario
    return jsonify(clientes)  # Devolver en formato JSON


if __name__ == '__main__':
    app.run(debug=True)
