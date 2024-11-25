from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pyodbc, re

app = Flask(__name__)

db = sessionmaker(bind=create_engine('sqlite:///database.db'))()


def obtener_codigo(texto):
    # Busca todo lo que está antes del primer guion
    match = re.match(r"^[^-]+", texto)
    if match:
        return match.group(0)
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/credito')
def credito():
    nombreProductos = []
    
    query = text("SELECT * FROM Cliente")
    clientes = db.execute(query).fetchall()
    
    query = text("SELECT codigo,nombre, descripcion, precio_unitario FROM Producto")
    produc = db.execute(query).fetchall()
    
    print("====================================")
    for i in produc:
        nombreProductos.append(f"{i[0]}-{i[1]}-{i[2]}-C${i[3]}")    
    
    return render_template('credito.html', clientes=clientes, producto=json.dumps(nombreProductos))

@app.route('/contado')
def contado():
    nombreProductos = []
    
    # Query para obtener el código, nombre y precio_unitario del producto
    query = text("SELECT codigo, nombre, precio_unitario FROM Producto")
    produc = db.execute(query).fetchall()
    
    # Formatear cada producto en una cadena específica para el autocompletado
    for i in produc:
        nombreProductos.append(f"{i[0]}-{i[1]}-C${i[2]}")  # Código-Nombre-Precio

    return render_template('contado.html', producto=json.dumps(nombreProductos))

@app.route('/abonarCredito')
def abonarCredito():
    query = text("SELECT * FROM Cliente")
    clientes = db.execute(query).fetchall()
    return render_template("abonarCredito.html", clientes=clientes)

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
        print("NO ENTRO AL IF")
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

@app.route('/danado')
def danado():        
    return render_template('danado.html')


@app.route('/verCredito')
def verCredito():
    try:
        # Consulta corregida
        query = text("""
            SELECT cliente.id, cliente.nombres, cliente.apellidos, cliente.telefono,
                credito.fecha_credito, credito.monto_pendiente, credito.total
            FROM cliente
            JOIN credito ON cliente.id = credito.id_cliente
        """)
        result = db.execute(query)
        verCredito = result.fetchall()
        return render_template('verCredito.html', verCredito=verCredito)
    except Exception as e:
        traceback.print_exc()
        return render_template('verCredito.html')

@app.route('/clientes')
def clientes():
    try:
        query = text("SELECT * FROM Cliente")
        result = db.execute(query)
        clientes = result.fetchall()
        return render_template('clientes.html', clientes=clientes)
    except Exception as e:
        traceback.print_exc()
        return render_template('clientes.html')


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
#articulo

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


@app.route('/cargarClientes', methods=['POST', 'GET'])
def cargarClientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        
        query = text("SELECT * FROM Cliente WHERE nombres = :nombres")
        result = db.execute(query, {'nombres': nombre})
        clientes = result.fetchall()
        print(clientes)
        return render_template('credito.html', clientes=clientes)
    
@app.route('/guardarCredito', methods=['POST'])
def guardarCredito():
    try:
        data = request.get_json()
        print(data)
        cliente = data['cliente']
        productos = data['productos']
        
        # Iniciamos la transacción
        db.begin()

        # Creamos un nuevo crédito al cliente
        query = text("INSERT INTO Credito (id_cliente) VALUES (:id_cliente)")
        db.execute(query, {'id_cliente': cliente})
        
        # Obtenemos el id del crédito
        query = text("SELECT id FROM Credito ORDER BY id DESC LIMIT 1")
        result = db.execute(query)
        id_credito = result.fetchone()[0]
        print(f"Credito ID: {id_credito}")
        
        # Validar que hay suficiente stock
        for i in productos:
            producto = obtener_codigo(i['producto'])
            cantidad = i['cantidad']
            query = text("SELECT cantidad FROM Producto WHERE codigo = :codigo")
            result = db.execute(query, {'codigo': producto})
            stock = result.fetchone()[0]
            print(f"Producto: {producto}, Stock: {stock}, Cantidad requerida: {cantidad}")
            if stock < cantidad:
                db.rollback()  # Rollback en caso de error
                return jsonify({'error': f'No hay suficiente stock para el producto {producto}'}), 400
        
        # Insertamos los detalles del crédito
        for i in productos:
            producto = obtener_codigo(i['producto'])
            cantidad = i['cantidad']
            
            # Insertamos el detalle del crédito
            query = text("INSERT INTO DetalleCredito (cantidad, codigo_producto, id_credito) VALUES (:cantidad, :codigo_producto, :id_credito)")
            db.execute(query, {'cantidad': cantidad, 'codigo_producto': producto, 'id_credito': id_credito})
        
        # Commit después de insertar todos los detalles
        db.commit()
        
        # Total a Pagar
        query = text("""
                    SELECT SUM(dc.cantidad * p.precio_unitario) AS total_a_pagar
                    FROM DetalleCredito dc
                    JOIN Producto p ON dc.codigo_producto = p.codigo
                    JOIN Credito c ON dc.id_credito = c.id
                    WHERE c.id = :id_credito;
                    """)
        result = db.execute(query, {'id_credito': id_credito})
        total_a_pagar = result.fetchone()[0]
        print(f"Total a pagar: {total_a_pagar}")
        
        # Actualizamos el total del crédito
        query = text("SELECT monto_pagado FROM Credito WHERE id = :id_credito")
        result = db.execute(query, {'id_credito': id_credito})
        monto_pagado = result.fetchone()[0]
        
        query = text("UPDATE Credito SET total = :total_a_pagar, monto_pendiente = :pendiente WHERE id = :id_credito")
        db.execute(query, {'total_a_pagar': total_a_pagar, 'pendiente': total_a_pagar - monto_pagado, 'id_credito': id_credito})
        
        # Actualizamos la cantidad de productos en stock
        for i in productos:
            producto = obtener_codigo(i['producto'])
            cantidad = i['cantidad']
            query = text("SELECT cantidad FROM Producto WHERE codigo = :codigo")
            result = db.execute(query, {'codigo': producto})
            stock = result.fetchone()[0]
            
            query = text("UPDATE Producto SET cantidad = :cantidad WHERE codigo = :codigo")
            db.execute(query, {'cantidad': stock - cantidad, 'codigo': producto})
        
        # Commit final
        db.commit()
        
        return jsonify({'message': 'Credito guardado correctamente'}), 200
    except Exception as e:
        db.rollback()  # Aseguramos que todo se revierta en caso de error
        return jsonify({'error': str(e)}), 500


