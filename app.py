from flask import Flask, render_template, jsonify, request
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

@app.route('/productos')
def productos():
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


if __name__ == '__main__':
    app.run(debug=True)
