from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def load_eml(path):
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return msg

def strip_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def parse_eml(path):
    msg = load_eml(path)

    sender = msg.get("From", "")
    receiver = msg.get("To", "")
    subject = msg.get("Subject", "")
    date = msg.get("Date", "")

    body_text = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            payload = part.get_payload(decode=True)

            if payload is None:
                continue
            
            
            try:
                decoded = payload.decode(errors="ignore")
            except:
                decoded = ""

            if ctype == "text/plain":
                body_text += decoded

            elif ctype == "text/html":
                body_text += strip_html(decoded)

    else:
        # not multipart — could be plain or HTML
        raw = msg.get_payload(decode=True).decode(errors="ignore")
        if "<html" in raw.lower():
            body_text = strip_html(raw)
        else:
            body_text = raw

    return sender, receiver, subject, body_text, date

