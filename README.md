# BookShare Frontend Python

Aplicación web BookShare construida con Python y Flask. La interfaz se abre desde el navegador, usa datos mock y no realiza conexiones a base de datos ni API externa.

## Ejecutar

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Después abre `http://127.0.0.1:5000`.

## Preparado para la API

La integración mock está centralizada en `app.py` y respeta la base `/api/v1` definida en el contrato. Cuando el Gateway esté disponible, estos endpoints pueden convertirse en proxy o reemplazarse por llamadas al backend real.

Rutas actuales: `/`, `/catalog`, `/requests`, `/loans`, `/chat` y `/profile`.
