from pathlib import Path
import os

import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "plantcare_model.pkl"

model = joblib.load(MODEL_PATH)

REQUIRED_FIELDS = [
    "tipo_planta",
    "dias_sem_rega",
    "frequencia_ideal_rega",
    "umidade_solo",
    "luz_recebida",
    "temperatura_media_c",
    "folhas_amareladas",
    "folhas_murchas",
    "manchas_folhas",
    "crescimento_lento",
    "solo_compactado",
]

RECOMMENDATIONS = {
    "saudavel": "Manter a rotina atual de cuidados.",
    "falta_agua": "Regue a planta e acompanhe a recuperação nas próximas 24 horas.",
    "excesso_agua": "Reduza a frequência de rega e verifique a drenagem do vaso.",
    "pouca_luz": "Mova a planta para um local com mais luz indireta.",
    "excesso_sol": "Mova a planta para um local com menos exposição solar direta.",
    "possivel_praga": "Verifique folhas e caule em busca de sinais de pragas.",
    "necessita_adubo": "Considere adubar a planta conforme a necessidade da espécie.",
}

RISK_LEVELS = {
    "saudavel": "baixo",
    "falta_agua": "medio",
    "excesso_agua": "alto",
    "pouca_luz": "medio",
    "excesso_sol": "medio",
    "possivel_praga": "alto",
    "necessita_adubo": "medio",
}


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "plantcare-ai-api",
        "status": "running",
        "endpoints": ["/health", "/predict"]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "plantcare-ai-api"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    try:
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)[0]

        response = {
            "diagnostico": prediction,
            "nivel_risco": RISK_LEVELS.get(prediction, "indefinido"),
            "recomendacao": RECOMMENDATIONS.get(
                prediction,
                "Não foi possível gerar uma recomendação para este diagnóstico."
            )
        }

        if hasattr(model.named_steps["model"], "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            classes = model.named_steps["model"].classes_

            response["confianca"] = round(float(max(probabilities)), 4)
            response["probabilidades"] = {
                str(class_name): round(float(prob), 4)
                for class_name, prob in zip(classes, probabilities)
            }

        return jsonify(response)

    except Exception as error:
        return jsonify({
            "error": "Prediction failed",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG") == "1"
    )