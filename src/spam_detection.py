import sys

from classify import classify_eml

if __name__ == "__main__":
    eml_path = sys.argv[1]
    label, prob = classify_eml(eml_path)

    print("Spam?" , "YES" if label == 1 else "NO")
    print("Spam Probability:", prob)