

import joblib
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import seaborn as sns
from feature_extraction import extract_features


new_df = pd.read_csv("./dataset/raw/SpamAssasin.csv")

print(new_df["label"].value_counts())

features_list = [extract_features(row) for _, row in new_df.iterrows()]
test_features_df = pd.DataFrame(features_list)

pipeline = joblib.load("./models/spam_detector.pkl")

preds = pipeline.predict(test_features_df)
probs = pipeline.predict_proba(test_features_df)[:, 1]

print("Accuracy:", accuracy_score(new_df["label"], preds))
print(classification_report(new_df["label"], preds, digits=5))

cm = confusion_matrix(new_df["label"], preds)

# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.show()


fpr, tpr, thresholds = roc_curve(new_df["label"], probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(7, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.4f})")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # random model line

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver Operating Characteristic (ROC)")
plt.legend()
plt.grid(True)
plt.show()