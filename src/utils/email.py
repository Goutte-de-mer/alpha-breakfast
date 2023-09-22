from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from jinja2 import Template
import re

# Config SMTP
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")

email_regex = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


# Fonction pour valider la conformité de l'email rentré
def is_valid_email(email):
    if re.fullmatch(email_regex, email) and len(email) <= 256:
        return True
    else:
        return False


# Fonction d'envoi de mail
def send_email(email, subject, template_name, variables):
    # Config de l'email
    sender_email = "from@example.com"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    # Définit le répertoire des modèles d'e-mails
    email_templates_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "templates", "mails"
    )

    # Utilise email_templates_dir pour charger le modèle d'e-mail
    template_path = os.path.join(email_templates_dir, template_name)
    with open(template_path, "r") as file:
        email_template = Template(file.read())

    # Remplace les placeholders dans le contenu HTML avec les variables fournies
    email_content = email_template.render(**variables)

    # Incorpore le contenu HTML dans le corps du message
    message = MIMEText(email_content, "html")
    msg.attach(message)

    try:
        # Connexion au serveur SMTP de Mailtrap
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)

        # Envoi de l'e-mail
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        return True
    except smtplib.SMTPConnectError as e:
        # Gérez la connexion au serveur SMTP en cas d'erreur
        print(f"Erreur lors de la connexion au serveur SMTP : {e}")
    except smtplib.SMTPAuthenticationError as e:
        # Gérez l'authentification SMTP en cas d'erreur
        print(f"Erreur d'authentification SMTP : {e}")
    except Exception as e:
        # Gérez d'autres exceptions SMTP ou erreurs génériques ici
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")


# Envoi du mail d'annulation d'événement
def send_cancellation_emails(event, participations):
    current_date = datetime.now().date()

    if event.date >= current_date:
        participants_emails = [
            participation.user.email for participation in participations
        ]

        email_subject = "Annulation petit déjeuner d'Alpha"
        email_template_name = "event_cancellation.html"
        email_variables = {"event_date": event.date, "event_time": event.start_time}

        for email in participants_emails:
            send_email(email, email_subject, email_template_name, email_variables)
