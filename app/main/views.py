import io, os, traceback, mimetypes
import numpy as np
import pandas as pd
from app.main import main as app
from pandas.api.types import is_float_dtype
from flask import request, jsonify, send_file, render_template


base_path = os.path.dirname(os.path.abspath(__file__))

FIELDS = ['BR_x', 'BR_y', 'BL_x', 'BL_y', 'TL_x', 'TL_y', 'TR_x', 'TR_y']
df_true = pd.read_csv(os.path.join(base_path, "../static/assets/test.csv"))
y_true = df_true[FIELDS].values.reshape(-1, 4, 2)

@app.route("/", methods=["GET"])
def Index():
    try:
        return render_template("index.html")
    except:
        return jsonify({
            "error_msg": traceback.format_exc()
        })

@app.route('/cs6550', methods=['POST'])
def metric():
    try:
        file = request.files["file"]
        extension = f.filename.split(".")[-1]

        if not file or extension not in app.config["ALLOWED_FILE_EXTENSIONS"]:
            return 'Invalid'

        data = io.BytesIO()
        file.save(data)
        data = data.getvalue().decode('utf-8')
        data = io.StringIO(data)
        df_pred = pd.read_csv(data)

        for col in ['name', *FIELDS]:
            if col not in df_pred.columns:
                return 'Invalid: Lack of column {}'.format(col)
        if not (df_pred.name == df_true.name).all():
            return 'Invalid: names are not correct'
        if not all(is_float_dtype(df_pred[field]) for field in FIELDS):
            return 'Invalid: Expect data to be float'

        y_pred = df_pred[FIELDS].values.reshape(-1, 4, 2)
        rmse = np.sqrt(((y_true - y_pred) ** 2).sum(axis=2).mean()).item()

        print(rmse)

        return jsonify({
            'rmse': round(rmse, 3),
        })
    except:
        return jsonify({
            "error_msg": traceback.format_exc()
        })

@app.route("/dataset", methods=["GET"])
def Dataset():
    try:
        return send_file(os.path.join(base_path, "../static/assets/ccpd6000.zip"), as_attachment=True, mimetype="application/x-zip-compressed")
    except:
        return jsonify({
            "error_msg": traceback.format_exc()
        })

@app.route("/code", methods=["GET"])
def Code():
    try:
        path = os.path.join(base_path, "../static/assets/HW3.zip")
        return send_file(path, as_attachment=True)
    except:
        return jsonify({
            "error_msg": traceback.format_exc()
        })
