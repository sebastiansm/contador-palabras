from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'palabra_secreta_por_defecto')

# Categorías de palabras
# Letras con mayor cantidad de palabras en español
LETRAS_PRODUCTIVAS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'V']

def generar_categoria_aleatoria():
    letra = random.choice(LETRAS_PRODUCTIVAS)
    return {
        "nombre": f"Palabras que empiezan con {letra}",
        "descripcion": f"Ingresa palabras que comiencen con la letra {letra}"
    }

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
    ranking = cargar_ranking()
    return render_template('index.html', ranking=ranking)

@app.route('/juego/<categoria>')
def juego(categoria):
    if categoria == 'random':
        categoria = generar_categoria_aleatoria()
    else:
        return redirect(url_for('index'))
    
    return render_template('juego.html', categoria=categoria['nombre'])

@app.route('/guardar_puntuacion', methods=['POST'])
def guardar_puntuacion():
    datos = request.json
    nombre = datos.get('nombre')
    puntuacion = datos.get('puntuacion')
    categoria = datos.get('categoria')
    
    if not nombre or not puntuacion or not categoria:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Guardar en ranking
    ranking = cargar_ranking()
    nuevo_entry = {
        "nombre": nombre,
        "categoria": categoria,
        "puntuacion": puntuacion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ranking.append(nuevo_entry)
    
    # Ordenar por puntuación (mayor a menor)
    ranking = sorted(ranking, key=lambda x: x["puntuacion"], reverse=True)
    guardar_ranking(ranking)
    
    return jsonify({"success": True, "ranking": ranking})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 