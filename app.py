from flask import Flask, request, redirect, url_for, render_template, session
import warnings
import numpy as np
import pandas as pd
import pickle
import openpyxl
from collections import Counter
import operator
from Treatment import diseaseDetail
from utils import preprocess_user_symptoms, get_similar_symptoms, build_input_vector, load_model, get_top_predictions_with_confidence

warnings.simplefilter("ignore")

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'super secret key'

# Load datasets and model once
DF_COMB = pd.read_csv("Dataset/dis_sym_dataset_comb.csv")
DF_NORM = pd.read_csv("Dataset/dis_sym_dataset_norm.csv")
X = DF_COMB.iloc[:, 1:]
Y = DF_COMB.iloc[:, 0:1]
SYMPTOM_COLUMNS = list(X.columns)
MODEL = load_model("model_saved")

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/demo", methods=["GET"])
def demo():
    return render_template("demo.html")

@app.route("/nearest-doctor", methods=["GET"])
def nearest_doctor():
    return render_template("nearest-doctor.html")

@app.route("/predict", methods=["POST"])
def predict():
    user_symptoms = request.form.get('symptoms', '').split(',')
    user_symptoms = preprocess_user_symptoms(user_symptoms)
    found_symptoms = get_similar_symptoms(SYMPTOM_COLUMNS, user_symptoms)

    session['candidate_symptoms'] = found_symptoms

    dis_list = set()
    for symp in found_symptoms:
        dis_list.update(set(DF_NORM[DF_NORM[symp] == 1]['label_dis']))

    counter_list = []
    for dis in dis_list:
        row = DF_NORM.loc[DF_NORM['label_dis'] == dis].values.tolist()[0][1:]
        for idx, val in enumerate(row):
            if val and SYMPTOM_COLUMNS[idx] not in found_symptoms:
                counter_list.append(SYMPTOM_COLUMNS[idx])

    suggestions = [sym for sym, _ in Counter(counter_list).most_common()]
    session['final_symptoms'] = found_symptoms
    session['suggested_symptoms'] = suggestions

    return render_template("predict.html", found_symptoms=enumerate(found_symptoms), another_symptoms=enumerate(suggestions), count=len(suggestions), dict_symp_tup=len(suggestions))

@app.route("/next", methods=["POST"])
def next():
    selected = request.form.get('relevance', '').split(',')
    all_symptoms = session.get('final_symptoms', []) + selected
    sample_x = build_input_vector(all_symptoms, SYMPTOM_COLUMNS)
    session['sample_x'] = sample_x
    session['all_symptoms'] = all_symptoms
    return render_template("next.html", my_var2=enumerate(all_symptoms))

@app.route("/final", methods=["POST"])
def final():
    sample_x = session.get('sample_x')
    all_symptoms = session.get('all_symptoms', [])
    diseases = sorted(set(Y['label_dis']))

    results = get_top_predictions_with_confidence(
        MODEL, sample_x, all_symptoms, SYMPTOM_COLUMNS, DF_NORM, diseases
    )

    return render_template("final.html", arr=results)

@app.route("/treatment", methods=["POST", "GET"])
def treatment():
    treat_dis = request.form.get('dis', '').strip().lower()
    workbook = openpyxl.load_workbook('cure_minor.xlsx')
    worksheet = workbook['Sheet1']
    for row in worksheet.iter_rows(values_only=True):
        disease_name = str(row[0]).strip().lower()
        if treat_dis == disease_name:
            treatments = ''.join(str(cell) for cell in row[1:] if cell).split(',')
            return render_template("treatment.html", ans=treatments)
    return render_template("treatment.html", ans=["No treatment info found."])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
