#!/mnt/c/TheYafen/scripts/save_tlushim/.venv/bin/python
from email.utils import parsedate_to_datetime
from email.header import decode_header
import imaplib
import email
import os
from dotenv import load_dotenv


SAVE_DIR = "payslips"
SENDER = "ritao@accupos.com"
TOFES = "טופס"
TLUSH = "תלוש"
SEARCH_CRITERIA = f'(FROM "{SENDER}")'
POLL_SECONDS = 30

os.makedirs(SAVE_DIR, exist_ok=True)

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "theyafen@gmail.com"

load_dotenv()
IMAP_PASS = os.getenv("IMAP_PASS")
print(IMAP_PASS)


def connect_mail():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")
    status, messages = mail.search(None, SEARCH_CRITERIA)
    return status, messages, mail

def build_filename(date, directory):
    year = date.year
    month = f"{date.month:02d}"

    base = f"Payslip_{year}_{month}.pdf"
    path = os.path.join(directory, base)

    if not os.path.exists(path):
        return base
    else:
        return None
    

def get_latest_payslip(save_dir=SAVE_DIR):
    status, messages, mail = connect_mail()
    i = 0
    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        files_names_list = []

        # Getting mail subject
        raw_subject = msg["Subject"]
        subject, encoding = decode_header(raw_subject)[0]
        subject = subject.decode(encoding)
        #print(subject)
        if TLUSH not in subject:
            continue

        # Getting mail date
        msg_date = parsedate_to_datetime(msg["Date"])

        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                payload = part.get_payload(decode=True)
                if not payload:
                    continue

                filename = build_filename(msg_date, save_dir)

                if not filename:
                    print("Exists, continue...")
                    continue
                
                full_path = os.path.join(save_dir, filename)

                files_names_list.append(filename)

                print(f"Saving: {full_path}")
                        
                with open(os.path.join(save_dir, filename), "wb") as f:
                    f.write(payload)
    return files_names_list

if __name__ == "__main__":
    a = get_latest_payslip()
