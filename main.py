import imaplib
import email
import os
from email.utils import parsedate_to_datetime

SAVE_DIR = "Payslips"
os.makedirs(SAVE_DIR, exist_ok=True)

MAIL = imaplib.IMAP4_SSL("imap.gmail.com")
MAIL.login("theyafen@gmail.com", "koae qwuh xdty uyom")

MAIL.select("inbox")

status, messages = MAIL.search(None, '(FROM "ritao@accupos.com")')

def build_filename(date, directory):
    year = date.year
    month = f"{date.month:02d}"

    base = f"Payslip_{year}_{month}.pdf"
    path = os.path.join(directory, base)

    if not os.path.exists(path):
        return base
    else:
        return None
    

for num in messages[0].split():
    status, data = MAIL.fetch(num, "(RFC822)")
    msg = email.message_from_bytes(data[0][1])

    # Getting mail date
    msg_date = parsedate_to_datetime(msg["Date"])

    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            payload = part.get_payload(decode=True)
            if not payload:
                continue

            filename = build_filename(msg_date, SAVE_DIR)

            if not filename:
                print("Exists, continue...")
                continue
            
            full_path = os.path.join(SAVE_DIR, filename)

            print(f"Before: {full_path}")
                      
            with open(os.path.join(SAVE_DIR, filename), "wb") as f:
                f.write(payload)
