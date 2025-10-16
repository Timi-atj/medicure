import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from itertools import combinations
import pickle
import numpy as np
import requests
from bs4 import BeautifulSoup

# --- NLTK Resource Setup (auto-download if missing) ---
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

try:
    _ = wordnet.synsets('disease')
except LookupError:
    nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

def synonyms(term):
    syns = set()
    try:
        response = requests.get(f'https://www.thesaurus.com/browse/{term}', timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        container = soup.find('section', {'class': 'MainContentContainer'})
        row = container.find('div', {'class': 'css-191l5o0-ClassicContentCard'})
        for x in row.find_all('li'):
            syns.add(x.get_text())
    except:
        pass
    for syn in wordnet.synsets(term):
        syns.update(syn.lemma_names())
    return syns

def preprocess_user_symptoms(symptom_list):
    processed = []
    for sym in symptom_list:
        sym = sym.strip().replace('-', ' ').replace("'", '')
        tokens = tokenizer.tokenize(sym)
        lems = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
        processed.append(' '.join(lems))

    enriched = []
    for sym in processed:
        words = sym.split()
        related = set()
        for i in range(1, len(words)+1):
            for combo in combinations(words, i):
                phrase = ' '.join(combo)
                related.update(synonyms(phrase))
        related.add(sym)
        enriched.append(' '.join(related).replace('_', ' '))
    return enriched

def get_similar_symptoms(dataset_symptoms, user_symptoms):
    found = set()
    for ds in dataset_symptoms:
        ds_words = ds.split()
        for us in user_symptoms:
            match = sum(1 for word in ds_words if word in us.split())
            if match / len(ds_words) > 0.5:
                found.add(ds)
    return list(found)

def build_input_vector(selected_symptoms, dataset_symptoms):
    vector = [0] * len(dataset_symptoms)
    for sym in selected_symptoms:
        if sym in dataset_symptoms:
            idx = dataset_symptoms.index(sym)
            vector[idx] = 1
    return vector

def load_model(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

def get_top_predictions_with_confidence(model, input_vector, user_symptoms, symptom_columns, df_norm, diseases):
    probas = model.predict_proba([input_vector])[0]
    topk = np.argsort(probas)[-5:][::-1]
    
    results = []
    for idx in topk:
        label = diseases[idx]
        confidence = round(probas[idx] * 100, 2)  # Actual percentage
        results.append((label, confidence))
    return results