@app.route('/proveedores')
def proveedores():
    try:
        query = text("SELECT * FROM Proveedor")
        result = db.execute(query)
        proveedores = result.fetchall()
        return render_template('proveedores.html', proveedores=proveedores)
    except Exception as e:
        traceback.print_exc()
    return render_template('proveedores.html')


@app.route('/consumido')
def consumido():
    nombreProductos = []
    
    # Query para obtener el código, nombre y precio_unitario del producto
    query = text("SELECT codigo, nombre, precio_unitario FROM Producto")
    produc = db.execute(query).fetchall()
    
    # Formatear cada producto en una cadena específica para el autocompletado
    for i in produc:
        nombreProductos.append(f"{i[0]}-{i[1]}-C${i[2]}")  # Código-Nombre-Precio

    return render_template('consumido.html', producto=json.dumps(nombreProductos))

# Endpoint para guardar el consumo
@app.route('/guardar_consumido', methods=['POST'])
def guardar_consumido():
    try:
        # Obtener los datos enviados en formato JSON
        data = request.get_json()
        fecha_registro = data['fecha_registro']
        productos = data['productos']
        
        # Iniciar la transacción
        db.begin()

        # Crear el nuevo registro en la tabla `Consumido`
        query_consumido = text("INSERT INTO Consumido (fecha_registro, total) VALUES (:fecha_registro, :total)")
        total_consumo = sum([p['precio'] * p['cantidad'] for p in productos])  # Calcular total
        db.execute(query_consumido, {'fecha_registro': fecha_registro, 'total': total_consumo})
        
        # Obtener el ID del consumo recién insertado
        query_consumido = text("INSERT INTO Consumido (fecha_registro, total) VALUES (:fecha_registro, :total) RETURNING id")
        result = db.execute(query_consumido, {'fecha_registro': fecha_registro, 'total': total_consumo})
        id_consumido = result.fetchone()[0]

        
        # Validar el stock de cada producto
        for prod in productos:
            producto_codigo = prod['codigo']
            cantidad = prod['cantidad']
            
            # Consultar el stock actual del producto
            query_stock = text("SELECT cantidad FROM Producto WHERE codigo = :codigo")
            result = db.execute(query_stock, {'codigo': producto_codigo})
            stock = result.fetchone()[0]
            
            # Si no hay suficiente stock, hacer rollback y devolver mensaje de error
            if stock < cantidad:
                db.rollback()  # Deshacer todo si hay error
                return jsonify({'error': f'No hay suficiente stock para el producto {producto_codigo}'}), 400
        
        for prod in productos:
            producto_codigo = prod['codigo']
            cantidad = prod['cantidad']
            
            query_detalle = text("""
                INSERT INTO DetalleConsumido (cantidad, codigo_producto, id_consumido)
                VALUES (:cantidad, :codigo_producto, :id_consumido)
            """)
            db.execute(query_detalle, {'cantidad': cantidad, 'codigo_producto': producto_codigo, 'id_consumido': id_consumido})
        
        db.commit()

        # Actualizar el stock de los productos después del consumo
        for prod in productos:
            producto_codigo = prod['codigo']
            cantidad = prod['cantidad']
            
            # Consultar el stock actual del producto
            query_stock = text("SELECT cantidad FROM Producto WHERE codigo = :codigo")
            result = db.execute(query_stock, {'codigo': producto_codigo})
            stock = result.fetchone()[0]
            
            # Actualizar el stock del producto
            query_update_stock = text("UPDATE Producto SET cantidad = :cantidad WHERE codigo = :codigo")
            db.execute(query_update_stock, {'cantidad': stock - cantidad, 'codigo': producto_codigo})

        db.commit()
        
        return jsonify({'message': 'Consumo guardado correctamente', 'id_consumido': id_consumido}), 200
    
    except Exception as e:
        db.rollback()  
        return jsonify({'error': str(e)}), 500
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        data = request.json
        codigo = data['codigo']
        nombre = data['nombre']
        categoria = data.get('categoria', '')
        descripcion = data.get('descripcion', '')

        # Asigna cantidad y precio_unitario a 0
        cantidad = 0
        precio_unitario = 0

        query = text("""
            INSERT INTO Producto (codigo, nombre, precio_unitario, cantidad, categoria, descripcion)
            VALUES (:codigo, :nombre, :precio_unitario, :cantidad, :categoria, :descripcion)
        """)
        db.execute(query, {
            'codigo': codigo,
            'nombre': nombre,
            'precio_unitario': precio_unitario,
            'cantidad': cantidad,
            'categoria': categoria,
            'descripcion': descripcion
        })
        db.commit()

        return jsonify({'message': 'Producto agregado correctamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)
