import pandas as pd
import re

from email.utils import parseaddr

# df = pd.read_csv("../dataset/raw/CEAS_08.csv")

# df[["sender", "receiver", "subject", "body", "date"]] = (
#     df[["sender", "receiver", "subject", "body", "date"]].fillna("").astype(str)
# )

SPAM_WORDS = [
    # Financial
    "free", "win", "winner", "prize", "cash", "money",
    "bonus", "reward", "lottery", "gift",

    # Urgency
    "urgent", "immediately", "action required", "final notice",
    "important", "alert", "warning",

    # Credential theft
    "verify", "confirm", "password", "account", "login",
    "unauthorized", "security", "reset", "access",

    # Phishing actions
    "click", "open", "review", "download", "invoice", "statement",

    # Commercial
    "offer", "promo", "sale", "discount", "limited time"
]

TZ_MAP = {
    "UT": "+0000",
    "UTC": "+0000",
    "GMT": "+0000",
    "EST": "-0500",
    "EDT": "-0400",
    "CST": "-0600",
    "CDT": "-0500",
    "MST": "-0700",
    "MDT": "-0600",
    "PST": "-0800",
    "PDT": "-0700",
}

def normalize_timezone(date_str):
    if not isinstance(date_str, str):
        return date_str
    
    # Match the timezone token at the end of the string
    match = re.search(r"\b([A-Z]{2,4})$", date_str.strip())
    
    if match:
        tz = match.group(1)
        if tz in TZ_MAP:
            # Replace only the ending timezone token
            return re.sub(r"\b" + tz + r"$", TZ_MAP[tz], date_str.strip())
    
    return date_str

def extract_features(row):
  features = {}

  # Sender Format: Full Name <Local@Domain>
  sender = str(row["sender"])
  sender_name, sender_email = parseaddr(sender)
  sender_domain = sender_email.split("@")[-1].lower() if "@" in sender_email else ""
  
  #features["sender_domain"] = sender_domain
  features["sender_has_numbers"] = int(bool(re.search(r"\d", sender)))
  features["sender_domain_length"] = len(sender_domain)

  # Receiver Format: Local@Domain
  receiver = str(row["receiver"])
  receiver_name, receiver_email = parseaddr(receiver)
  receiver_domain = receiver_email.split("@")[-1].lower() if "@" in receiver_email else ""
  #features["receiver_domain"] = receiver_domain
  features["domain_mismatch"] = int(sender_domain != receiver_domain)

  # Subject
  subject = str(row["subject"])
  features["subject_text"] = subject
  features["subject_length"] = len(subject)

  features["subject_num_exclamations"] = subject.count("!")
  features["subject_num_question"] = subject.count("?")
  features["subject_max_repeated_punct"] = max(
    (len(m.group(0)) for m in re.finditer(r"([!?.,])\1{1,}", subject)),
    default=1
  )

  features["subject_num_caps"] = sum(1 for c in subject if c.isupper())
  features["subject_has_spam_words"] = int(any(
      w in subject.lower() for w in SPAM_WORDS
  ))

  # Body
  body = str(row["body"])
  features["body_text"] = body
  features["body_length"] = len(body)

  features["body_num_links"] = len(re.findall(r"https?://", body.lower()))

  features["body_num_exclamations"] = body.count("!")
  features["body_num_question"] = body.count("?")
  features["body_max_repeated_punct"] = max(
    (len(m.group(0)) for m in re.finditer(r"([!?.,])\1{1,}", body)),
    default=1
)

  features["body_num_caps"] = sum(1 for c in body if c.isupper())
  features["body_has_spam_words"] = int(any(
      w in body.lower() for w in SPAM_WORDS
  ))

  # Date
  date_str = str(row["date"])
  date_clean = normalize_timezone(date_str)
  dt = pd.to_datetime(date_clean, errors="coerce")
  features["email_hour"] = dt.hour if not pd.isna(dt) else -1
  features["email_day_of_week"] = dt.dayofweek if not pd.isna(dt) else -1

  return features