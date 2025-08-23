import requests
import random
import smtplib
from email.mime.text import MIMEText
import time

# ---------- CONFIG ----------
URL = "https://cssp.examinations.ie/auth/login"
PAYLOAD = {
    "exam_number": "EXAM NUMBER", 
    "password": "PORTAL PASSWORD", 
    "lang": "en"
}

EXPECTEDRESPONSE = {
    "results_live": False,
    "message": "Your Login details are correct.  The Leaving Certificate 2025 results will be available from 10a.m. Friday 22 August"
}
EMAIL_TO = ["EMAIL 1", "EMAIL 2", "EMAIL 3"]
EMAIL_FROM = "GMAIL ACCOUNT EMAIL"
EMAIL_PASSWORD = "GMAIL APP PASSWORD"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# -----------------------------

def send_email(subject, body, to_email):
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = EMAIL_FROM
    message["To"] = ", ".join(to_email) 

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(message)

def main():
    while True:
        CHECKINTERVAL = random.uniform(1, 40)
        try:
            request = requests.post(URL, json=PAYLOAD, timeout=5)
            data = request.json()
            currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            print(f"[{currentTime}] Checked:", data)

            if data != EXPECTEDRESPONSE:
                send_email(
                    "Leaving Certificate Results Live!",
                    f"The portal response changed:\n\n{data}\n\nTime detected: {currentTime}",
                    EMAIL_TO
                )
                print("Results live – email sent. Exiting.")
                break
        except Exception as exception:
            print("Error checking:", exception)

        time.sleep(CHECKINTERVAL)

if __name__ == "__main__":
    main()