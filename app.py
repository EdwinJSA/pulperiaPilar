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
    
    nombreProductos = []
    
    query = text("SELECT nombres, apellidos, empresa FROM Proveedor")
    resultados = db.execute(query).fetchall()
    
    proveedores = [{"nombre": fila[0], "apellido": fila[1], "empresa": fila[2]} for fila in resultados]
    
    query = text("SELECT codigo,nombre, descripcion, precio_unitario FROM Producto")
    produc = db.execute(query).fetchall()
    
    print("====================================")
    for i in produc:
        nombreProductos.append(f"{i[0]}-{i[1]}-{i[2]}-C${i[3]}")    
    
    return render_template('compras.html', proveedores=proveedores, producto=json.dumps(nombreProductos))

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
        data = json.loads(request.data)
        #recuperamos el monto pendiente y el total
        pendiente = 0
        
        #AGREGAMOS UN NUEVO CREDITO
        query = text("INSERT INTO Credito(monto_pagado, monto_pendiente, total, id_cliente) VALUES (:monto_pagado, :monto_pendiente, :total, :id_cliente)")
        db.execute(query, {'monto_pagado': 0, 'monto_pendiente': 0, 'total': 0, 'id_cliente': data['cliente']})
        db.commit()
        
        #recuperamos el id del ultimo credito
        query = text("SELECT id FROM Credito ORDER BY id DESC LIMIT 1")
        result = db.execute(query)
        id_credito = result.fetchone()[0]
        
        #agregamos los detalles del credito
        for producto in data['productos']:
            codigoProducto = obtener_codigo(producto['producto'])
            query = text("INSERT INTO DetalleCredito(cantidad, codigo_producto, id_credito) VALUES (:cantidad, :codigo_producto, :id_credito)")
            db.execute(query, {'cantidad': producto['cantidad'], 'codigo_producto': codigoProducto, 'id_credito': id_credito})
            db.commit()
            
            #recuperamos el precio unitario del producto
            query = text("SELECT precio_unitario FROM Producto WHERE codigo = :codigo")
            result = db.execute(query, {'codigo': codigoProducto})
            precio_unitario = result.fetchone()[0]
            pendiente += (int(producto['cantidad']) * float(precio_unitario))

        #actualizamos el total del credito
        query = text("UPDATE Credito SET monto_pendiente = :monto_pendiente, total = :total WHERE id = :id")
        db.execute(query, {'monto_pendiente': pendiente, 'total': pendiente, 'id': id_credito})
        db.commit()
        
        return jsonify({'message': 'Credito guardado correctamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/proveedores')
def proveedores():
    try:
        query = text("SELECT * FROM Proveedor")
        result = db.execute(query)
        proveedores = result.fetchall()
        # Convertir los resultados en una lista de diccionarios
        proveedores = [dict(proveedor) for proveedor in proveedores]
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

@app.route('/registrar_compra', methods=['POST'])
def registrar_compra():
    try:
        # Datos enviados desde el frontend
        data = request.json
        fecha = data.get('fecha')
        id_proveedor = data.get('id_proveedor')
        productos = data.get('productos')  # Lista de {codigo_producto, cantidad}

        # Validación de datos incompletos
        if not fecha or not id_proveedor or not productos:
            return jsonify({'error': 'Datos incompletos'}), 400

        # Verificar si `id_proveedor` es un nombre en lugar de un ID y obtener el ID correspondiente
        if isinstance(id_proveedor, str):  # Asumiendo que si es string, es el nombre
            query = text("SELECT id FROM Proveedor WHERE nombres = :nombres")
            result = db.execute(query, {'nombres': id_proveedor}).fetchone()
            if result:
                id_proveedor = result[0]  # Reemplaza `id_proveedor` con el ID
            else:
                return jsonify({'error': 'Proveedor no encontrado'}), 400

        # Calcular el total de la compra
        total = 0
        for producto in productos:
            query = text("SELECT precio_unitario FROM Producto WHERE codigo = :codigo")
            result = db.execute(query, {'codigo': producto['codigo_producto']}).fetchone()
            if not result:
                return jsonify({'error': f"Producto con código {producto['codigo_producto']} no encontrado"}), 400

            precio_unitario = result[0]
            total += precio_unitario * producto['cantidad']

        # Insertar la compra en la tabla Compra
        query = text("""
            INSERT INTO Compra (fecha, total, id_proveedor)
            VALUES (:fecha, :total, :id_proveedor)
            RETURNING id
        """)
        compra_id = db.execute(query, {'fecha': fecha, 'total': total, 'id_proveedor': id_proveedor}).fetchone()[0]

        # Insertar detalles de la compra en DetalleCompra
        for producto in productos:
            query = text("""
                INSERT INTO DetalleCompra (cantidad, codigo_producto, id_compra)
                VALUES (:cantidad, :codigo_producto, :id_compra)
            """)
            db.execute(query, {
                'cantidad': producto['cantidad'],
                'codigo_producto': producto['codigo_producto'],
                'id_compra': compra_id
            })

            # Actualizar la cantidad del producto en la tabla Producto
            query = text("""
                UPDATE Producto
                SET cantidad = cantidad + :cantidad
                WHERE codigo = :codigo_producto
            """)
            db.execute(query, {
                'cantidad': producto['cantidad'],
                'codigo_producto': producto['codigo_producto']
            })

        db.commit()  # Confirmar las transacciones

        return jsonify({'message': 'Compra registrada exitosamente', 'compra_id': compra_id}), 201

    except Exception as e:
        db.rollback()  # Revertir cambios en caso de error
        return jsonify({'error': str(e)}), 500
    
@app.route('/buscar_proveedores', methods=['GET'])
def buscar_proveedores():
    query = request.args.get('query', '')
    try:
        query_sql = text("SELECT * FROM Proveedor WHERE nombres LIKE :query OR apellidos LIKE :query OR empresa LIKE :query")
        result = db.execute(query_sql, {'query': f'%{query}%'})
        proveedores = result.fetchall()
        proveedores = [dict(proveedor) for proveedor in proveedores]  # Convertir a diccionario
        return jsonify({'proveedores': proveedores})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/agregar_vendedor', methods=['POST'])
def agregar_vendedor():
    try:
        data = request.get_json()
        nombres = data['nombres']
        apellidos = data['apellidos']
        empresa = data['empresa']
        telefono = data['telefono']

        query = text("""
            INSERT INTO Proveedor (nombres, apellidos, empresa, telefono)
            VALUES (:nombres, :apellidos, :empresa, :telefono)
        """)
        db.execute(query, {'nombres': nombres, 'apellidos': apellidos, 'empresa': empresa, 'telefono': telefono})
        db.commit()
        return jsonify({'message': 'Vendedor agregado correctamente'}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Ruta para editar un vendedor
@app.route('/editar_vendedor/<int:id>', methods=['PUT'])
def editar_vendedor(id):
    try:
        data = request.get_json()
        nombres = data['nombres']
        apellidos = data['apellidos']
        empresa = data['empresa']
        telefono = data['telefono']

        query = text("""
            UPDATE Proveedor
            SET nombres = :nombres, apellidos = :apellidos, empresa = :empresa, telefono = :telefono
            WHERE id = :id
        """)
        db.execute(query, {'id': id, 'nombres': nombres, 'apellidos': apellidos, 'empresa': empresa, 'telefono': telefono})
        db.commit()
        return jsonify({'message': 'Vendedor actualizado correctamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un vendedor
@app.route('/eliminar_vendedor/<int:id>', methods=['DELETE'])
def eliminar_vendedor(id):
    try:
        query = text("DELETE FROM Proveedor WHERE id = :id")
        db.execute(query, {'id': id})
        db.commit()
        return jsonify({'message': 'Vendedor eliminado correctamente'}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
@app.route('/creditoCliente', methods=['POST'])
def creditoCliente():
    try:
        data = request.json
        cliente = data['cliente']
        print(f"Obteniendo credito del cliente: {cliente}")
        query = text("""
            SELECT 
                Credito.id AS id_credito,
                Credito.fecha_credito,
                Credito.monto_pendiente
            FROM 
                Credito
            INNER JOIN 
                Cliente ON Credito.id_cliente = Cliente.id
            WHERE 
                Cliente.id = :id_cliente;
        """)
        
        # Ejecutar la consulta
        result = db.execute(query, {'id_cliente': cliente})
        
        # Convertir los resultados a una lista de diccionarios
        credito = [
            {
                'id_credito': row.id_credito,
                'fecha_credito': row.fecha_credito,
                'monto_pendiente': row.monto_pendiente
            } for row in result
        ]
        
        # Retornar los resultados en formato JSON
        return jsonify(credito), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        
@app.route('/abonarCreditoCliente', methods=['POST'])
def abonarCreditoCliente():
    if request.method == 'POST':
        data = request.json
        print(data.keys())
        id_credito = data['credito_id']
        monto_abonado = data['monto_abonar']
        
        query = text("""
            UPDATE Credito
            SET monto_pendiente = monto_pendiente - :monto_abonado
            WHERE id = :id_credito
        """)
        db.execute(query, {'monto_abonado': monto_abonado, 'id_credito': id_credito})
        db.commit()
        
        query = text("""
            UPDATE Credito
            SET monto_pagado = monto_pagado + :monto_abonado
            WHERE id = :id_credito
        """)
        db.execute(query, {'monto_abonado': monto_abonado, 'id_credito': id_credito})
        db.commit()
        
        return jsonify({'message': 'Credito abonado correctamente'}), 200
    
    return jsonify({'error': 'Metodo no permitido'}), 405


@app.route('/verProductosCredito', methods=['POST'])
def verProductosCredito():
    if request.method == 'POST':
        data = request.json
        credito_id = data['credito_id']
        print("CREDITO ID:", credito_id)
        
        query = text("""
            SELECT p.nombre
            FROM DetalleCredito dc
            JOIN Producto p ON dc.codigo_producto = p.codigo
            WHERE dc.id_credito = :id_credito;
        """)
        
        # Ejecutar la consulta y obtener los resultados
        result = db.execute(query, {'id_credito': credito_id}).fetchall()
        
        # Convertir los resultados en una lista de nombres
        productos = [row[0] for row in result]  # row[0] porque seleccionamos solo `p.nombre`
        print(productos)
        
        # Devolver los productos como JSON
        return jsonify({'productos': productos}), 200
    
    return jsonify({'error': 'Metodo no permitido'}), 405


if __name__ == '__main__':
    app.run(debug=True)
