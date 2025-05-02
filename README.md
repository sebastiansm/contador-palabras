# Juego de Contador de Palabras

Una aplicación web que permite a los usuarios jugar a escribir la mayor cantidad de palabras posibles en 60 segundos según una categoría dada. Después del juego, los usuarios pueden verificar sus palabras, guardar resultados y ver un ranking.

## Características

- Múltiples categorías predefinidas
- Temporizador de 60 segundos
- Verificación de palabras después del juego
- Ranking de mejores puntuaciones
- Registro de partidas históricas

## Requisitos

- Python 3.7 o superior
- Flask
- Gunicorn (para producción)

## Instalación local

1. Clona este repositorio:
   ```
   git clone <url-del-repositorio>
   cd contador-palabras
   ```

2. Crea un entorno virtual:
   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

5. Ejecuta la aplicación:
   ```
   python app.py
   ```

6. Accede a la aplicación en tu navegador:
   ```
   http://localhost:5000
   ```

## Despliegue en Render.com (Gratuito)

Esta aplicación está diseñada para ser fácilmente desplegada en Render.com, que ofrece un plan gratuito adecuado para aplicaciones con bajo tráfico.

### Pasos para el despliegue

1. Crea una cuenta en [Render.com](https://render.com) si no tienes una.

2. En el Dashboard de Render, haz clic en "New" y selecciona "Web Service".

3. Conecta tu repositorio de GitHub o GitLab donde hayas subido este código.

4. Configura el servicio:
   - **Name**: Elige un nombre para tu aplicación
   - **Environment**: Python
   - **Region**: Selecciona la región más cercana a tus usuarios
   - **Branch**: main (o la rama que uses)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

5. Haz clic en "Create Web Service".

6. Render automáticamente desplegará tu aplicación. Una vez completado, podrás acceder a tu aplicación a través de la URL proporcionada por Render.

### Variables de entorno recomendadas para Render

Puedes configurar estas variables de entorno en la sección "Environment" de tu servicio en Render:

- `SECRET_KEY`: Una clave secreta para la sesión de Flask (genera una fuerte)
- `PORT`: Render lo configura automáticamente
- `PYTHON_VERSION`: 3.9 (o la versión que prefieras)

## Estructura del proyecto

```
contador-palabras/
├── app.py                # Aplicación principal de Flask
├── requirements.txt      # Dependencias del proyecto
├── README.md             # Documentación
├── ranking.json          # Archivo para almacenar el ranking
├── logs.json             # Archivo para almacenar el historial
├── static/               # Archivos estáticos
│   └── css/
│       └── style.css     # Estilos CSS
└── templates/            # Plantillas HTML
    ├── index.html        # Página principal
    ├── juego.html        # Página del juego
    └── ranking.html      # Página de ranking
```

## Licencia

MIT 