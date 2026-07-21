"""
Script de prueba para verificar que el envío de correos funciona correctamente.
Envía un correo de prueba a través de Gmail SMTP.
"""

import os
import smtplib
from email.mime.text import MIMEText

def test_email():
    remitente = os.environ.get("GMAIL_USER")
    clave = os.environ.get("GMAIL_APP_PASSWORD")
    destinatario = os.environ.get("NOTIFY_EMAIL", remitente)

    if not remitente or not clave:
        print("❌ Error: GMAIL_USER o GMAIL_APP_PASSWORD no están configurados")
        return False

    msg = MIMEText("¡Este es un correo de prueba! Si lo ves, todo funciona correctamente.")
    msg["Subject"] = "TEST: Correo desde GitHub Actions"
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        print(f"📧 Intentando enviar correo de prueba...")
        print(f"   De: {remitente}")
        print(f"   Para: {destinatario}")
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remitente, clave)
            server.sendmail(remitente, [destinatario], msg.as_string())
        
        print("✅ Correo enviado exitosamente")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
        print("   Verifica que GMAIL_USER y GMAIL_APP_PASSWORD sean correctos")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = test_email()
    exit(0 if success else 1)
