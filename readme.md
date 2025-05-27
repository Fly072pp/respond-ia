Voici un exemple de fichier **README.md** pour ton script Python de réponse automatique aux emails avec IA :

````markdown
# Répondeur Automatique d'Emails avec IA

Ce script Python permet de récupérer automatiquement les emails non lus d'une boîte Gmail, d'ignorer les emails automatiques (newsletters, notifications, etc.), de générer une réponse professionnelle à l'aide d'une IA (Pollinations) et d'envoyer cette réponse par email.

---

## Fonctionnalités

- Connexion sécurisée à une boîte Gmail via IMAP et SMTP.
- Filtrage automatique des emails de type newsletters, notifications ou autres emails automatiques.
- Extraction du contenu des emails texte (plain text).
- Envoi de requêtes à une IA via une API publique pour générer une réponse personnalisée et professionnelle.
- Envoi automatique de la réponse à l'expéditeur du mail.
- Fonctionnement en boucle avec une pause de 30 secondes entre chaque vérification.

---

## Prérequis

- Python 3.x
- Modules Python suivants :
  - `imaplib`
  - `smtplib`
  - `email`
  - `requests`
  - `time`

Ces modules sont pour la plupart intégrés à Python, sauf `requests` à installer via pip :

```bash
git clone https://github.com/tonpseudo/mail-auto-reply-bot.git
cd mail-auto-reply-bot
pip install requests
````

---

## Configuration

Modifie les variables suivantes dans le script :

```python
EMAIL_ADDRESS = "ton.email@gmail.com"
EMAIL_PASSWORD = "ton_mot_de_passe_application"  # Mot de passe d'application Gmail
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

> **Important** : Utilise un mot de passe d'application Gmail (via Google Account > Sécurité > Mots de passe d'application) pour l'authentification.

---

## Utilisation

Lance simplement le script Python. Il vérifie toutes les 30 secondes la présence de nouveaux emails non lus, filtre ceux automatiques, puis répond automatiquement aux emails légitimes via l'API Pollinations.

```bash
python index.py
```

---

## Fonctionnement technique

1. Connexion IMAP sécurisée à Gmail pour lire les emails non lus.
2. Filtrage via mots-clés et en-têtes pour détecter les emails automatiques.
3. Récupération du corps du mail (texte brut).
4. Envoi du contenu à l'API Pollinations pour générer une réponse.
5. Envoi de la réponse via SMTP avec TLS.
6. Recommence la boucle après 30 secondes.

---

## Remarques

* L'API Pollinations est utilisée ici en GET simple sur l'URL `https://text.pollinations.ai/{prompt}`. La fiabilité dépend du service tiers.
* Le script ne gère que les emails en texte brut, pas les emails HTML ou pièces jointes.
* À utiliser avec précaution, car un envoi automatique massif peut être bloqué par Gmail.
* Assure-toi que la boîte Gmail a activé l'accès IMAP.

---

## Licence

Ce projet est libre et ouvert. Utilisation et modification à votre convenance.

---

## Auteur

Fly

---

N'hésitez pas à faire des pulls requests

