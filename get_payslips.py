<<<<<<< HEAD
=======
#!/mnt/c/TheYafen/scripts/save_tlushim/.venv/bin/python
>>>>>>> 9796c69 (from home)
import imaplib
import email
import os
from email.utils import parsedate_to_datetime

<<<<<<< HEAD
SAVE_DIR = "Payslips"
os.makedirs(SAVE_DIR, exist_ok=True)

MAIL = imaplib.IMAP4_SSL("imap.gmail.com")
MAIL.login("theyafen@gmail.com", "koae qwuh xdty uyom")

MAIL.select("inbox")

status, messages = MAIL.search(None, '(FROM "ritao@accupos.com")')
=======
SAVE_DIR = "payslips"
SENDER = "ritao@accupos.com"
SEARCH_CRITERIA = f'(UNSEEN FROM "{SENDER}")'
POLL_SECONDS = 30

os.makedirs(SAVE_DIR, exist_ok=True)

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "theyafen@gmail.com"
IMAP_PASS = "koae qwuh xdty uyom"


def connect_mail():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")
    return mail
>>>>>>> 9796c69 (from home)

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
    for num in messages[0].split():
        status, data = MAIL.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        # Getting mail date
        msg_date = parsedate_to_datetime(msg["Date"])

        files_names_list = []

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
<<<<<<< HEAD
                
=======

>>>>>>> 9796c69 (from home)
                files_names_list.append(filename)

                print(f"Saving: {full_path}")
                        
                with open(os.path.join(save_dir, filename), "wb") as f:
                    f.write(payload)
    return files_names_list

if __name__ == "__main__":
    a = get_latest_payslip()