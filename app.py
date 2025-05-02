from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'palabra_secreta_por_defecto')

# Categorías de palabras
CATEGORIAS = [
    {"id": 1, "nombre": "Animales de la selva", "descripcion": "Ingresa nombres de animales que viven en la selva"},
    {"id": 2, "nombre": "Palabras que empiezan con A", "descripcion": "Ingresa palabras que comiencen con la letra A"},
    {"id": 3, "nombre": "Ciudades de Europa", "descripcion": "Ingresa nombres de ciudades europeas"},
    {"id": 4, "nombre": "Frutas y verduras", "descripcion": "Ingresa nombres de frutas o verduras"},
    {"id": 5, "nombre": "Países del mundo", "descripcion": "Ingresa nombres de países"}
]

# Función para cargar el ranking
def cargar_ranking():
    if not os.path.exists('ranking.json'):
        with open('ranking.json', 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open('ranking.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Función para guardar ranking
def guardar_ranking(ranking):
    with open('ranking.json', 'w') as f:
        json.dump(ranking, f)

# Función para guardar registro
def guardar_log(usuario, categoria, palabras, puntuacion):
    log_entry = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": usuario,
        "categoria": categoria,
        "palabras": palabras,
        "puntuacion": puntuacion
    }
    
    if not os.path.exists('logs.json'):
        logs = []
    else:
        try:
            with open('logs.json', 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(log_entry)
    
    with open('logs.json', 'w') as f:
        json.dump(logs, f)

@app.route('/')
def index():
    return render_template('index.html', categorias=CATEGORIAS)

@app.route('/juego/<int:categoria_id>')
def juego(categoria_id):
    categoria = next((cat for cat in CATEGORIAS if cat["id"] == categoria_id), None)
    if not categoria:
        return redirect(url_for('index'))
    
    return render_template('juego.html', categoria=categoria)

@app.route('/guardar_resultado', methods=['POST'])
def guardar_resultado():
    datos = request.json
    usuario = datos.get('usuario', 'Anónimo')
    categoria_id = datos.get('categoria_id')
    palabras = datos.get('palabras', [])
    puntuacion = len(palabras)
    
    categoria = next((cat for cat in CATEGORIAS if cat["id"] == categoria_id), None)
    if not categoria:
        return jsonify({"error": "Categoría no válida"}), 400
    
    # Guardar en ranking
    ranking = cargar_ranking()
    nuevo_entry = {
        "usuario": usuario,
        "categoria": categoria["nombre"],
        "puntuacion": puntuacion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ranking.append(nuevo_entry)
    
    # Ordenar por puntuación (mayor a menor)
    ranking = sorted(ranking, key=lambda x: x["puntuacion"], reverse=True)
    guardar_ranking(ranking)
    
    # Guardar en log
    guardar_log(usuario, categoria["nombre"], palabras, puntuacion)
    
    return jsonify({"success": True, "posicion": ranking.index(nuevo_entry) + 1})

@app.route('/ranking')
def ranking():
    ranking_data = cargar_ranking()
    return render_template('ranking.html', ranking=ranking_data)

@app.route('/get_random_category')
def get_random_category():
    categoria = random.choice(CATEGORIAS)
    return jsonify(categoria)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 