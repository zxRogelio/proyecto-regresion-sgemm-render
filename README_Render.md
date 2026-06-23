# Proyecto Flask - Predicción SGEMM GPU

## Archivos principales
- app.py: aplicación Flask.
- modelo_sgemm_pipeline.joblib: pipeline entrenado.
- metadata_sgemm.json: columnas, descripciones, opciones y ejemplos para el formulario.
- filas_recomendadas_formulario.csv: filas reales recomendadas para probar.
- templates/index.html: formulario web.
- static/style.css: estilos.
- requirements.txt: dependencias.
- runtime.txt: versión de Python recomendada para Render.
- Procfile: comando de arranque.

## Ejecución local
```bash
pip install -r requirements.txt
python app.py
```

## Configuración en Render
- Build Command:
```bash
pip install -r requirements.txt
```

- Start Command:
```bash
gunicorn app:app
```

Cuando Render genere la URL pública, copiarla en `URL_Render.txt`, en la portada del PDF y en la libreta.
