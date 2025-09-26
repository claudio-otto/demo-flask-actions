# app.py
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import numpy as np

# Inicializar la aplicación Flask
app = Flask(__name__)

# --- Carga de datos y entrenamiento del modelo ---
# Usamos el famoso dataset 'iris'
iris = load_iris()
X = iris.data
y = iris.target

# Creamos un DataFrame para facilidad de uso (opcional)
df = pd.DataFrame(data=X, columns=iris.feature_names)
df['target'] = y

# Entrenar un modelo simple de Regresión Logística
model = LogisticRegression(max_iter=200)
model.fit(X, y)


# --- Definición de Endpoints de la API ---

@app.route('/')
def home():
    return "<h1>API del Modelo Iris</h1><p>Usa el endpoint /predict para hacer predicciones.</p>"


@app.route('/predict', methods=['POST'])
def predict():
    """
    Recibe datos en formato JSON y devuelve la predicción del modelo.
    Ejemplo de JSON:
    {
        "features": [5.1, 3.5, 1.4, 0.2]
    }
    """
    try:
        # Obtener los datos del request
        data = request.get_json(force=True)

        # Extraer las características y convertirlas a un formato adecuado
        features = np.array(data['features']).reshape(1, -1)

        # Realizar la predicción
        prediction_idx = model.predict(features)

        # Obtener el nombre de la especie predicha
        predicted_species = iris.target_names[prediction_idx[0]]

        # Devolver el resultado
        return jsonify({
            'prediction': predicted_species,
            'class_index': int(prediction_idx[0])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # El puerto 8080 es común para aplicaciones en contenedores
    app.run(host='0.0.0.0', port=8080)