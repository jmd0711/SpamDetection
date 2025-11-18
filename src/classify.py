import joblib
import pandas as pd
from feature_extraction import extract_features
from parse_eml import parse_eml

pipeline = joblib.load("./models/spam_detector.pkl")

def eml_to_features(path):
    sender, receiver, subject, body, date = parse_eml(path)

    row = {
        "sender": sender,
        "receiver": receiver,
        "subject": subject,
        "body": body,
        "date": date,
    }

    return extract_features(row)

def classify_eml(path):
    features = eml_to_features(path)
    df = pd.DataFrame([features])
    
    pred = pipeline.predict(df)[0]
    prob = pipeline.predict_proba(df)[0][1]

    return pred, prob