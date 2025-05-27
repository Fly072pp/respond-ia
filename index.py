import imaplib
import smtplib
import email
from email.message import EmailMessage
import requests
import time

# === CONFIGURATION ===
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""  # mot de passe d'application
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === MOTS CLÉS AUTOMATIQUES ===
AUTO_KEYWORDS = ["newsletter", "notification", "no-reply", "noreply", "digest", "alerte", "abonnement"]

# === FONCTION POUR VÉRIFIER SI C’EST UN MAIL AUTOMATIQUE ===
def is_automated_email(from_address, subject, msg):
    from_lower = from_address.lower()
    subject_lower = (subject or "").lower()

    # Vérifie les mots dans l'adresse ou le sujet
    if any(keyword in from_lower for keyword in AUTO_KEYWORDS):
        return True
    if any(keyword in subject_lower for keyword in AUTO_KEYWORDS):
        return True

    # Vérifie les en-têtes automatiques
    auto_headers = ["Auto-Submitted", "Precedence", "X-Auto-Response-Suppress", "X-Mailer"]
    for header in auto_headers:
        value = msg.get(header, "").lower()
        if "auto" in value or "bulk" in value or "junk" in value:
            return True

    return False

# === SE CONNECTER À LA BOITE MAIL ===
def get_latest_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        mail_ids = messages[0].split()

        if not mail_ids:
            return None, None, None

        for email_id in reversed(mail_ids):  # du plus récent au plus ancien
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            subject = msg["subject"] or "(Sans sujet)"
            from_address = email.utils.parseaddr(msg["From"])[1]

            if is_automated_email(from_address, subject, msg):
                print(f"Email ignoré (automatique) : {from_address} - {subject}")
                continue

            # Lire le contenu
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                        except UnicodeDecodeError:
                            body = part.get_payload(decode=True).decode('latin-1')
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode()
                except UnicodeDecodeError:
                    body = msg.get_payload(decode=True).decode('latin-1')

            return subject, body.strip(), from_address

        return None, None, None  # Tous les mails étaient automatiques

    except Exception as e:
        print(f"Erreur lors de la récupération de l'e-mail : {e}")
        return None, None, None

# === APPEL DE L’IA POLLINATIONS ===
def get_ai_response(prompt):
    try:
        url = f"https://text.pollinations.ai/{prompt}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"(Erreur IA: {response.status_code})"
    except Exception as e:
        return f"(Erreur appel IA: {e})"

# === ENVOYER UNE RÉPONSE ===
def send_email(to_address, subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_address
        msg["Subject"] = f"Re: {subject}"
        msg.set_content(body)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Réponse envoyée à :", to_address)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# === BOUCLE PRINCIPALE ===
while True:
    subject, body, sender = get_latest_email()
    if body:
        print(f"Nouveau mail de {sender} : {subject}")
        prompt = f"Réponds à ce mail de manière professionnelle : {body}"
        ai_reply = get_ai_response(prompt)
        send_email(sender, subject, ai_reply)
    else:
        print("Aucun nouveau mail ou mail ignoré.")
    time.sleep(30)
