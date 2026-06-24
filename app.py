from flask import Flask, render_template, request
import json
import pandas as pd
import joblib
from model_utils import ColumnIndexSelector

app = Flask(__name__)

pipeline = joblib.load("modelo_sgemm_pipeline.joblib")
with open("metadata_sgemm.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "ok",
        "message": "Servicio activo",
        "model": metadata.get("model_name", "DecisionTreeRegressor")
    }, 200


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    values = {}

    if request.method == "POST":
        try:
            row = {}
            for col in metadata["input_columns"]:
                raw_value = request.form.get(col, "").strip()
                values[col] = raw_value

                if raw_value == "":
                    raise ValueError(f"Falta capturar el campo {col}.")

                field_info = metadata["fields"][col]
                if field_info["kind"] == "categorical":
                    allowed = [str(v) for v in field_info["options"]]
                    if raw_value not in allowed:
                        raise ValueError(f"El campo {col} debe ser uno de estos valores: {allowed}.")
                    row[col] = int(raw_value)
                else:
                    value = float(raw_value)
                    min_value = field_info.get("min")
                    max_value = field_info.get("max")
                    if min_value is not None and max_value is not None:
                        if value < min_value or value > max_value:
                            raise ValueError(
                                f"El campo {col} debe estar entre {min_value} y {max_value}."
                            )
                    row[col] = value

            X_input = pd.DataFrame([row], columns=metadata["input_columns"])
            prediction = float(pipeline.predict(X_input)[0])

        except Exception as exc:
            error = str(exc)

    return render_template(
        "index.html",
        metadata=metadata,
        prediction=prediction,
        error=error,
        values=values
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
