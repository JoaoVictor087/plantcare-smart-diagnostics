from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "plantcare_model.pkl"

model = joblib.load(MODEL_PATH)

RECOMMENDATIONS = {
    "saudavel": "Manter a rotina atual de cuidados.",
    "falta_agua": "Regue a planta e acompanhe a recuperação nas próximas 24 horas.",
    "excesso_agua": "Reduza a frequência de rega e verifique a drenagem do vaso.",
    "pouca_luz": "Mova a planta para um local com mais luz indireta.",
    "excesso_sol": "Mova a planta para um local com menos exposição solar direta.",
    "possivel_praga": "Verifique folhas e caule em busca de sinais de pragas.",
    "necessita_adubo": "Considere adubar a planta conforme a necessidade da espécie."
}

RISK_LEVELS = {
    "saudavel": "baixo",
    "falta_agua": "medio",
    "excesso_agua": "alto",
    "pouca_luz": "medio",
    "excesso_sol": "medio",
    "possivel_praga": "alto",
    "necessita_adubo": "medio"
}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "plantcare-ai-api"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body is required"
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

            confidence = max(probabilities)
            response["confianca"] = round(float(confidence), 4)

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
    app.run(debug=True, host="0.0.0.0", port=5000)