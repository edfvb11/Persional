"""
Monitor de citas - Embajada del Japón en Colombia
Revisa el calendario de agendamiento y envía un correo cuando aparece
un día con cupo disponible que antes no lo tenía.
"""

import json
import os
import smtplib
import time
import random
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent  # <-- NUEVO: Importar generador de User-Agents

URL = "https://embjpcol.rsvsys.jp/reservations/calendar"
STATE_FILE = "state.json"


def obtener_estado():
    """Descarga el calendario y devuelve {dia: disponible(bool)}."""
    
    # 1. Inicializar el generador de User-Agents y crear una Sesión
    ua = UserAgent()
    session = requests.Session()
    
    # 2. Generar headers realistas (simulando un navegador Chrome real)
    headers = {
        'User-Agent': ua.random,  # Navegador aleatorio en cada ejecución
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-CO,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    session.headers.update(headers)
    
    # 3. Añadir un retraso aleatorio antes de la petición (Comportamiento humano)
    # Los bots piden la página en el milisegundo exacto, los humanos tardan segundos
    time.sleep(random.uniform(2.0, 5.0))
    
    # 4. Hacer la petición usando la sesión configurada
    resp = session.get(URL, timeout=30)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, "html.parser")

    estado = {}
    for celda in soup.select("td"):
        texto = celda.get_text(strip=True)
        if not texto or not texto.isdigit():
            continue  # celda vacía o que no corresponde a un día

        img = celda.find("img")
        if img and img.get("src"):
            # Los íconos "disabled" son los días sin cupo (受付終了).
            # Cualquier otro ícono se interpreta como día con cupo (受付中).
            disponible = "disabled" not in img["src"].lower()
        else:
            disponible = False

        estado[texto] = disponible

    return estado


def cargar_estado_previo():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_estado(estado):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)


def enviar_correo(dias_nuevos):
    remitente = os.environ["GMAIL_USER"]
    clave = os.environ["GMAIL_APP_PASSWORD"]
    destinatario = os.environ.get("NOTIFY_EMAIL", remitente)

    cuerpo = (
        "Se detectó cupo disponible para los siguientes días:\n\n"
        + "\n".join(f"- Día {d}" for d in dias_nuevos)
        + f"\n\nAgenda ya, los cupos vuelan: {URL}"
    )

    msg = MIMEText(cuerpo)
    msg["Subject"] = "¡Cupo disponible en la Embajada de Japón!"
    msg["From"] = remitente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(remitente, clave)
        server.sendmail(remitente, [destinatario], msg.as_string())


def main():
    estado_actual = obtener_estado()
    estado_previo = cargar_estado_previo()

    dias_nuevos = [
        dia
        for dia, disponible in estado_actual.items()
        if disponible and not estado_previo.get(dia, False)
    ]

    if dias_nuevos:
        print(f"Cupos nuevos detectados: {dias_nuevos}")
        enviar_correo(dias_nuevos)
    else:
        print("Sin cambios. No hay cupos nuevos.")

    guardar_estado(estado_actual)


if __name__ == "__main__":
    main()
